import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from pp_oauth_config import ENTRY, expected_sha256, install


class OAuthConfigTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.jar = root / 'core.jar'
        self.data = b'{"clientId": "synthetic-public-client"}\n'
        with zipfile.ZipFile(self.jar, 'w') as archive:
            archive.writestr(ENTRY, self.data)
        self.destination = root / 'private' / 'oauth-config.json'
        self.digest = hashlib.sha256(self.data).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def test_install_verifies_and_writes_outside_source_tree(self):
        self.assertTrue(install(self.jar, self.destination, self.digest))
        self.assertEqual(self.data, self.destination.read_bytes())
        self.assertEqual(0o600, self.destination.stat().st_mode & 0o777)
        # Second run must not rewrite the file.
        self.assertFalse(install(self.jar, self.destination, self.digest))

    def test_checksum_mismatch_is_refused(self):
        with self.assertRaises(ValueError):
            install(self.jar, self.destination, '0' * 64)
        self.assertFalse(self.destination.exists())

    def test_expected_checksum_is_read_from_pom(self):
        pom = Path(self.temp.name) / 'pom.xml'
        pom.write_text('<condition><equals arg1="a" arg2="' + self.digest + '" /></condition>')
        self.assertEqual(self.digest, expected_sha256(pom))

    def test_missing_entry_is_an_error(self):
        other = Path(self.temp.name) / 'empty.jar'
        with zipfile.ZipFile(other, 'w') as archive:
            archive.writestr('other.txt', 'x')
        with self.assertRaises(KeyError):
            install(other, self.destination, self.digest)


if __name__ == '__main__':
    unittest.main()
