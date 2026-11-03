"""Create a disposable committed development repo; never modify original Assignment 5."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from repository_intake import safe_path


def build(manifest, output):
    raw = manifest.read_bytes()
    if hashlib.sha256(raw).hexdigest() != manifest.with_suffix('.sha256').read_text().strip():
        raise ValueError('Development corpus changed')
    corpus = json.loads(raw)
    case = next(c for c in corpus['cases'] if c['id'] == 'a5-email-omission')
    output.mkdir(parents=True, exist_ok=False)
    repo = output / 'repository'
    repo.mkdir()
    for name, file in case['files'].items():
        safe_path(name)
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file['content'], encoding='utf-8', newline='')
    origin = {'kind': 'DELIBERATELY_SEEDED_DEVELOPMENT_COPY', 'case': case['id'],
              'original': corpus['origin'], 'mutation': case['seeded_mutation'],
              'original_repository_modified': False}
    (repo / 'ORIGIN.json').write_text(json.dumps(origin, indent=2), encoding='utf-8')
    (output / 'contracts.json').write_text(json.dumps(case['contracts'], indent=2), encoding='utf-8')
    for args in [('init',), ('add', '.'), ('-c', 'user.name=Review Ledger Development', '-c',
                 'user.email=development@example.invalid', 'commit', '-m', 'Seeded Assignment 5 repair experiment')]:
        subprocess.run(['git','-C',str(repo),*args], check=True, capture_output=True, timeout=30)
    return repo


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(build(args.manifest, args.output))
