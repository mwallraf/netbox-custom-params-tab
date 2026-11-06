"""Run only plugin-owned tests in native NetBox, preserving the live sandbox."""
import argparse
import re
import subprocess
import sys
import time

import sandbox


SNAPSHOT = '''
import hashlib, json
from django.db import connection
tables = sorted(t for t in connection.introspection.table_names()
    if t == 'dcim_device' or t.startswith('extras_customfield')
    or t.startswith('netbox_custom_field_profiles_'))
payload = []
with connection.cursor() as cursor:
    for table in tables:
        cursor.execute('SELECT * FROM ' + connection.ops.quote_name(table) + ' ORDER BY id')
        payload.append((table, cursor.fetchall()))
print('PROFILE_LIVE_SNAPSHOT=' + hashlib.sha256(json.dumps(payload, default=str, sort_keys=True).encode()).hexdigest())
'''


def snapshot():
    output = sandbox.django(['shell', '-c', SNAPSHOT])
    match = re.search(r'^PROFILE_LIVE_SNAPSHOT=([0-9a-f]{64})$', output, re.MULTILINE)
    if not match:
        raise RuntimeError('live snapshot was not produced')
    return match[1]


def run(label):
    if not re.fullmatch(r'netbox_custom_field_profiles\.tests(?:\.[A-Za-z_][A-Za-z_0-9]*)*', label):
        raise ValueError('test label must name the plugin-owned native test package')
    sandbox.validate_compose()
    before = snapshot()
    started = time.monotonic()
    args = ['exec', '-T', 'netbox', sandbox.PYTHON, sandbox.MANAGE, 'test', label,
            '--noinput', '--keepdb', '--testrunner',
            'netbox_custom_field_profiles.tests.runner.ProfileTestRunner']
    result = subprocess.run(sandbox.compose_argv(args), cwd=sandbox.ROOT,
                            env=sandbox.docker_environment(), text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    print(sandbox.redact(result.stdout), end='')
    after = snapshot()
    if before != after:
        raise RuntimeError('PROFILE_LIVE_CHANGED: live native/plugin snapshot differs after tests')
    print('PROFILE_LIVE_UNCHANGED')
    if result.returncode:
        return result.returncode
    if not re.search(r'Ran [1-9][0-9]* tests? in ', result.stdout):
        raise RuntimeError('PROFILE_TESTS_EMPTY: no nonzero executed-test result')
    if 'PROFILE_TESTS_ISOLATED' not in result.stdout:
        raise RuntimeError('PROFILE_TESTS_DATABASE: missing native isolation confirmation')
    print(f'PROFILE_TESTS_OK elapsed={time.monotonic() - started:.2f}s')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--label', default='netbox_custom_field_profiles.tests')
    args = parser.parse_args()
    try:
        return run(args.label)
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print('PROFILE_TESTS_ERROR: ' + sandbox.redact(str(error)), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
