"""Exercise only the fixed, validated development project's resources."""
import hashlib
import json
import subprocess

import sandbox


def docker_json(args):
    result = subprocess.run(['docker', *args], text=True, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError('Docker metadata inspection failed')
    return result.stdout


def validate_volume(name, labels):
    if not name.startswith(sandbox.PROJECT + '_') or labels.get('com.docker.compose.project') != sandbox.PROJECT:
        raise ValueError('refusing a volume not owned by this sandbox')


def reset():
    config = sandbox.validate_compose()
    for volume in config['volumes'].values():
        name = volume['name']
        existing = docker_json(['volume', 'ls', '--format', '{{.Name}}']).splitlines()
        if name in existing:
            details = json.loads(docker_json(['volume', 'inspect', name]))[0]
            validate_volume(name, details.get('Labels') or {})
    sandbox.run(['down', '--volumes', '--remove-orphans'])
    sandbox.setup()
    sandbox.seed()
    sandbox.smoke()
    print('PROJECT_RESET_OK')


def unrelated_ids():
    ids = docker_json(['ps', '-aq']).splitlines()
    if not ids:
        return set()
    containers = json.loads(docker_json(['inspect', *ids]))
    return {item['Id'] for item in containers
            if (item['Config'].get('Labels') or {}).get('com.docker.compose.project') != sandbox.PROJECT}


def sentinel():
    code = "from dcim.models import Site; s,_=Site.objects.get_or_create(slug='cfp-sandbox-persistence', defaults={'name':'CFP sandbox persistence'}); print('SENTINEL_ID='+str(s.pk))"
    output = sandbox.django(['shell', '-c', code])
    return next(line for line in output.splitlines() if line.startswith('SENTINEL_ID='))


def check():
    env_digest = hashlib.sha256((sandbox.ROOT / '.env').read_bytes()).digest()
    others = unrelated_ids()
    identity = sentinel()
    for _ in range(2):
        sandbox.setup()
        assert sentinel() == identity, 'database identity changed on setup'
    sandbox.run(['down'])
    sandbox.run(['up', '-d', '--wait', '--wait-timeout', '600'])
    assert sentinel() == identity, 'database identity changed on restart'
    assert hashlib.sha256((sandbox.ROOT / '.env').read_bytes()).digest() == env_digest, 'credentials changed'
    sandbox.smoke()
    print('PERSISTENCE_OK')
    reset()
    code = "from dcim.models import Site; assert not Site.objects.filter(slug='cfp-sandbox-persistence').exists(); print('RESET_RECREATED_DATABASE_OK')"
    print(sandbox.django(['shell', '-c', code]).strip())
    assert hashlib.sha256((sandbox.ROOT / '.env').read_bytes()).digest() == env_digest, 'reset rotated credentials'
    assert others == unrelated_ids(), 'unrelated container identities changed'
    print('CREDENTIALS_STABLE unrelated-containers-unchanged LIFECYCLE_OK')


if __name__ == '__main__':
    check()
