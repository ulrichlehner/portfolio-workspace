"""Synthetic TLS server; no external networking or real portfolio data."""
import contextlib
import http.server
import io
import json
import os
from pathlib import Path
import shutil
import ssl
import subprocess
import tempfile
import threading
import time
import unittest
from unittest.mock import patch
import zipfile

import pp_dev_data as data
from pp_dev import DevError

XML = b'<?xml version="1.0" encoding="UTF-8"?><client><version>70</version><securities/></client>'


class DataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cert_temp = tempfile.TemporaryDirectory()
        cls.cert = Path(cls.cert_temp.name) / 'cert.pem'
        cls.key = Path(cls.cert_temp.name) / 'key.pem'
        subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:2048', '-nodes',
                        '-keyout', str(cls.key), '-out', str(cls.cert), '-days', '1',
                        '-subj', '/CN=localhost', '-addext', 'subjectAltName=DNS:localhost'],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @classmethod
    def tearDownClass(cls):
        cls.cert_temp.cleanup()

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.storage = self.root / 'pp-dev-data'
        self.config = self.root / 'config.json'
        self.requests = []
        self.paths = []
        self.status = 200
        self.body = XML
        self.length = None
        self.delay = 0
        parent = self

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parent.requests.append((self.command, self.headers.get('Authorization')))
                parent.paths.append(self.path)
                self.send_response(parent.status)
                self.send_header('Content-Length', str(parent.length or len(parent.body)))
                self.send_header('Location', 'https://other.invalid/private')
                self.end_headers()
                time.sleep(parent.delay)
                try:
                    self.wfile.write(parent.body)
                except (BrokenPipeError, ssl.SSLError):
                    pass
                self.close_connection = True

            def log_message(self, *args):
                pass

        self.server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        tls = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls.load_cert_chain(self.cert, self.key)
        self.server.socket = tls.wrap_socket(self.server.socket, server_side=True)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.stop_server)
        self.write_config()
        self.trusted = ssl.create_default_context(cafile=str(self.cert))
        self.store = data.Generations(self.storage)

    def stop_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    def write_config(self, **updates):
        config = {'url': 'https://localhost:' + str(self.server.server_port) + '/synthetic.xml',
                  'format': 'xml', 'read_only_confirmed': True,
                  'auth': {'method': 'bearer', 'token': 'synthetic-secret'}}
        config.update(updates)
        self.config.write_text(json.dumps(config))
        self.config.chmod(0o600)

    def refresh(self):
        with patch('pp_dev_data.ssl.create_default_context', return_value=self.trusted):
            return self.store.refresh(self.config, {'revision': 'synthetic'})

    def test_get_only_and_no_credentials_in_output(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            generation = self.refresh()
            self.store.report(generation)
        self.assertEqual([('GET', 'Bearer synthetic-secret')], self.requests)
        for private in ('synthetic-secret', 'localhost', 'synthetic.xml'):
            self.assertNotIn(private, output.getvalue())

    def test_changed_remote_preserves_local_edits_and_adjacent_files(self):
        first = self.refresh()
        self.store.working(first).write_bytes(b'local edits')
        (first / 'Development-Copy.xml.backup').write_bytes(b'backup')
        self.body = XML.replace(b'70', b'69')
        second = self.refresh()
        self.assertEqual(b'local edits', self.store.working(first).read_bytes())
        self.assertEqual(b'backup', (first / 'Development-Copy.xml.backup').read_bytes())
        self.assertEqual(self.body, self.store.working(second).read_bytes())
        self.assertEqual(XML, (first / 'baseline').read_bytes())
        self.assertNotEqual((second / 'baseline').stat().st_ino, self.store.working(second).stat().st_ino)

    def test_unchanged_remote_uses_baseline_not_local_edits(self):
        first = self.refresh()
        self.store.working(first).write_bytes(b'local edits')
        second = self.refresh()
        self.assertEqual(XML, self.store.working(second).read_bytes())
        self.assertEqual(XML, (first / 'baseline').read_bytes())
        self.assertEqual(['GET', 'GET'], [method for method, _ in self.requests])

    def test_previous_retained_and_older_pruned_after_success(self):
        first, second, third = self.refresh(), self.refresh(), self.refresh()
        self.assertFalse(first.exists())
        self.assertTrue(second.exists())
        self.assertEqual(third, self.store.current())

    def test_keep_prevents_pruning(self):
        first = self.refresh()
        (first / 'keep').touch()
        self.refresh()
        self.refresh()
        self.assertTrue(first.exists())

    def test_failures_preserve_active_and_previous(self):
        first, second = self.refresh(), self.refresh()
        for status in (301, 302, 307, 308, 401, 403, 500):
            self.status = status
            with self.assertRaises(DevError):
                self.refresh()
            self.assertEqual(second, self.store.current())
            self.assertTrue(first.exists())
        self.assertEqual(9, len(self.requests))

    def test_untrusted_tls_rejected(self):
        with self.assertRaises(DevError):
            self.store.refresh(self.config, {})
        self.assertIsNone(self.store.current())
        self.assertEqual([], self.requests)

    def test_hostname_verification(self):
        config = json.loads(self.config.read_text())
        self.write_config(url=config['url'].replace('localhost', '127.0.0.1'))
        with self.assertRaises(DevError):
            self.refresh()
        self.assertEqual([], self.requests)

    def test_interrupted_download_preserves_current(self):
        first = self.refresh()
        self.length = len(XML) + 100
        with self.assertRaises(DevError):
            self.refresh()
        self.assertEqual(first, self.store.current())
        self.assertEqual([], list(self.storage.glob('.staging-*')))

    def test_error_body_and_malformed_xml_rejected(self):
        first = self.refresh()
        for body in (b'<html>error</html>', b'<client version="69">', b'',
                     b'<!DOCTYPE client [<!ENTITY x "x">]><client version="69">&x;</client>'):
            self.body = body
            with self.assertRaises(DevError):
                self.refresh()
            self.assertEqual(first, self.store.current())

    def test_size_and_deadline_limits(self):
        with patch('pp_dev_data.MAX_BYTES', 2):
            with self.assertRaises(DevError):
                self.refresh()
        with patch('pp_dev_data.DEADLINE', -1):
            with self.assertRaises(DevError):
                self.refresh()
        self.assertIsNone(self.store.current())

    def test_no_read_only_confirmation(self):
        self.write_config(read_only_confirmed=False)
        with self.assertRaises(DevError):
            self.refresh()
        self.assertEqual([], self.requests)

    def test_total_deadline_interrupts_a_stalled_response(self):
        first = self.refresh()
        self.delay = 0.2
        with patch('pp_dev_data.DEADLINE', 0.05):
            with self.assertRaises(DevError):
                self.refresh()
        self.assertEqual(first, self.store.current())

    def test_http_userinfo_and_invalid_auth_rejected(self):
        for url in ('http://localhost/file', 'https://user:password@localhost/file',
                    'https://localhost/file#fragment'):
            self.write_config(url=url)
            with self.assertRaises(DevError):
                self.refresh()
        self.write_config(auth={'method': 'bearer', 'token': 'bad\r\nheader'})
        with self.assertRaises(DevError):
            self.refresh()
        self.assertEqual([], self.requests)

    def test_basic_auth(self):
        self.write_config(auth={'method': 'basic', 'username': 'synthetic', 'password': 'test-only'})
        self.refresh()
        self.assertTrue(self.requests[0][1].startswith('Basic '))

    def test_spaces_and_unicode_in_source_path_are_encoded(self):
        self.write_config(url='https://localhost:' + str(self.server.server_port) + '/space and ü.xml')
        self.refresh()
        self.assertEqual(['/space%20and%20%C3%BC.xml'], self.paths)

    def test_private_config_permissions_and_links(self):
        self.config.chmod(0o644)
        with self.assertRaises(DevError):
            self.refresh()
        self.config.chmod(0o600)
        other = self.root / 'link'
        os.link(self.config, other)
        with self.assertRaises(DevError):
            self.refresh()

    def test_zip_xml_and_protobuf_container(self):
        for name, payload in [('data.xml', XML), ('data.portfolio', b'PPPBV1\x08\x46\x12\x03EUR')]:
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w') as archive:
                archive.writestr(name, payload)
            self.body = output.getvalue()
            self.write_config(format='zip')
            generation = self.refresh()
            self.assertEqual(self.body, self.store.working(generation).read_bytes())
            self.assertEqual('.portfolio', self.store.working(generation).suffix)

    def test_malformed_or_unsafe_zip_rejected(self):
        for name, payload in [('../escape.xml', XML), ('data.xml', b'<html/>'),
                              ('/absolute.xml', XML), ('data.portfolio', b'<html/>'),
                              ('data.portfolio', b'\x08\x46\x12\x00')]:
            output = io.BytesIO()
            with zipfile.ZipFile(output, 'w') as archive:
                archive.writestr(name, payload)
            self.body = output.getvalue()
            self.write_config(format='zip')
            with self.assertRaises(DevError):
                self.refresh()
        self.body = b'PK\x03\x04truncated'
        with self.assertRaises(DevError):
            self.refresh()

    def test_encrypted_container_preserved_without_content_claim(self):
        self.write_config(format='encrypted')
        self.body = b'PORTFOLIO\x01' + b'i' * 16 + b'e' * 32
        generation = self.refresh()
        self.assertEqual(self.body, self.store.working(generation).read_bytes())
        info = json.loads((generation / 'manifest.json').read_text())
        self.assertIn('container only', info['validation'])
        self.body = b'PORTFOLIO\x01short'
        with self.assertRaises(DevError):
            self.refresh()
        self.assertEqual(generation, self.store.current())

    def test_atomic_activation_failure_preserves_previous(self):
        first = self.refresh()
        replace = os.replace

        def fail_activation(src, dst):
            if Path(dst).name == 'active.json':
                raise OSError('synthetic interruption')
            return replace(src, dst)

        with patch('pp_dev_data.os.replace', side_effect=fail_activation):
            with self.assertRaises(OSError):
                self.refresh()
        self.assertEqual(first, self.store.current())
        self.assertEqual(XML, self.store.working(first).read_bytes())

    def test_symlink_hardlink_and_escaping_active_rejected(self):
        first = self.refresh()
        link = self.storage / 'unsafe'
        link.symlink_to(self.config)
        with self.assertRaises(DevError):
            data.Generations(self.storage)
        link.unlink()
        os.link(self.config, link)
        with self.assertRaises(DevError):
            data.Generations(self.storage)
        link.unlink()
        (self.storage / 'active.json').write_text('{"current":"../../escape"}')
        with self.assertRaises(DevError):
            self.store.current()
        self.assertTrue(first.exists())

    def test_cleanup_removes_only_managed_storage(self):
        self.refresh()
        unrelated = self.root / 'unrelated'
        unrelated.write_text('keep')
        self.store.cleanup()
        self.assertTrue(self.storage.is_dir())
        self.assertEqual([], list(self.storage.iterdir()))
        self.assertTrue(self.config.exists())
        self.assertTrue(unrelated.exists())


class StartupModelTest(unittest.TestCase):
    def test_exact_managed_local_path_is_escaped_and_selected(self):
        with tempfile.TemporaryDirectory() as temporary:
            pp = Path(temporary)
            source = pp / 'name.abuchen.portfolio.bootstrap/Application.e4xmi'
            source.parent.mkdir()
            source.write_text('<application xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
                              'xmlns:xmi="http://www.omg.org/XMI" xmlns:basic="basic">'
                              '<children xsi:type="basic:PartStack" '
                              'elementId="name.abuchen.portfolio.ui.partstack.main">'
                              '</children></application>')
            destination = pp / 'private.e4xmi'
            local = Path('/private/managed/data & space/Development-Copy.xml')
            data.prepare_model(pp, destination, local)
            import xml.etree.ElementTree as ET
            root = ET.parse(destination).getroot()
            stack = root.find('children')
            self.assertEqual('_ManagedDevelopmentPortfolio', stack.get('selectedElement'))
            self.assertEqual(str(local), stack.find('children/persistedState').get('value'))
            self.assertNotIn('WebDAV', destination.read_text())
            self.assertNotIn('Development-Copy', source.read_text())
