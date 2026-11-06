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

    def test_metadata_and_compose_use_same_docker_environment(self):
        import subprocess
        from unittest.mock import Mock
        with patch.dict('os.environ', {'DOCKER_HOST': 'tcp://other:2375', 'DOCKER_CONTEXT': 'other'}), patch.object(lifecycle.sandbox, 'ensure_env', return_value={}):
            environment = lifecycle.sandbox.docker_environment()
            self.assertNotIn('DOCKER_HOST', environment)
            self.assertNotIn('DOCKER_CONTEXT', environment)
            with patch.object(lifecycle.subprocess, 'run', return_value=Mock(returncode=0, stdout='[]')) as run:
                lifecycle.docker_json(['ps', '-aq'])
                metadata_env = run.call_args.kwargs['env']
                lifecycle.sandbox.run(['ps'], capture=True)
                self.assertEqual(metadata_env, run.call_args.kwargs['env'])

    def test_foreign_database_bind_rejected(self):
        with self.assertRaises(ValueError):
            lifecycle.sandbox.validate_mounts('postgres', [{'type': 'bind', 'source': '/other/database', 'target': '/var/lib/postgresql'}])

    def test_symlinked_source_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docker').mkdir()
            (root / 'docker/plugins.py').symlink_to('/tmp/foreign-plugin.py')
            with patch.object(lifecycle.sandbox, 'ROOT', root):
                with self.assertRaises(ValueError):
                    lifecycle.sandbox.validate_mounts('netbox', [])

    def test_missing_sentinel_is_not_recreated(self):
        with patch.object(lifecycle.sandbox, 'django', side_effect=RuntimeError('missing')) as django:
            with self.assertRaises(RuntimeError):
                lifecycle.sentinel()
            code = django.call_args.args[0][-1]
            self.assertIn('Site.objects.get(', code)
            self.assertNotIn('create(', code)
            self.assertIn('seed_snapshot()', code)

    def test_new_unrelated_container_does_not_invalidate_existing_ids(self):
        lifecycle.assert_original_containers({'original'}, {'original', 'new'})
        with self.assertRaises(RuntimeError):
            lifecycle.assert_original_containers({'original'}, {'replacement'})

    def test_unrelated_inspection_selects_only_id_and_project_label(self):
        with patch.object(lifecycle, 'docker_json', side_effect=['one\n', '"one"|other\n']) as inspect:
            self.assertEqual(lifecycle.unrelated_ids(), {'one'})
            argv = inspect.call_args.args[0]
            self.assertIn('--format', argv)
            self.assertNotIn('.Config.Env', argv[argv.index('--format') + 1])
