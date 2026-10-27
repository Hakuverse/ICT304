from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch
import build_package as build


class PackageTests(unittest.TestCase):
    def test_only_declared_architectures(self):
        self.assertEqual(build.platform_tag('Windows', 'AMD64'), 'windows-x64')
        self.assertEqual(build.platform_tag('Darwin', 'arm64'), 'macos-arm64')
        for args in [('Darwin', 'x86_64'), ('Windows', 'arm64'), ('Linux', 'x86_64')]:
            with self.assertRaises(ValueError):
                build.platform_tag(*args)

    def test_version_cannot_escape_output_folder(self):
        self.assertEqual(build.valid_version('0.1.0-preview'), '0.1.0-preview')
        for value in ('../outside', '/tmp/file', '', 'x y', 'a' * 51):
            with self.assertRaises(ValueError):
                build.valid_version(value)

    def test_dirty_sources_are_rejected(self):
        with patch('build_package.subprocess.check_output', side_effect=['abc\n', ' M file.py\n']):
            with self.assertRaises(RuntimeError):
                build.source_commit()

    def test_archive_keeps_complete_windows_folder(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            folder = root / 'SARAH test'
            (folder / '_internal').mkdir(parents=True)
            (folder / 'SARAH.exe').write_bytes(b'exe')
            (folder / '_internal/model').write_bytes(b'model')
            archive = root / 'package.zip'
            build.archive_package(folder, archive, 'windows-x64')
            with zipfile.ZipFile(archive) as zipped:
                self.assertEqual(set(zipped.namelist()), {'SARAH test/SARAH.exe', 'SARAH test/_internal/model'})

    def test_mac_uses_symlink_preserving_tool(self):
        with patch('build_package.run') as run:
            build.archive_package(Path('/app'), Path('/app.zip'), 'macos-arm64')
            self.assertEqual(run.call_args.args[0][:5], ['/usr/bin/ditto', '-c', '-k', '--sequesterRsrc', '--keepParent'])


if __name__ == '__main__':
    unittest.main()
