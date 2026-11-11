"""Release gates reject mismatched versions and code outside main's history."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[2] / 'scripts/ci_prepare_release.py'


class ReleaseSourceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'scripts').mkdir()
        (self.root / 'automation/scripts').mkdir(parents=True)
        (self.root / 'automation/scripts/release_check.py').write_text('# current release tool\n')
        (self.source / 'netbox_custom_field_profiles').mkdir()
        (self.source / 'netbox_custom_field_profiles/__init__.py').write_text(
            'class Config:\n    version = "0.1.0"\n')
        (self.source / 'pyproject.toml').write_text(
            '[project]\nname = "netbox-custom-field-profiles"\nversion = "0.1.0"\n')
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'user.name=Release Test', '-c', 'user.email=release@example.test',
                 'commit', '-qm', 'release fixture')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.source, check=True,
                              capture_output=True, text=True)

    def run_gate(self, tag='v0.1.0'):
        return subprocess.run([sys.executable, str(SCRIPT)], cwd=self.root,
                              env=dict(os.environ, RELEASE_TAG=tag), capture_output=True, text=True)

    def test_matching_main_ancestor_accepts_and_copies_only_tool(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.source / 'scripts/release_check.py').read_text(),
                         '# current release tool\n')
        self.assertEqual(self.git('diff', '--', 'netbox_custom_field_profiles').stdout, '')

    def test_different_package_version_is_rejected_before_copy(self):
        result = self.run_gate('v0.2.0')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Tag and distribution version must match', result.stderr)
        self.assertFalse((self.source / 'scripts/release_check.py').exists())

    def test_different_plugin_version_is_rejected(self):
        (self.source / 'netbox_custom_field_profiles/__init__.py').write_text(
            'class Config:\n    version = "0.2.0"\n')
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('PluginConfig version must match', result.stderr)

    def test_unmerged_commit_is_rejected(self):
        (self.source / 'unmerged.txt').write_text('outside main\n')
        self.git('add', '.')
        self.git('-c', 'user.name=Release Test', '-c', 'user.email=release@example.test',
                 'commit', '-qm', 'unmerged code')
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.source / 'scripts/release_check.py').exists())
