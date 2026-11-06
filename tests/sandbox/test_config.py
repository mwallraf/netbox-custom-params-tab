import concurrent.futures
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import sandbox


class EnvironmentTests(unittest.TestCase):
    def test_repeat_preserves_bytes_and_permissions(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / '.env'
            first = sandbox.ensure_env(path)
            before = path.read_bytes()
            self.assertEqual(first, sandbox.ensure_env(path))
            self.assertEqual(before, path.read_bytes())
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertEqual(len(first['SUPERUSER_API_KEY']), 12)
            self.assertEqual(len(first['SUPERUSER_API_TOKEN']), 40)

    def test_partial_config_fails_without_rotation(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / '.env'
            path.write_text('SECRET_KEY=keep\n')
            with self.assertRaises(ValueError):
                sandbox.ensure_env(path)
            self.assertEqual(path.read_text(), 'SECRET_KEY=keep\n')

    def test_config_is_data(self):
        for value in ['KEY=$(touch /tmp/bad)', 'KEY=`id`', 'bad data', 'KEY=a\nKEY=b']:
            with self.assertRaises(ValueError):
                sandbox.parse_env(value)

    def test_atomic_concurrent_initialization(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / '.env'
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
                values = list(pool.map(lambda _: sandbox.ensure_env(path), range(4)))
            self.assertTrue(all(v == values[0] for v in values))

    def test_project_cannot_be_overridden(self):
        with self.assertRaises(ValueError):
            sandbox.validate_env(dict(sandbox.new_env(), COMPOSE_PROJECT_NAME='netbox'))

    def test_explicit_compose_target(self):
        command = sandbox.compose_argv(['up', '-d'])
        self.assertIn(sandbox.PROJECT, command)
        self.assertIn(str(sandbox.ROOT / 'docker-compose.yml'), command)
        self.assertIn(str(sandbox.ROOT / '.env'), command)
        with self.assertRaises(ValueError):
            sandbox.compose_argv(['-p', 'other', 'down'])


if __name__ == '__main__':
    unittest.main()
