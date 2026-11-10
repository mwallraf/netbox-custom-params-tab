"""Build and test an installed wheel using a fresh, disposable native test DB."""
import sys
import time
import json

import sandbox
from test_profiles import snapshot


CHECK = r'''
import json, os, pathlib, shutil, subprocess, sys, tempfile, uuid, zipfile
source = pathlib.Path('/opt/netbox-custom-field-profiles')
python = '/opt/netbox/venv/bin/python'
manage = '/opt/netbox/netbox/manage.py'
with tempfile.TemporaryDirectory(prefix='cfprofiles-release-') as temporary:
    root = pathlib.Path(temporary)
    clean = root / 'source'
    clean.mkdir()
    # The image's baked metadata can predate the bind-mounted source checkout.
    (clean / 'pyproject.toml').write_text(json.load(sys.stdin)['pyproject'])
    shutil.copytree(source / 'netbox_custom_field_profiles', clean / 'netbox_custom_field_profiles',
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '*.egg-info'))
    subprocess.run(['uv', 'build', '--out-dir', str(root / 'dist'), str(clean)], check=True)
    wheels = list((root / 'dist').glob('*.whl'))
    assert len(wheels) == 1, 'Expected one release wheel'
    with zipfile.ZipFile(wheels[0]) as archive:
        names = set(archive.namelist())
        expected = ['templates/netbox_custom_field_profiles/device_parameters.html',
                    'templates/netbox_custom_field_profiles/device_parameters_edit.html',
                    'static/netbox_custom_field_profiles/profile_fields.js',
                    'migrations/0001_initial.py', 'migrations/0002_profiles.py',
                    'migrations/0003_retire_legacy_configuration.py']
        assert all('netbox_custom_field_profiles/' + name in names for name in expected), 'Missing package assets'
        assert not any(name.startswith('netbox_custom_params_tab/') for name in names), 'Retired package included'
    print('RELEASE_WHEEL_ASSETS_OK', flush=True)
    target = root / 'installed'
    subprocess.run(['uv', 'pip', 'install', '--offline', '--no-deps', '--python', python,
                    '--target', str(target), str(wheels[0])], check=True)
    environment = dict(os.environ, PYTHONPATH=str(target))
    # Startup loads the installed wheel, not the mounted editable checkout.
    provenance = ('import pathlib, netbox_custom_field_profiles as plugin; '
                  f'assert pathlib.Path(plugin.__file__).is_relative_to({str(target)!r}); '
                  'print("RELEASE_INSTALLED_IMPORT_OK")')
    subprocess.run([python, manage, 'shell', '-c', provenance], env=environment, check=True)
    subprocess.run([python, manage, 'check'], env=environment, check=True)
    subprocess.run([python, manage, 'makemigrations', 'netbox_custom_field_profiles',
                    '--check', '--dry-run'], env=environment, check=True)
    database = 'test_cfprofiles_release_' + uuid.uuid4().hex
    assert database.startswith('test_cfprofiles_release_')
    run_tests = (f'from django.conf import settings; '
                 f'settings.DATABASES["default"].setdefault("TEST", {{}})["NAME"] = {database!r}; '
                 'from django.core.management import call_command; '
                 'call_command("test", "netbox_custom_field_profiles.tests", interactive=False, '
                 'keepdb=False, testrunner="netbox_custom_field_profiles.tests.runner.ProfileTestRunner")')
    subprocess.run([python, manage, 'shell', '-c', run_tests], env=environment, check=True)
    print('RELEASE_CLEAN_INSTALL_MIGRATIONS_TESTS_OK', flush=True)
'''


def main():
    started = time.monotonic()
    try:
        sandbox.validate_compose()
        before = snapshot()
        try:
            output = sandbox.run(['exec', '-T', 'netbox', sandbox.PYTHON, '-c', CHECK], capture=True,
                                 input=json.dumps({'pyproject': (sandbox.ROOT / 'pyproject.toml').read_text()}))
            print(sandbox.redact(output), end='')
            for marker in ('RELEASE_WHEEL_ASSETS_OK', 'RELEASE_INSTALLED_IMPORT_OK',
                           'PROFILE_TESTS_ISOLATED', 'RELEASE_CLEAN_INSTALL_MIGRATIONS_TESTS_OK'):
                if marker not in output:
                    raise RuntimeError('Missing release verification marker: ' + marker)
        finally:
            if snapshot() != before:
                raise RuntimeError('RELEASE_LIVE_CHANGED: live native/plugin state differs')
            print('RELEASE_LIVE_UNCHANGED')
        print(f'RELEASE_CHECK_OK elapsed={time.monotonic() - started:.2f}s')
        return 0
    except (RuntimeError, OSError) as error:
        print('RELEASE_CHECK_ERROR: ' + sandbox.redact(str(error)), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
