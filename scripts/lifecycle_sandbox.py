"""Exercise only the fixed, validated development project's resources."""
import hashlib
import json
import subprocess
import secrets

import sandbox


def docker_json(args):
    result = subprocess.run(['docker', *args], text=True, capture_output=True, timeout=30,
                            env=sandbox.docker_environment())
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


def unrelated_ids(running=False):
    ids = docker_json(['ps', '-q' if running else '-aq']).splitlines()
    if not ids:
        return set()
    metadata = docker_json(['inspect', '--format', '{{json .Id}}|{{index .Config.Labels "com.docker.compose.project"}}', *ids])
    return {json.loads(line.partition('|')[0]) for line in metadata.splitlines()
            if line.partition('|')[2] != sandbox.PROJECT}


def sentinel(create=False):
    if create:
        marker = secrets.token_hex(24)
        code = "from dcim.models import Site; s,_=Site.objects.update_or_create(slug='cfp-sandbox-persistence', defaults={'name':'CFP sandbox persistence','description':" + repr(marker) + "})"
    else:
        code = "from dcim.models import Site; s=Site.objects.get(slug='cfp-sandbox-persistence')"
    code += "; import json; exec(open('/opt/netbox-custom-field-profiles/scripts/seed_sandbox.py').read()); print('SENTINEL='+json.dumps({'pk':s.pk,'marker':s.description,'seed':seed_snapshot()},sort_keys=True))"
    output = sandbox.django(['shell', '-c', code])
    return next(line for line in output.splitlines() if line.startswith('SENTINEL='))


def check():
    env_digest = hashlib.sha256((sandbox.ROOT / '.env').read_bytes()).digest()
    others = unrelated_ids(running=True)
    report = sandbox.ROOT / '.sandbox'
    report.mkdir(mode=0o700, exist_ok=True)
    (report / 'lifecycle-before.json').write_text(json.dumps(sorted(others)))
    sandbox.ensure_env()
    identity = sentinel(create=True)
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
    after = unrelated_ids()
    (report / 'lifecycle-after.json').write_text(json.dumps(sorted(after)))
    assert_original_containers(others, after)
    print('CREDENTIALS_STABLE unrelated-containers-unchanged LIFECYCLE_OK')


def assert_original_containers(before, after):
    if not before.issubset(after):
        raise RuntimeError('original unrelated container identities disappeared; inspect local lifecycle metadata')


if __name__ == '__main__':
    check()
