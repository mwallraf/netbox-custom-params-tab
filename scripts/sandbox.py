"""Dedicated local sandbox. Configuration is data and never shell sourced."""
import argparse
import fcntl
import json
import os
from pathlib import Path
import re
import secrets
import socket
import string
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'netbox-custom-field-profiles'
PYTHON = '/opt/netbox/venv/bin/python'
MANAGE = '/opt/netbox/netbox/manage.py'
IMAGE = 'netboxcommunity/netbox:v4.7.4-5.1.1'
SECRET_NAMES = ('DB_PASSWORD', 'REDIS_PASSWORD', 'REDIS_CACHE_PASSWORD', 'SECRET_KEY',
                'SUPERUSER_PASSWORD', 'API_TOKEN_PEPPER_1', 'SUPERUSER_API_KEY', 'SUPERUSER_API_TOKEN')


def new_env():
    alphabet = string.ascii_letters + string.digits
    result = {key: ''.join(secrets.choice(alphabet) for _ in range(64)) for key in SECRET_NAMES}
    result['SUPERUSER_API_KEY'] = ''.join(secrets.choice(alphabet) for _ in range(12))
    result['SUPERUSER_API_TOKEN'] = ''.join(secrets.choice(alphabet) for _ in range(40))
    result.update(COMPOSE_PROJECT_NAME=PROJECT, NETBOX_PORT='18047', SUPERUSER_NAME='admin',
                  SUPERUSER_EMAIL='admin@example.test')
    return result


def parse_env(content):
    result = {}
    for line in content.splitlines():
        if not line or line.startswith('#'):
            continue
        match = re.fullmatch(r'([A-Z][A-Z0-9_]*)=([A-Za-z0-9_.@:/+-]+)', line)
        if not match or match[1] in result:
            raise ValueError('invalid or duplicate environment entry (values redacted)')
        result[match[1]] = match[2]
    return result


def validate_env(values):
    expected = set(SECRET_NAMES) | {'COMPOSE_PROJECT_NAME', 'NETBOX_PORT', 'SUPERUSER_NAME', 'SUPERUSER_EMAIL'}
    if set(values) != expected or any(not v for v in values.values()):
        raise ValueError('incomplete or unexpected environment keys (values redacted)')
    if values['COMPOSE_PROJECT_NAME'] != PROJECT:
        raise ValueError('sandbox project identity cannot be changed')
    if not values['NETBOX_PORT'].isdigit() or not 1024 <= int(values['NETBOX_PORT']) <= 65535:
        raise ValueError('invalid localhost port')
    for key in SECRET_NAMES:
        minimum = 12 if key == 'SUPERUSER_API_KEY' else 40
        if len(values[key]) < minimum or not values[key].isalnum():
            raise ValueError('invalid generated credential format (values redacted)')
    if len(values['SUPERUSER_API_KEY']) != 12 or len(values['SUPERUSER_API_TOKEN']) != 40:
        raise ValueError('invalid native token format (values redacted)')
    return values


def ensure_env(path=None):
    path = path or ROOT / '.env'
    path = Path(path)
    if path.is_symlink():
        raise ValueError('environment must be a regular local file')
    lock_path = path.with_suffix('.env.lock')
    with open(lock_path, 'a') as lock:
        deadline = time.monotonic() + 10
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise ValueError('environment initialization lock timeout')
                time.sleep(.05)
        if path.exists():
            values = validate_env(parse_env(path.read_text()))
            if path.stat().st_mode & 0o777 != 0o600:
                raise ValueError('environment permissions must be 0600; credentials preserved')
            return values
        values = new_env()
        override = os.environ.get('NETBOX_PORT')
        if override:
            values['NETBOX_PORT'] = override
        validate_env(values)
        if path == ROOT / '.env':
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', int(values['NETBOX_PORT'])))
        fd, temporary = tempfile.mkstemp(prefix='.sandbox-env-', dir=path.parent)
        try:
            with os.fdopen(fd, 'w') as handle:
                handle.write(''.join(f'{k}={v}\n' for k, v in values.items()))
                handle.flush()
                os.fsync(handle.fileno())
            os.link(temporary, path)
        finally:
            os.unlink(temporary)
        return values


def compose_argv(args):
    forbidden = ('-p', '--project-name', '--project-directory', '-f', '--file', '--env-file')
    if not args or args[0].startswith('-') or any(a in forbidden or any(a.startswith(flag + '=') for flag in forbidden) for a in args):
        raise ValueError('Compose target overrides forbidden')
    return ['docker', 'compose', '--project-directory', str(ROOT), '-p', PROJECT,
            '-f', str(ROOT / 'docker-compose.yml'), '--env-file', str(ROOT / '.env'), *args]


def redact(text):
    path = ROOT / '.env'
    if path.exists():
        for name, value in parse_env(path.read_text()).items():
            if name in SECRET_NAMES:
                text = text.replace(value, '[REDACTED]')
    return text


def docker_environment():
    """Use the same daemon selection for metadata, checks, and mutations."""
    env = {k: v for k, v in os.environ.items() if not k.startswith(('COMPOSE_', 'DOCKER_'))}
    env.update(ensure_env())
    return env


def run(args, *, capture=False, input=None, timeout=900):
    env = docker_environment()
    process = subprocess.run(compose_argv(args), cwd=ROOT, env=env, text=True,
                             input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if process.returncode:
        if process.stdout:
            print(redact(process.stdout[-6000:]), file=sys.stderr)
        if process.stderr:
            print(redact(process.stderr[-6000:]), file=sys.stderr)
        raise RuntimeError('project Compose command failed: ' + args[0])
    if capture:
        return process.stdout
    if process.stdout:
        print(redact(process.stdout), end='')


def django(args, *, oneoff=False, input=None):
    prefix = ['run', '--rm', '--no-deps', '--entrypoint', PYTHON, 'netbox'] if oneoff else ['exec', '-T', 'netbox', PYTHON]
    return run([*prefix, MANAGE, *args], capture=True, input=input)


def runtime():
    for command in [['check'], ['migrate', '--check'], ['makemigrations', 'netbox_custom_field_profiles', '--check', '--dry-run']]:
        django(command)
    code = "from django.apps import apps; from django.db.migrations.recorder import MigrationRecorder; from django.conf import settings; VERSION=settings.VERSION; assert VERSION == '4.7.4-Docker-5.1.1', VERSION; assert apps.is_installed('netbox_custom_field_profiles'); assert MigrationRecorder.Migration.objects.filter(app='netbox_custom_field_profiles', name='0001_initial').exists(); print('RUNTIME_OK NetBox='+VERSION)"
    print(django(['shell', '-c', code]).strip())


def validate_compose():
    config = json.loads(run(['config', '--format', 'json'], capture=True))
    if config.get('name') != PROJECT:
        raise ValueError('wrong rendered project identity')
    if set(config.get('services', {})) != {'netbox', 'netbox-worker', 'postgres', 'redis', 'redis-cache'}:
        raise ValueError('unexpected sandbox service set')
    for name, volume in config.get('volumes', {}).items():
        if name not in {'postgres', 'redis', 'redis-cache', 'media'} or volume.get('external') or volume.get('driver_opts') or volume.get('driver', 'local') != 'local' or volume.get('name') != PROJECT + '_' + name:
            raise ValueError('external or shared volume forbidden')
    for name, network in config.get('networks', {}).items():
        if name != 'default' or network.get('external') or network.get('driver_opts') or network.get('name') != PROJECT + '_' + name:
            raise ValueError('external or shared network forbidden')
    for service, data in config['services'].items():
        validate_mounts(service, data.get('volumes', []))
        if data.get('network_mode') or data.get('volumes_from') or data.get('privileged'):
            raise ValueError('unsafe service namespace override')
        if any(network not in config.get('networks', {}) for network in data.get('networks', {})):
            raise ValueError('undeclared service network')
        if data.get('container_name'):
            raise ValueError('global container names forbidden')
        for port in data.get('ports', []):
            if service != 'netbox' or port.get('host_ip') != '127.0.0.1' or port.get('target') != 8080:
                raise ValueError('unsafe port exposure')
    return config


def validate_mounts(service, mounts):
    native = {'postgres': ('postgres', '/var/lib/postgresql'),
              'redis': ('redis', '/data'), 'redis-cache': ('redis-cache', '/data')}
    expected = {}
    if service in native:
        source, target = native[service]
        expected[target] = ('volume', source, False)
    elif service in ('netbox', 'netbox-worker'):
        expected['/opt/netbox/netbox/media'] = ('volume', 'media', False)
        for relative, target, readonly in [
            ('docker/plugins.py', '/etc/netbox/config/plugins.py', True),
            ('netbox_custom_field_profiles', '/opt/netbox-custom-field-profiles/netbox_custom_field_profiles', False),
            ('scripts', '/opt/netbox-custom-field-profiles/scripts', True),
            ('tests', '/opt/netbox-custom-field-profiles/tests', True),
            ('testing', '/opt/netbox-custom-field-profiles/testing', True),
            ('pytest.ini', '/opt/netbox-custom-field-profiles/pytest.ini', True),
        ]:
            path = ROOT / relative
            if path.resolve() != path or not path.exists():
                raise ValueError('sandbox bind path missing or symlinked')
            expected[target] = ('bind', str(path), readonly)
    else:
        raise ValueError('unexpected sandbox service')
    actual = {}
    for mount in mounts:
        target = mount.get('target')
        if target in actual or mount.get('volume', {}).get('subpath'):
            raise ValueError('duplicate or redirected sandbox mount')
        actual[target] = (mount.get('type'), mount.get('source'), bool(mount.get('read_only')))
    if actual != expected:
        raise ValueError('unexpected or external service mount')


def setup():
    ensure_env()
    migration = ROOT / 'netbox_custom_field_profiles/migrations/0001_initial.py'
    if not migration.read_text().startswith('# Generated by Django'):
        raise ValueError('initial schema requires explicit prepare-schema before native bootstrap')
    validate_compose()
    run(['build'])
    run(['up', '-d', '--wait', '--wait-timeout', '180', 'postgres', 'redis', 'redis-cache'])
    run(['up', '-d', '--wait', '--wait-timeout', '600'])
    runtime()
    seed()
    print('SANDBOX_READY')


def seed(check=False):
    code = "exec(open('/opt/netbox-custom-field-profiles/scripts/seed_sandbox.py').read()); seed(check=" + str(check) + ")"
    print(django(['shell', '-c', code]).strip())


def smoke():
    from smoke_sandbox import smoke as verify
    verify()


def prepare_schema():
    """One-time direct interpreter generation, strictly before native bootstrap."""
    ensure_env()
    validate_compose()
    run(['build'])
    run(['up', '-d', '--wait', '--wait-timeout', '180', 'postgres', 'redis', 'redis-cache'])
    code = "from django.db import connection; from django.db.migrations.recorder import MigrationRecorder; tables=connection.introspection.table_names(); assert not any(t.startswith('netbox_custom_field_profiles_') for t in tables), 'plugin tables already exist'; assert 'django_migrations' not in tables or not MigrationRecorder.Migration.objects.filter(app='netbox_custom_field_profiles').exists(), 'plugin migration already applied'; print('PRE_BOOTSTRAP_SCHEMA_ABSENT')"
    print(django(['shell', '-c', code], oneoff=True).strip())
    migration = ROOT / 'netbox_custom_field_profiles/migrations/0001_initial.py'
    if migration.read_text().startswith('# Generated by Django'):
        raise ValueError('initial schema already generated; use normal setup')
    original = migration.read_bytes()
    migration.unlink()
    try:
        print(django(['makemigrations', 'netbox_custom_field_profiles', '--noinput'], oneoff=True).strip())
        if not migration.exists() or not migration.read_text().startswith('# Generated by Django'):
            raise RuntimeError('native migration generation did not produce expected schema')
    except BaseException:
        if not migration.exists():
            migration.write_bytes(original)
        raise
    print('NATIVE_SCHEMA_GENERATED_BEFORE_BOOTSTRAP')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['env', 'compose', 'check', 'setup', 'verify-runtime', 'prepare-schema', 'seed', 'seed-check', 'smoke', 'reset', 'lifecycle-check'])
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == 'env':
        ensure_env()
        print('ENV_READY')
    elif args.command == 'compose':
        if not args.args or args.args[0] != 'config':
            validate_compose()
        run(args.args)
    elif args.command == 'check':
        ensure_env()
        validate_compose()
        print('CONFIG_OK')
    elif args.command == 'setup':
        setup()
    elif args.command == 'prepare-schema':
        prepare_schema()
    elif args.command in ('seed', 'seed-check'):
        seed(check=args.command == 'seed-check')
    elif args.command == 'smoke':
        smoke()
    elif args.command in ('reset', 'lifecycle-check'):
        from lifecycle_sandbox import reset, check
        (reset if args.command == 'reset' else check)()
    else:
        runtime()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print('SANDBOX_ERROR: ' + redact(str(error)), file=sys.stderr)
        sys.exit(1)
