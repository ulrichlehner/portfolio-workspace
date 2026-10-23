"""Build provenance tests use synthetic repositories and fake Mach-O files."""
import contextlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest
from types import SimpleNamespace

import pp_dev as dev


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pp = self.root / 'pp'
        self.pp.mkdir()
        self.git('init', '-q')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'user.name', 'Synthetic Test')
        (self.pp / '.gitignore').write_text('**/target/\n')
        (self.pp / 'source').write_text('first')
        self.git('add', '.')
        self.git('commit', '-qm', 'test: initial synthetic source')
        self.manifest = self.root / 'build/manifest.json'
        self.app = dev.app_path(self.pp, 'aarch64')
        self.binary('Contents/MacOS/PortfolioPerformance')
        self.binary('Contents/Eclipse/plugins/runtime/jre/bin/java')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.pp), *args], stderr=subprocess.DEVNULL)

    def binary(self, name, cpu=0x100000C):
        path = self.app / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'\xcf\xfa\xed\xfe' + struct.pack('<I', cpu))
        path.chmod(0o755)
        return path

    def run_build(self, action, arch='aarch64'):
        with contextlib.redirect_stdout(io.StringIO()):
            dev.build_command(SimpleNamespace(action=action, pp=self.pp,
                                             manifest=self.manifest, arch=arch))

    def build(self):
        self.run_build('before')
        self.run_build('after')
        self.run_build('check')

    def test_clean_build_and_persistent_manifest(self):
        self.build()
        manifest = json.loads(self.manifest.read_text())
        self.assertFalse(manifest['source']['dirty'])
        self.assertNotIn('target', str(self.manifest))
        self.assertEqual(0o600, self.manifest.stat().st_mode & 0o777)

    def test_dirty_content_changes_without_status_change(self):
        source = self.pp / 'source'
        source.write_text('second')
        self.build()
        self.assertTrue(json.loads(self.manifest.read_text())['source']['dirty'])
        source.write_text('third')
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_untracked_sources_invalidate_build(self):
        self.build()
        (self.pp / 'new-source').write_text('new')
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_changed_revision_invalidates_build(self):
        self.build()
        self.git('commit', '--allow-empty', '-qm', 'test: next revision')
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_changed_sources_during_build_rejected(self):
        self.run_build('before')
        (self.pp / 'source').write_text('changed')
        with self.assertRaises(dev.DevError):
            self.run_build('after')
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_missing_manifest_or_app_rejected(self):
        with self.assertRaises(dev.DevError):
            self.run_build('check')
        self.build()
        (self.app / 'Contents/MacOS/PortfolioPerformance').unlink()
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_missing_runtime_rejected(self):
        (self.app / 'Contents/Eclipse/plugins/runtime/jre/bin/java').unlink()
        self.run_build('before')
        with self.assertRaises(dev.DevError):
            self.run_build('after')

    def test_runtime_architecture_mismatch_rejected(self):
        self.binary('Contents/Eclipse/plugins/runtime/jre/bin/java', 0x1000007)
        self.run_build('before')
        with self.assertRaises(dev.DevError):
            self.run_build('after')

    def test_manifest_architecture_mismatch_rejected(self):
        self.build()
        with self.assertRaises(dev.DevError):
            self.run_build('check', 'x86_64')

    def test_modified_packaged_app_rejected(self):
        self.build()
        (self.app / 'Contents/extra').write_text('changed artifact')
        with self.assertRaises(dev.DevError):
            self.run_build('check')

    def test_failed_rebuild_invalidates_old_build(self):
        self.build()
        self.run_build('before')
        with self.assertRaises(dev.DevError):
            self.run_build('check')
