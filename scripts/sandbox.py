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
    if not args or args[0].startswith('-') or any(a in ('-p', '--project-name', '--project-directory', '-f', '--file', '--env-file') for a in args):
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


def run(args, *, capture=False, input=None, timeout=900):
    values = ensure_env()
    env = {k: v for k, v in os.environ.items() if not k.startswith(('COMPOSE_', 'DOCKER_'))}
    env.update(values)
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
    code = "from django.apps import apps; from django.db.migrations.recorder import MigrationRecorder; from netbox.release import VERSION; assert VERSION == '4.7.4', VERSION; assert apps.is_installed('netbox_custom_field_profiles'); assert MigrationRecorder.Migration.objects.filter(app='netbox_custom_field_profiles', name='0001_initial').exists(); print('RUNTIME_OK NetBox='+VERSION)"
    print(django(['shell', '-c', code]).strip())


def validate_compose():
    config = json.loads(run(['config', '--format', 'json'], capture=True))
    if config.get('name') != PROJECT:
        raise ValueError('wrong rendered project identity')
    for name, volume in config.get('volumes', {}).items():
        if volume.get('external') or volume.get('name') != PROJECT + '_' + name:
            raise ValueError('external or shared volume forbidden')
    for service, data in config['services'].items():
        if data.get('container_name'):
            raise ValueError('global container names forbidden')
        for port in data.get('ports', []):
            if service != 'netbox' or port.get('host_ip') != '127.0.0.1' or port.get('target') != 8080:
                raise ValueError('unsafe port exposure')
    return config


def setup():
    ensure_env()
    validate_compose()
    run(['build'])
    run(['up', '-d', '--wait', '--wait-timeout', '180', 'postgres', 'redis', 'redis-cache'])
    run(['up', '-d', '--wait', '--wait-timeout', '600'])
    runtime()
    print('SANDBOX_READY')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['env', 'compose', 'check', 'setup', 'verify-runtime'])
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command == 'env':
        ensure_env()
        print('ENV_READY')
    elif args.command == 'compose':
        run(args.args)
    elif args.command == 'check':
        ensure_env()
        validate_compose()
        print('CONFIG_OK')
    elif args.command == 'setup':
        setup()
    else:
        runtime()


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print('SANDBOX_ERROR: ' + redact(str(error)), file=sys.stderr)
        sys.exit(1)
