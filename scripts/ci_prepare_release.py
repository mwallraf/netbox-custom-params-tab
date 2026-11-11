"""Validate a release checkout and install current release tooling into it."""
import ast
import os
from pathlib import Path
import re
import shutil
import subprocess
import tomllib

source = Path('source').resolve()
automation = Path('automation').resolve()
tag = os.environ.get('RELEASE_TAG', '')
if tag:
    if not re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+(?:[a-zA-Z0-9.-]+)?', tag):
        raise SystemExit('Invalid release tag')
    project = tomllib.loads((source / 'pyproject.toml').read_text())['project']
    if project['name'] != 'netbox-custom-field-profiles' or tag != 'v' + project['version']:
        raise SystemExit('Tag and distribution version must match')
    tree = ast.parse((source / 'netbox_custom_field_profiles/__init__.py').read_text())
    versions = [ast.literal_eval(node.value) for node in ast.walk(tree)
                if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == 'version' for target in node.targets)]
    if versions != [project['version']]:
        raise SystemExit('PluginConfig version must match package version')
    subprocess.run(['git', 'merge-base', '--is-ancestor', 'HEAD', 'origin/main'], cwd=source, check=True)
    # Read tagged product code; only the validation/export tool comes from this workflow.
    shutil.copyfile(automation / 'scripts/release_check.py', source / 'scripts/release_check.py')
    print('RELEASE_TAG_VERSION_AND_MAIN_ANCESTRY_OK ' + tag)
