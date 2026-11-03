"""Check exported source hashes, credential exclusions and frozen corpus bytes."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    manifest = ROOT / 'SOURCE-MANIFEST.json'
    checked = 0
    if manifest.exists():
        for name, expected in json.loads(manifest.read_text(encoding='utf-8')).items():
            relative = Path(name)
            if relative.is_absolute() or '..' in relative.parts or any(part in
                    {'.env', '.venv', '.git', 'artifacts', '__pycache__'} for part in relative.parts):
                raise ValueError('Forbidden package path')
            if hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() != expected:
                raise ValueError('Package hash mismatch: ' + name)
            checked += 1
    corpus = ROOT / 'evaluation/manifest.json'
    if hashlib.sha256(corpus.read_bytes()).hexdigest() != corpus.with_suffix('.sha256').read_text().strip():
        raise ValueError('Frozen corpus differs after checkout')
    print(json.dumps({'source_manifest_files_checked': checked, 'frozen_corpus_hash_matches': True,
                      'package_manifest_present': manifest.exists()}))


if __name__ == '__main__':
    main()
