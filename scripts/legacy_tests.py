"""Capture the real legacy runner status separately from blocking baseline checks."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import sandbox


def classify(returncode, output):
    lower = output.lower()
    if 'no module named pytest' in lower or 'pytest: not found' in lower:
        return 'runner-unavailable'
    if 'error collecting' in lower or 'errors during collection' in lower or returncode == 2:
        return 'collection-error'
    if 'error at setup' in lower or 'improperlyconfigured' in lower or 'modulenotfounderror' in lower:
        return 'setup-error'
    if returncode == 0:
        if not re.search(r'\b\d+ passed\b', output):
            return 'unverified-zero-exit'
        return 'passed'
    if returncode == 1:
        return 'test-failures'
    if returncode == 5:
        return 'no-tests-collected'
    return 'runner-error'


def counts(output):
    result = {}
    for number, name in re.findall(r'\b(\d+) (passed|failed|errors?|skipped|deselected)\b', output):
        result[name] = int(number)
    return result


def execute(args, values):
    env = sandbox.docker_environment()
    result = subprocess.run(sandbox.compose_argv(args), cwd=sandbox.ROOT, env=env,
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=600)
    return result.returncode, sandbox.redact(result.stdout)


def main():
    values = sandbox.ensure_env()
    sandbox.validate_compose()
    prefix = ['exec', '-T', '-w', '/opt/netbox-custom-field-profiles', 'netbox', sandbox.PYTHON, '-m', 'pytest']
    version_status, version = execute([*prefix, '--version'], values)
    command = [*prefix, 'tests/', '-v']
    status, output = execute(command, values)
    outcome = classify(status, output)
    report = {'command': command, 'runner_version': version.strip(), 'runner_version_exit': version_status,
              'exit_status': status, 'classification': outcome, 'counts': counts(output),
              'collection_status': 'failed' if outcome == 'collection-error' else ('unavailable' if outcome == 'runner-unavailable' else 'see-output'),
              'output': output}
    directory = sandbox.ROOT / '.sandbox'
    directory.mkdir(mode=0o700, exist_ok=True)
    path = directory / 'legacy-tests.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    path.chmod(0o600)
    print('LEGACY_REPORT classification=' + outcome + ' exit=' + str(status) + ' report=.sandbox/legacy-tests.json')
    return status if status else (0 if outcome == 'passed' else 3)


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as error:
        print('LEGACY_REPORT_ERROR: ' + sandbox.redact(str(error)), file=sys.stderr)
        sys.exit(3)
