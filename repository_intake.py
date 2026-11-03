"""Freeze a bounded, committed Python repository selection without executing it."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

MAX_FILES = 40
MAX_FILE_BYTES = 128 * 1024
MAX_TOTAL_BYTES = 512 * 1024
CONFIGS = {'pyproject.toml', 'pytest.ini', 'setup.cfg', '.flake8', 'ruff.toml', '.ruff.toml'}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def safe_path(name):
    path = PurePosixPath(name)
    if (not name or str(path) != name or path.is_absolute() or
            any(part in {'.', '..', '.git', '.env', '.venv', '__pycache__'} for part in path.parts) or
            any(c in name for c in '\\:\x00\n\r') or
            any(part.endswith(('.', ' ')) for part in path.parts) or
            any(re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I) for part in path.parts)):
        raise ValueError('Unsafe repository path')
    if path.suffix != '.py' and path.name not in CONFIGS:
        raise ValueError('Only Python source/tests and declared configuration are supported')
    return name


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, timeout=30)
    if result.returncode:
        raise ValueError('Git read failed; verify repository and revision')
    return result.stdout


def freeze(repo, revision='HEAD', paths=None, base=None):
    repo = Path(repo).resolve()
    if revision.startswith('-') or (base and base.startswith('-')):
        raise ValueError('Invalid revision')
    commit = git(repo, 'rev-parse', '--verify', revision + '^{commit}').decode().strip()
    tree = git(repo, 'rev-parse', commit + '^{tree}').decode().strip()
    entries = {}
    for raw in git(repo, 'ls-tree', '-r', '-z', commit).split(b'\0'):
        if raw:
            meta, name = raw.split(b'\t', 1)
            mode, kind, oid = meta.decode().split()
            entries[name.decode('utf-8')] = (mode, kind, oid)
    selected = paths if paths else [n for n in entries if n.endswith('.py') or PurePosixPath(n).name in CONFIGS]
    if not selected or len(selected) > MAX_FILES or len(set(selected)) != len(selected):
        raise ValueError('Select between 1 and 40 unique files explicitly for larger repositories')
    files, total = {}, 0
    for name in sorted(selected):
        safe_path(name)
        if name not in entries or entries[name][0] not in {'100644', '100755'} or entries[name][1] != 'blob':
            raise ValueError('Selection must contain regular committed files; links/submodules are unsupported')
        oid = entries[name][2]
        if int(git(repo, 'cat-file', '-s', oid)) > MAX_FILE_BYTES:
            raise ValueError('File exceeds 128 KiB limit')
        raw = git(repo, 'cat-file', 'blob', oid)
        total += len(raw)
        if total > MAX_TOTAL_BYTES:
            raise ValueError('Selection exceeds 512 KiB limit')
        if b'\0' in raw or re.search(rb'AIza[\w-]{30,}|-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----|ghp_[A-Za-z0-9]{30,}', raw):
            raise ValueError('Binary content or credential pattern blocked; no snapshot created')
        text = raw.decode('utf-8')
        role = 'test' if PurePosixPath(name).name.startswith('test_') or 'tests' in PurePosixPath(name).parts else 'source'
        if not name.endswith('.py'):
            role = 'configuration'
        files[name] = {'role': role, 'git_blob': oid, 'sha256': hashlib.sha256(raw).hexdigest(), 'content': text}
    base_commit = git(repo, 'rev-parse', '--verify', base + '^{commit}').decode().strip() if base else None
    changed = git(repo, 'diff', '--name-only', '-z', base_commit, commit).decode().split('\0') if base else []
    snapshot = {'schema': 1, 'kind': 'committed_python_selection', 'repository_name': repo.name,
                'commit': commit, 'tree': tree, 'base_commit': base_commit,
                'changed_paths': [p for p in changed if p], 'files': files,
                'coverage': 'selected_files_only', 'excluded_file_count': len(entries) - len(files),
                'working_tree_changes_excluded': bool(git(repo, 'status', '--porcelain')),
                'limits': {'max_files': MAX_FILES, 'max_file_bytes': MAX_FILE_BYTES, 'max_total_bytes': MAX_TOTAL_BYTES},
                'limitations': ['Committed revision only; uncommitted changes are excluded.',
                    'No dependency installation, imports, hooks, tests, or repository commands executed.',
                    'Selected context may be incomplete; this snapshot alone does not authorize patches.']}
    snapshot['snapshot_sha256'] = digest(snapshot)
    return snapshot


def validate(snapshot):
    payload = dict(snapshot)
    expected = payload.pop('snapshot_sha256', None)
    if digest(payload) != expected:
        raise ValueError('Snapshot digest mismatch')
    for name, file in snapshot['files'].items():
        safe_path(name)
        if hashlib.sha256(file['content'].encode()).hexdigest() != file['sha256']:
            raise ValueError('File digest mismatch')
    return snapshot


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True)
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--base')
    parser.add_argument('--path', action='append', dest='paths')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = freeze(args.repo, args.revision, args.paths, args.base)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps({'snapshot': str(target), 'commit': result['commit'],
                      'files': len(result['files']), 'snapshot_sha256': result['snapshot_sha256']}))


if __name__ == '__main__':
    main()
