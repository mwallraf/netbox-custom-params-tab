from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import lifecycle_sandbox as lifecycle


class LifecycleGuards(unittest.TestCase):
    def test_foreign_labels_rejected(self):
        with self.assertRaises(ValueError):
            lifecycle.validate_volume('netbox-custom-field-profiles_postgres', {'com.docker.compose.project': 'other'})

    def test_foreign_name_rejected(self):
        with self.assertRaises(ValueError):
            lifecycle.validate_volume('other_postgres', {'com.docker.compose.project': lifecycle.sandbox.PROJECT})

    def test_external_config_stops_reset_before_mutation(self):
        with patch.object(lifecycle.sandbox, 'validate_compose', side_effect=ValueError('external')), patch.object(lifecycle.sandbox, 'run') as run:
            with self.assertRaises(ValueError):
                lifecycle.reset()
            run.assert_not_called()

    def test_owned_volume_accepted(self):
        lifecycle.validate_volume(lifecycle.sandbox.PROJECT + '_postgres', {'com.docker.compose.project': lifecycle.sandbox.PROJECT})

    def test_env_path_override_and_external_network_rejected(self):
        import json
        with self.assertRaises(ValueError):
            lifecycle.sandbox.compose_argv(['up', '--env-file=/tmp/other'])
        with patch.object(lifecycle.sandbox, 'run', return_value=json.dumps({'name': lifecycle.sandbox.PROJECT, 'networks': {'default': {'external': True}}, 'services': {}})):
            with self.assertRaises(ValueError):
                lifecycle.sandbox.validate_compose()

    def test_build_context_excludes_local_secrets(self):
        excluded = (lifecycle.sandbox.ROOT / '.dockerignore').read_text().splitlines()
        for name in ('.env', '.recovery', '.sandbox', '.planning'):
            self.assertIn(name, excluded)
