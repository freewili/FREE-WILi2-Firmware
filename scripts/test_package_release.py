import copy
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile
from package_release import package, validate


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.folder = self.root / 'v07'
        shutil.copytree(Path(__file__).resolve().parents[1] / 'releases/v07', self.folder)

    def change(self, fn):
        path = self.folder / 'manifest.json'
        manifest = json.loads(path.read_text())
        fn(manifest)
        path.write_text(json.dumps(manifest))

    def test_reproducible_complete_package(self):
        a = package(self.folder, self.root / 'a').read_bytes()
        b = package(self.folder, self.root / 'b').read_bytes()
        self.assertEqual(a, b)
        self.assertEqual(len(validate(self.folder)[1]), 6)
        with zipfile.ZipFile(self.root / 'a/FREE-WILi2-v07.zip') as archive:
            self.assertTrue(all(info.create_system == 3 for info in archive.infolist()))

    def test_corrupt_firmware(self):
        path = self.folder / 'firmware/FW2Main-v07.uf2'
        data = bytearray(path.read_bytes()); data[100] ^= 1; path.write_bytes(data)
        with self.assertRaisesRegex(ValueError, 'Checksum'):
            validate(self.folder)

    def test_wrong_embedded_version(self):
        self.change(lambda m: m['files'][0].update(version='v08'))
        with self.assertRaisesRegex(ValueError, 'version mismatch'):
            validate(self.folder)

    def test_missing_component(self):
        self.change(lambda m: m['files'].pop())
        with self.assertRaisesRegex(ValueError, 'Release needs'):
            validate(self.folder)

    def test_duplicate_component(self):
        self.change(lambda m: m['files'].append(copy.deepcopy(m['files'][0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            validate(self.folder)

    def test_unsafe_path(self):
        self.change(lambda m: m['files'][0].update(file='../outside.uf2'))
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            validate(self.folder)

    def test_unlisted_file(self):
        (self.folder / 'extra.txt').write_text('unexpected')
        with self.assertRaisesRegex(ValueError, 'Unlisted'):
            validate(self.folder)

    def test_mismatched_bottlenose_metadata_version(self):
        self.change(lambda m: m['files'][3].update(version='different-build'))
        with self.assertRaisesRegex(ValueError, 'versions disagree'):
            validate(self.folder)


if __name__ == '__main__':
    unittest.main()
