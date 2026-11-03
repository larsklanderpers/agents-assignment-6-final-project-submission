"""Read-only public GitHub PR intake, pinned to exact base/head commits.

Downloads into a NEW bare repository; never checks out or executes repository code.
Private GitHub repositories and non-GitHub hosts are deliberately unsupported.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import urllib.request

from repository_intake import freeze, git


def parse_url(url):
    match = re.fullmatch(r'https://github\.com/([A-Za-z0-9][A-Za-z0-9-]*)/([A-Za-z0-9_.-]+)/pull/([1-9][0-9]*)/?', url)
    if not match or match[2] in {'.', '..'}:
        raise ValueError('Expected a public https://github.com/owner/repo/pull/number URL')
    return match.groups()


def metadata(url):
    owner, repo, number = parse_url(url)
    request = urllib.request.Request(f'https://api.github.com/repos/{owner}/{repo}/pulls/{number}',
        headers={'Accept': 'application/vnd.github+json', 'User-Agent': 'Review-Ledger-read-only-intake'})
    with urllib.request.urlopen(request, timeout=30) as response:
        if response.geturl() != request.full_url:
            raise ValueError('Redirected PR identity unsupported')
        data = response.read(2 * 1024 * 1024 + 1)
    if len(data) > 2 * 1024 * 1024:
        raise ValueError('PR metadata too large')
    value = json.loads(data)
    head, base = value['head']['sha'], value['base']['sha']
    if not all(re.fullmatch('[0-9a-f]{40}', sha) for sha in (head, base)):
        raise ValueError('Invalid commit IDs')
    if value['number'] != int(number) or value['base']['repo']['full_name'].lower() != f'{owner}/{repo}'.lower():
        raise ValueError('PR repository identity mismatch')
    return {'kind': 'github_pr', 'url': url, 'head': head, 'base': base, 'state': value['state'],
            'repository': f'{owner}/{repo}', 'number': int(number)}


def ingest(url, output, paths=None):
    owner, repo, number = parse_url(url)
    pinned = metadata(url)
    # Closed PRs may be inspected as historical evidence; live repair freshness
    # separately requires an open PR and cannot approve a historical snapshot.
    output.mkdir(parents=True, exist_ok=False)
    (output / 'origin.json').write_text(json.dumps(pinned, indent=2), encoding='utf-8')
    bare = output / 'source.git'
    subprocess.run(['git', 'init', '--bare', str(bare)], check=True, capture_output=True, timeout=30)
    # Explicit HTTPS host/path, no repository hooks, no working tree, no submodules.
    remote = f'https://github.com/{owner}/{repo}.git'
    for ref in (f'refs/pull/{number}/head', pinned['base']):
        subprocess.run(['git', '-C', str(bare), '-c', 'credential.helper=', 'fetch', '--no-tags', '--depth=1',
                        remote, ref], check=True, capture_output=True, timeout=120)
        expected = pinned['head'] if ref.startswith('refs/') else pinned['base']
        if git(bare, 'rev-parse', 'FETCH_HEAD').decode().strip() != expected:
            raise ValueError('PR changed during fetch; retained download cannot authorize a repair')
    if metadata(url) != pinned:
        raise ValueError('PR changed during intake; prepare a new snapshot')
    # Freeze committed blobs directly; bare repositories have no working-tree changes.
    snapshot = freeze(bare, pinned['head'], paths, pinned['base'])
    (output / 'snapshot.json').write_text(json.dumps(snapshot, indent=2), encoding='utf-8')
    return {'origin': pinned, 'snapshot_sha256': snapshot['snapshot_sha256'],
            'selected_files': len(snapshot['files']), 'changed_paths': snapshot['changed_paths']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--url', required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--path', action='append', dest='paths')
    args = parser.parse_args()
    print(json.dumps(ingest(args.url, args.output, args.paths), indent=2))
