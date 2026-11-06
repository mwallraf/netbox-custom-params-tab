"""One-time allowlisted source recovery; never includes local credentials."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

DIRECTORIES = ('netbox_custom_field_profiles', 'tests', 'testing', 'docker')
FILES = ('Makefile', 'docker-compose.yml', '.dockerignore', 'pyproject.toml', 'pytest.ini')


def inventory(root):
    paths = [root / name for name in FILES]
    for name in DIRECTORIES:
        paths.extend((root / name).rglob('*'))
    result = {}
    for path in sorted(paths):
        rel = path.relative_to(root)
        if any(p.startswith('.') or p == '__pycache__' or p.endswith('.egg-info') for p in rel.parts):
            if str(rel) != '.dockerignore':
                continue
        if path.is_symlink():
            raise ValueError('symlink forbidden: ' + str(rel))
        if path.is_file() and path.suffix != '.pyc':
            result[str(rel)] = hashlib.sha256(path.read_bytes()).hexdigest()
    if not result or not all(name in result for name in FILES):
        raise ValueError('incomplete source inventory')
    if not all(any(p.startswith(d + '/') for p in result) for d in DIRECTORIES):
        raise ValueError('missing source directory')
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['capture', 'verify', 'verify-layout'])
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--manifest', type=Path, default=Path('docs/development/source-recovery.md'))
    parser.add_argument('--commit')
    args = parser.parse_args()
    if args.command == 'capture':
        data = {'version': 1, 'files': inventory(args.root)}
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        if args.manifest.exists():
            raise ValueError('refusing to replace original manifest')
        args.manifest.write_text('# Source recovery\n\nOriginal renamed working snapshot; feature history: `42ad9c2`.\n\n```json\n' + json.dumps(data, indent=2) + '\n```\n')
        print('SOURCE_CAPTURE_OK')
    elif args.command == 'verify':
        data = json.loads(re.search(r'```json\n(.*?)\n```', args.manifest.read_text(), re.S)[1])
        if args.commit:
            actual = {p: hashlib.sha256(subprocess.check_output(['git', 'show', args.commit + ':' + p], cwd=args.root)).hexdigest() for p in data['files']}
        else:
            actual = inventory(args.root)
        if actual != data['files']:
            raise ValueError('source manifest mismatch')
        print('SOURCE_SNAPSHOT_OK')
    else:
        tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=args.root, text=True).splitlines())
        required = ['AGENTS.md', 'README.md', 'docs/REQUIREMENTS.md', '.planning/STATE.md', '.planning/ROADMAP.md', 'netbox_custom_field_profiles/__init__.py']
        if not all(p in tracked and (args.root / p).exists() for p in required):
            raise ValueError('canonical source/documents not tracked')
        if (args.root / '.worktrees/feature/implement-plugin/.git').exists():
            raise ValueError('obsolete pointer remains')
        worktrees = subprocess.check_output(['git', 'worktree', 'list', '--porcelain'], cwd=args.root, text=True)
        if worktrees.count('worktree ') != 1:
            raise ValueError('unexpected linked worktrees')
        print('SOURCE_LAYOUT_OK')


if __name__ == '__main__':
    main()
