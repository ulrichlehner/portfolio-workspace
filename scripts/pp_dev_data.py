"""Read-only HTTPS retrieval and atomic private portfolio generations (container only)."""
import base64
import hashlib
import http.client
import io
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import ssl
import stat
import tempfile
import time
from urllib.parse import quote, urlsplit
import uuid
import xml.etree.ElementTree as ET
import zipfile

from pp_dev import DevError, atomic_json, now

MAX_BYTES = 512 * 1024 * 1024
DEADLINE = 120
GENERATION = re.compile(r'[0-9a-f]{32}')
# PP treats a .zip filename as compressed XML. .portfolio selects content-based
# detection for both binary and XML ZIP containers, without changing their bytes.
FORMATS = {'xml': 'xml', 'zip': 'portfolio', 'encrypted': 'portfolio'}


def safe_tree(root):
    """Reject links, special files and multiply linked files before touching managed data."""
    for path in [root, *root.rglob('*')]:
        mode = path.lstat()
        if stat.S_ISLNK(mode.st_mode) or not (stat.S_ISDIR(mode.st_mode) or stat.S_ISREG(mode.st_mode)):
            raise DevError('Unsafe link or special file in managed storage.')
        if stat.S_ISREG(mode.st_mode) and mode.st_nlink != 1:
            raise DevError('Hard links are not allowed in managed storage.')


def private_config(path):
    meta = path.lstat()
    if not stat.S_ISREG(meta.st_mode) or meta.st_nlink != 1 or meta.st_mode & 0o077:
        raise DevError('Private configuration must be a regular file with mode 600.')
    try:
        config = json.loads(path.read_text())
        url = urlsplit(config['url'])
        if (url.scheme != 'https' or not url.hostname or url.username or url.password
                or url.fragment or any(ord(c) < 32 or ord(c) == 127 for c in config['url'])):
            raise ValueError()
        url.port  # Validate the port without emitting its value.
        if config.get('read_only_confirmed') is not True:
            raise DevError('Server-side read-only access must be confirmed before use.')
        if config['format'] not in FORMATS:
            raise ValueError()
        auth = config['auth']
        if auth['method'] == 'basic':
            if ':' in auth['username']:
                raise ValueError()
            token = base64.b64encode((auth['username'] + ':' + auth['password']).encode()).decode()
            authorization = 'Basic ' + token
        elif auth['method'] == 'bearer' and auth['token']:
            authorization = 'Bearer ' + auth['token']
        else:
            raise ValueError()
        if '\r' in authorization or '\n' in authorization:
            raise ValueError()
        return config, url, authorization
    except DevError:
        raise
    except Exception:
        raise DevError('Private WebDAV configuration is missing or invalid.') from None


def download(config_path, destination):
    """Always fetch in full: no conditional request can accidentally reuse local edits."""
    config, url, authorization = private_config(config_path)
    connection = http.client.HTTPSConnection(url.hostname, url.port or 443,
                                           timeout=15, context=ssl.create_default_context())
    started = time.monotonic()
    if DEADLINE <= 0:
        raise DevError('WebDAV download deadline exceeded.')

    def timed_out(signum, frame):
        raise DevError('WebDAV download deadline exceeded.')

    old_handler = signal.signal(signal.SIGALRM, timed_out)
    old_timer = signal.setitimer(signal.ITIMER_REAL, DEADLINE)
    try:
        target = quote(url.path or '/', safe="/%:@!$&'()*+,;=-._~")
        if url.query:
            target += '?' + quote(url.query, safe="/%?:@!$&'()*+,;=-._~")
        # http.client does not follow redirects, negotiate alternate methods, or retry.
        connection.request('GET', target, headers={'Authorization': authorization,
                           'Accept-Encoding': 'identity', 'Connection': 'close'})
        response = connection.getresponse()
        if response.status != 200:
            raise DevError('WebDAV retrieval rejected (authentication, redirect or server status).')
        if response.getheader('Content-Encoding', 'identity') != 'identity':
            raise DevError('Encoded WebDAV response is unsupported.')
        length = response.getheader('Content-Length')
        expected = int(length) if length is not None else None
        if expected is not None and not 0 < expected <= MAX_BYTES:
            raise DevError('WebDAV response has an invalid size.')
        total = 0
        with destination.open('xb') as stream:
            os.chmod(destination, 0o600)
            while True:
                if time.monotonic() - started > DEADLINE:
                    raise DevError('WebDAV download deadline exceeded.')
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_BYTES:
                    raise DevError('WebDAV response exceeds the size limit.')
                stream.write(chunk)
            stream.flush()
            os.fsync(stream.fileno())
        if not total or (expected is not None and total != expected):
            raise DevError('WebDAV download was incomplete.')
        return {'checked_at': now(), 'downloaded_at': now(), 'format': config['format'],
                'etag': response.getheader('ETag'), 'last_modified': response.getheader('Last-Modified')}
    except DevError:
        raise
    except ssl.SSLCertVerificationError:
        raise DevError('WebDAV certificate/hostname verification failed; check the server certificate chain.') from None
    except ssl.SSLError:
        raise DevError('WebDAV TLS negotiation failed; check the server HTTPS configuration.') from None
    except socket.gaierror:
        raise DevError('WebDAV hostname could not be resolved from Docker; check DNS/network access.') from None
    except TimeoutError:
        raise DevError('WebDAV connection or transfer timed out; check Docker network access.') from None
    except ConnectionError:
        raise DevError('WebDAV connection failed; check Docker reachability and the HTTPS port.') from None
    except http.client.InvalidURL:
        raise DevError('WebDAV URL is invalid; check the private file URL.') from None
    except Exception:
        raise DevError('WebDAV TLS or transfer failed; previous data remains available.') from None
    finally:
        connection.close()
        signal.setitimer(signal.ITIMER_REAL, *old_timer)
        signal.signal(signal.SIGALRM, old_handler)


def validate_xml(payload):
    try:
        text = payload.decode('utf-8-sig')
    except UnicodeError:
        raise DevError('PP XML must use UTF-8 encoding.') from None
    if '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        raise DevError('XML declarations with entities are unsupported.')
    try:
        root = ET.fromstring(payload)
    except ET.ParseError:
        raise DevError('Downloaded XML is malformed.') from None
    if root.tag != 'client' or not root.findtext('version', '').isdigit():
        raise DevError('Downloaded XML is not a PP portfolio.')


def validate_container(path, expected):
    payload = path.read_bytes()
    if expected == 'xml':
        validate_xml(payload)
    elif expected == 'encrypted':
        # PP: nine-byte signature, method, 16-byte IV, AES ciphertext blocks.
        if (not payload.startswith(b'PORTFOLIO') or len(payload) < 58
                or payload[9] not in (0, 1) or (len(payload) - 26) % 16):
            raise DevError('Encrypted portfolio container is malformed.')
        return 'encrypted container only; PP must validate the password and content'
    elif expected == 'zip':
        try:
            with zipfile.ZipFile(io.BytesIO(payload)) as archive:
                entries = archive.infolist()
                if not entries or sum(e.file_size for e in entries) > MAX_BYTES:
                    raise DevError('ZIP portfolio has an invalid expanded size.')
                for entry in entries:
                    if (entry.is_dir() or '/' in entry.filename or '\\' in entry.filename
                            or entry.filename in ('.', '..') or entry.flag_bits & 1
                            or stat.S_ISLNK(entry.external_attr >> 16)):
                        raise DevError('Unsafe ZIP portfolio entry.')
                if archive.testzip() is not None:
                    raise DevError('ZIP portfolio is damaged.')
                first = archive.read(entries[0])
                if entries[0].filename.endswith('.portfolio'):
                    # The signature proves the envelope, not protobuf semantics.
                    if not first.startswith(b'PPPBV1') or len(first) <= 6:
                        raise DevError('ZIP protobuf payload is invalid.')
                    return 'ZIP integrity only; PP must validate protobuf content'
                validate_xml(first)
        except (zipfile.BadZipFile, RuntimeError, OSError):
            raise DevError('Downloaded ZIP is malformed.') from None
    else:
        raise DevError('Unsupported configured portfolio format.')
    return 'container and XML structure checked; PP validates portfolio semantics'


def file_digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Generations:
    def __init__(self, root):
        self.root = root
        if root.is_symlink():
            raise DevError('Managed storage must not be a link.')
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        safe_tree(root)
        os.chmod(root, 0o700)
        self.generations = root / 'generations'
        self.generations.mkdir(mode=0o700, exist_ok=True)

    def current(self):
        state = self.root / 'active.json'
        if not state.exists():
            return None
        value = json.loads(state.read_text())
        name = value.get('current', '')
        if not GENERATION.fullmatch(name):
            raise DevError('Invalid active generation.')
        path = self.generations / name
        if not path.is_dir():
            raise DevError('Active generation is missing.')
        return path

    def working(self, generation):
        manifest = json.loads((generation / 'manifest.json').read_text())
        extension = FORMATS.get(manifest.get('format'))
        if extension is None:
            raise DevError('Invalid generation format.')
        path = generation / ('Development-Copy.' + extension)
        if not path.is_file():
            raise DevError('Local development portfolio is missing.')
        return path

    def refresh(self, config, build):
        previous = self.current()
        temporary = Path(tempfile.mkdtemp(prefix='.staging-', dir=self.root))
        try:
            baseline = temporary / 'baseline'
            info = download(config, baseline)
            info['validation'] = validate_container(baseline, info['format'])
            info['sha256'] = file_digest(baseline)
            info['build'] = build
            # Keep the baseline immutable to accidental writes; use a separate inode.
            baseline.chmod(0o400)
            working = temporary / ('Development-Copy.' + FORMATS[info['format']])
            shutil.copyfile(baseline, working)
            working.chmod(0o600)
            atomic_json(temporary / 'manifest.json', info)
            generation = self.generations / uuid.uuid4().hex
            os.replace(temporary, generation)
            state = {'current': generation.name, 'previous': previous.name if previous else None}
            # One atomic pointer changes both baseline and working-copy selection.
            atomic_json(self.root / 'active.json', state)
            # Pruning happens strictly after successful activation.
            for old in self.generations.iterdir():
                if (GENERATION.fullmatch(old.name) and old.name not in state.values()
                        and not (old / 'keep').exists()):
                    shutil.rmtree(old)
            return generation
        finally:
            if temporary.exists():
                shutil.rmtree(temporary)

    def report(self, generation, offline=False):
        info = json.loads((generation / 'manifest.json').read_text())
        print('STALE DATA: explicit offline launch.' if offline else 'Remote copy refreshed.')
        print('Source checked: ' + info['checked_at'] + '; downloaded: ' + info['downloaded_at'])
        print('Validation: ' + info['validation'])

    def cleanup(self):
        safe_tree(self.root)
        # /data is a Docker bind mount: clear it without unlinking the mount
        # point. The host wrapper removes the empty managed directory afterward.
        for child in self.root.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()


def prepare_model(pp, destination, local_path):
    """Seed the existing PP part via Eclipse's applicationXMI startup option."""
    from html import escape
    model = (pp / 'name.abuchen.portfolio.bootstrap/Application.e4xmi').read_text(encoding='ascii')
    marker = r'(<children xsi:type="basic:PartStack"[^>]*elementId="name.abuchen.portfolio.ui.partstack.main")([^>]*>)'
    part = ('\n<children xsi:type="basic:Part" xmi:id="_ManagedDevelopmentPortfolio" '
            'elementId="name.abuchen.portfolio.ui.part.portfolio" '
            'label="Development Copy" closeable="true" '
            'bindingContexts="_KwZhsBoEEeiQOJdQgYCbNA" '
            'contributionURI="bundleclass://name.abuchen.portfolio.ui/name.abuchen.portfolio.ui.editor.PortfolioPart">'
            '<tags>NoDetach</tags><tags>Editor</tags><tags>removeOnHide</tags>'
            '<persistedState key="file" value="' + escape(str(local_path), quote=True) + '"/></children>')
    model, count = re.subn(marker, lambda match: match[1]
                          + ' selectedElement="_ManagedDevelopmentPortfolio"' + match[2] + part, model)
    if count != 1:
        raise DevError('PP startup model changed; managed launch needs review.')
    # Encoding changes only in this private generated copy, never the PP source.
    model = model.replace('encoding="ASCII"', 'encoding="UTF-8"', 1)
    destination.write_text(model, encoding='utf-8')
    destination.chmod(0o600)


def main():
    import argparse
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['refresh', 'offline', 'keep', 'recover', 'cleanup'])
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--config', type=Path, default=Path('/secret/config.json'))
    parser.add_argument('--build', type=Path, default=Path('/build/manifest.json'))
    parser.add_argument('--pp', type=Path, default=Path('/src'))
    parser.add_argument('--host-data', type=Path)
    args = parser.parse_args()
    try:
        os.umask(0o077)
        store = Generations(args.data)
        if args.action == 'cleanup':
            store.cleanup()
            print('Managed private test data removed; credentials remain in private configuration.')
            return 0
        current = store.current()
        if args.action == 'keep':
            if current is None:
                raise DevError('No local generation to keep.')
            (current / 'keep').touch(mode=0o600)
            print('Current generation retained until explicit private-data cleanup.')
            return 0
        if args.action == 'recover':
            state = json.loads((args.data / 'active.json').read_text())
            previous = state.get('previous', '')
            if not isinstance(previous, str) or not GENERATION.fullmatch(previous):
                raise DevError('No previous generation to recover.')
            recovered = store.generations / previous
            store.working(recovered)
            atomic_json(args.data / 'active.json', {'current': previous, 'previous': current.name})
            print('Previous local generation activated; use explicit offline launch.')
            return 0
        if args.action == 'refresh':
            current = store.refresh(args.config, json.loads(args.build.read_text())['source'])
        elif current is None:
            raise DevError('No retained portfolio for offline launch.')
        info = json.loads((current / 'manifest.json').read_text())
        if file_digest(current / 'baseline') != info['sha256']:
            raise DevError('Retained baseline changed; refusing managed launch.')
        working = store.working(current)
        host_path = args.host_data / working.relative_to(args.data)
        prepare_model(args.pp, args.data / 'startup.e4xmi', host_path)
        # Eclipse accepts a platform plug-in URI here, not an arbitrary file URI.
        # A resource-only local bundle exposes the model without patching PP jars.
        bundle = args.data / 'startup-model.jar'
        with zipfile.ZipFile(bundle, 'w') as archive:
            archive.writestr('META-INF/MANIFEST.MF',
                             'Manifest-Version: 1.0\r\nBundle-ManifestVersion: 2\r\n'
                             'Bundle-SymbolicName: workspace.testing.model\r\n'
                             'Bundle-Version: 1.0.0\r\n\r\n')
            archive.write(args.data / 'startup.e4xmi', 'Startup.e4xmi')
            for resource in (args.pp / 'name.abuchen.portfolio.bootstrap/OSGI-INF/l10n').glob('*.properties'):
                archive.write(resource, 'OSGI-INF/l10n/' + resource.name)
        (args.data / 'startup-uri').write_text('platform:/plugin/workspace.testing.model/Startup.e4xmi')
        (args.data / 'startup-bundle').write_text(
            'workspace.testing.model,1.0.0,' + (args.host_data / 'startup-model.jar').as_uri() + ',4,false\n')
        store.report(current, offline=args.action == 'offline')
        return 0
    except DevError as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        return 1
    except Exception:
        print('ERROR: Private portfolio setup or retrieval failed; active data was not replaced by an invalid download.',
              file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
