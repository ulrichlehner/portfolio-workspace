"""Exercise shell safety and kernel locking inside the development container."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
import unittest


class WrapperTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'scripts').mkdir()
        source = Path('/tools/dev.sh').read_text()
        self.script = self.root / 'scripts/dev.sh'
        self.script.write_text(source)
        self.script.chmod(0o755)
        self.library = self.root / 'scripts/functions.sh'
        self.library.write_text(source.split('case "${1:-}" in')[0])
        self.scratch = self.root / 'scratch'
        (self.root / 'portfolio/portfolio-app').mkdir(parents=True)

    def test_ordinary_clean_preserves_generations_and_unrelated_files(self):
        generation = self.scratch / 'pp-dev-data/generations/example/Development-Copy.xml'
        generation.parent.mkdir(parents=True)
        generation.write_text('synthetic')
        target = self.root / 'portfolio/bundle/target'
        target.mkdir(parents=True)
        workspace = self.scratch / 'pp-dev-workspace'
        workspace.mkdir()
        unrelated = self.scratch / 'unrelated'
        unrelated.write_text('keep')
        subprocess.run([str(self.script), 'clean'], check=True)
        self.assertTrue(generation.exists())
        self.assertTrue(unrelated.exists())
        self.assertFalse(target.exists())
        self.assertFalse(workspace.exists())

    def test_linked_scratch_rejected_before_cleanup(self):
        outside = self.root / 'outside'
        outside.mkdir()
        self.scratch.symlink_to(outside)
        result = subprocess.run([str(self.script), 'clean'], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertTrue(outside.exists())

    def test_concurrent_operation_rejected_and_lock_recovers_on_exit(self):
        command = ['bash', '-c', 'source "$1"; SCRATCH="$2"; acquire_lock; '
                   'touch "$2/ready"; exec sleep 30', 'test', str(self.library), str(self.scratch)]
        process = subprocess.Popen(command)
        self.addCleanup(lambda: process.poll() is None and process.kill())
        for _ in range(100):
            if (self.scratch / 'ready').exists():
                break
            time.sleep(0.01)
        self.assertTrue((self.scratch / 'ready').exists())
        result = subprocess.run([str(self.script), 'clean'], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn(b'already running', result.stderr)
        process.terminate()
        process.wait(timeout=5)
        subprocess.run([str(self.script), 'clean'], check=True)
        self.assertTrue((self.scratch / 'pp-dev.lock').exists())

    def test_lock_hardlink_rejected(self):
        self.scratch.mkdir()
        other = self.root / 'other'
        other.write_text('do not touch')
        os.link(other, self.scratch / 'pp-dev.lock')
        result = subprocess.run([str(self.script), 'clean'], capture_output=True)
        self.assertNotEqual(0, result.returncode)
        self.assertEqual('do not touch', other.read_text())
