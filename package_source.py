"""Export reviewable source only; never include local credentials or run evidence."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent


def source_files():
    files = [p for p in ROOT.iterdir() if p.is_file() and
             not p.name.startswith('~$') and
             (p.suffix in {'.py', '.md', '.cmd', '.lock', '.ps1', '.pdf', '.pptx'} or p.name in {'.gitignore', '.gitattributes', '.env.example', 'dashboard.html', 'dashboard-scope.json'})]
    for folder in ('evaluation', 'results', 'deliverables'):
        files.extend(p for p in (ROOT / folder).rglob('*') if p.is_file() and
                     not p.name.startswith('~$') and
                     p.suffix in {'.py', '.json', '.sha256', '.md', '.csv', '.jsonl', '.log', '.pdf', '.pptx'})
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    files = source_files()
    with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        manifest = {}
        for path in files:
            name = path.relative_to(ROOT).as_posix()
            raw = path.read_bytes()
            if path.suffix not in {'.pdf', '.pptx'}:
                raw = raw.replace(b'\r\n', b'\n')  # Same bytes as LF Git checkouts.
            manifest[name] = hashlib.sha256(raw).hexdigest()
            archive.writestr(name, raw)
        archive.writestr('SOURCE-MANIFEST.json', json.dumps(manifest, indent=2))
    print(json.dumps({'archive': str(output), 'files': len(files),
        'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
