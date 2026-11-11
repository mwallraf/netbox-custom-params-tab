"""Build and test an installed wheel using a fresh, disposable native test DB."""
import sys
import time
import json
import argparse
import base64
from pathlib import Path
import re

import sandbox
from test_profiles import snapshot


CHECK = r'''
import base64, json, os, pathlib, re, shutil, subprocess, sys, tempfile, tomllib, uuid, zipfile
source = pathlib.Path('/opt/netbox-custom-field-profiles')
python = '/opt/netbox/venv/bin/python'
manage = '/opt/netbox/netbox/manage.py'
with tempfile.TemporaryDirectory(prefix='cfprofiles-release-') as temporary:
    root = pathlib.Path(temporary)
    clean = root / 'source'
    clean.mkdir()
    # The image's baked metadata can predate the bind-mounted source checkout.
    inputs = json.load(sys.stdin)
    for name in ('pyproject.toml', 'README.md', 'LICENSE'):
        (clean / name).write_text(inputs[name])
    release_tag = inputs.get('release_tag')
    if release_tag:
        version = tomllib.loads(inputs['pyproject.toml'])['project']['version']
        assert release_tag == 'v' + version, 'Release tag/package version mismatch'
        assert re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+(?:[a-zA-Z0-9.-]+)?', release_tag), 'Invalid tag'
        # PyPI cannot resolve GitHub-relative README links. Transform only build input.
        base = 'https://github.com/mwallraf/netbox-custom-params-tab/blob/' + release_tag + '/'
        raw = 'https://raw.githubusercontent.com/mwallraf/netbox-custom-params-tab/' + release_tag + '/'
        def absolute_link(match):
            image, label, target = match.groups()
            if '://' in target or target.startswith(('#', 'mailto:')):
                return match.group(0)
            return image + '[' + label + '](' + (raw if image else base) + target + ')'
        readme = re.sub(r'(!?)\[([^\]]*)\]\(([^)]+)\)', absolute_link, inputs['README.md'])
        (clean / 'README.md').write_text(readme)
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
        retired = ['templates/netbox_custom_field_profiles/customtabconfig_edit.html',
                   'templates/netbox_custom_field_profiles/customtabconfig_delete.html',
                   'templates/netbox_custom_field_profiles/tab_panel.html',
                   'templatetags/customtab_tags.py']
        assert not any('netbox_custom_field_profiles/' + name in names for name in retired), 'Retired UI assets included'
        metadata = next(name for name in names if name.endswith('.dist-info/METADATA'))
        metadata = archive.read(metadata).decode()
        assert 'Maarten Wallraf' in metadata, 'Missing package author'
        assert 'https://github.com/mwallraf/netbox-custom-params-tab' in metadata, 'Missing project URL'
        assert '/blob/HEAD/docs/README.md' in metadata, 'Missing documentation index URL'
        assert '/blob/HEAD/docs/installation.md' in metadata, 'Missing current installation URL'
        assert 'MIT License' in metadata, 'Missing license metadata'
        licenses = [name for name in names if '.dist-info/' in name and name.endswith('/LICENSE')]
        assert licenses and 'Copyright (c) 2026 Maarten Wallraf' in archive.read(licenses[0]).decode(), 'Missing packaged license'
    print('RELEASE_WHEEL_ASSETS_OK', flush=True)
    print('RELEASE_RETIRED_UI_ABSENT', flush=True)
    print('RELEASE_PROJECT_METADATA_LICENSE_OK', flush=True)
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
    if inputs.get('export_dist'):
        print('RELEASE_DISTRIBUTIONS=' + json.dumps({
            file.name: base64.b64encode(file.read_bytes()).decode()
            for file in sorted((root / 'dist').iterdir())
            if file.name.endswith(('.whl', '.tar.gz'))
        }), flush=True)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dist-dir', type=Path, help='Retain the exact tested wheel and source archive')
    parser.add_argument('--release-tag', help='Validate version and make build README links absolute')
    args = parser.parse_args()
    if args.release_tag and not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+(?:[a-zA-Z0-9.-]+)?', args.release_tag):
        parser.error('Invalid release tag')
    distributions = None
    started = time.monotonic()
    try:
        sandbox.validate_compose()
        before = snapshot()
        try:
            output = sandbox.run(['exec', '-T', 'netbox', sandbox.PYTHON, '-c', CHECK], capture=True,
                                 input=json.dumps(dict(
                                     {name: (sandbox.ROOT / name).read_text()
                                      for name in ('pyproject.toml', 'README.md', 'LICENSE')},
                                     export_dist=bool(args.dist_dir), release_tag=args.release_tag)))
            lines = output.splitlines(keepends=True)
            payloads = [line for line in lines if line.startswith('RELEASE_DISTRIBUTIONS=')]
            if args.dist_dir:
                if len(payloads) != 1:
                    raise RuntimeError('Missing verified distribution export')
                distributions = json.loads(payloads[0].split('=', 1)[1])
            print(sandbox.redact(''.join(line for line in lines
                                        if not line.startswith('RELEASE_DISTRIBUTIONS='))), end='')
            for marker in ('RELEASE_WHEEL_ASSETS_OK', 'RELEASE_RETIRED_UI_ABSENT', 'RELEASE_INSTALLED_IMPORT_OK',
                           'RELEASE_PROJECT_METADATA_LICENSE_OK', 'PROFILE_TESTS_ISOLATED',
                           'RELEASE_CLEAN_INSTALL_MIGRATIONS_TESTS_OK'):
                if marker not in output:
                    raise RuntimeError('Missing release verification marker: ' + marker)
        finally:
            if snapshot() != before:
                raise RuntimeError('RELEASE_LIVE_CHANGED: live native/plugin state differs')
            print('RELEASE_LIVE_UNCHANGED')
        if args.dist_dir:
            if len(distributions) != 2:
                raise RuntimeError('Expected one wheel and one source archive')
            decoded = {}
            for name, data in distributions.items():
                if not re.fullmatch(r'netbox_custom_field_profiles-[A-Za-z0-9_.+-]+(?:\.whl|\.tar\.gz)', name):
                    raise RuntimeError('Unexpected distribution filename')
                decoded[name] = base64.b64decode(data, validate=True)
            if sum(name.endswith('.whl') for name in decoded) != 1:
                raise RuntimeError('Expected exactly one tested wheel')
            args.dist_dir.mkdir(parents=True, exist_ok=True)
            if any(args.dist_dir.iterdir()):
                raise RuntimeError('Distribution output directory must be empty')
            for name, data in decoded.items():
                (args.dist_dir / name).write_bytes(data)
            print('RELEASE_DISTRIBUTIONS_EXPORTED ' + str(args.dist_dir))
        print(f'RELEASE_CHECK_OK elapsed={time.monotonic() - started:.2f}s')
        return 0
    except (RuntimeError, OSError, ValueError, TypeError) as error:
        print('RELEASE_CHECK_ERROR: ' + sandbox.redact(str(error)), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
