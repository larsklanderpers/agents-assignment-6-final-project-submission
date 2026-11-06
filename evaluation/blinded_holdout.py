"""Three separate processes: private oracle checks, public-only review, locked scoring.

The model has no filesystem tools. Its complete payloads are retained for audit.
The host is not an OS-enforced secret store; blinding is at the model-input boundary.
"""
import argparse
import ast
import asyncio
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import statistics
import time


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def save_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(data, stream, indent=2)


def check_frozen(home):
    record = read(home / 'freeze.json')
    changed = [name for name, expected in record['files'].items()
               if not (home / 'frozen' / name).is_file() or sha(home / 'frozen' / name) != expected]
    if changed:
        raise ValueError('Frozen system changed')
    sys.path.insert(0, str(home / 'frozen'))
    return record


def check_public(public):
    if set(public) != {'schema', 'cases'} or len(public['cases']) != 12:
        raise ValueError('Expected twelve public cases and schema only')
    ids = set()
    for case in public['cases']:
        if set(case) != {'id', 'files', 'contracts'} or case['id'] in ids:
            raise ValueError('Public package includes unexpected fields or duplicate IDs')
        ids.add(case['id'])
        if set(case['files']) != {'subject.py', 'tests/test_visible.py'}:
            raise ValueError('Unsupported public file scope')
        for name, file in case['files'].items():
            if set(file) != {'role', 'content'} or file['role'] != ('source' if name == 'subject.py' else 'test'):
                raise ValueError('Unexpected public metadata')
            ast.parse(file['content'])
        if not case['contracts'] or not all(isinstance(k, str) and isinstance(v, str) for k, v in case['contracts'].items()):
            raise ValueError('Invalid contracts')


def preflight(home, public_path, private_path, output):
    check_frozen(home)
    from evaluation.end_to_end import run_tests
    import approval_executor as ae
    public, private = read(public_path), read(private_path)
    check_public(public)
    answers = {c['id']: c for c in private['cases']}
    if set(answers) != {c['id'] for c in public['cases']}:
        raise ValueError('Public/private IDs differ')
    output.mkdir(parents=True, exist_ok=False)
    ae.preflight()
    rows = []
    for case in public['cases']:
        answer = answers[case['id']]
        original = run_tests(case['files'], answer['hidden_tests'], output / case['id'] / 'original')
        reference = run_tests(answer['reference_files'], answer['hidden_tests'], output / case['id'] / 'reference')
        row = {'id': case['id'], 'original': original, 'reference': reference,
               'consistent': original['status'] == answer['original_oracle_expected'] and reference['status'] == 'passed'}
        rows.append(row)
        print(json.dumps({'id': case['id'], 'oracle_consistent': row['consistent']}), flush=True)
    save_new(output / 'report.json', {'public_sha256': sha(public_path), 'private_sha256': sha(private_path),
        'all_consistent': all(r['consistent'] for r in rows), 'rows': rows})
    if not all(r['consistent'] for r in rows):
        raise SystemExit(1)


def seal(home, public_path, private_path, preflight_path):
    freeze = check_frozen(home)
    report = read(preflight_path)
    if not report['all_consistent'] or report['public_sha256'] != sha(public_path) or report['private_sha256'] != sha(private_path):
        raise ValueError('Oracle checks do not match final packages')
    # The run side reads only this receipt, which contains no labels or test content.
    save_new(home / 'package-lock.json', {'public_sha256': sha(public_path), 'private_sha256': sha(private_path),
        'preflight_sha256': sha(preflight_path), 'frozen_commit': freeze['frozen_commit'],
        'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'oracle_consistent_cases': 12})


async def run_public(home, public_path, output):
    freeze = check_frozen(home)
    public = read(public_path)
    check_public(public)
    if sha(public_path) != read(home / 'package-lock.json')['public_sha256']:
        raise ValueError('Public cases changed after seal')
    from hardening_review import review_files
    from dotenv import load_dotenv
    # Read only credentials/configuration from the user's established environment;
    # never copy .env or emit its values other than the nonsecret model identifier.
    load_dotenv(Path(__file__).resolve().parents[1] / '.env')
    if os.environ.get('REVIEW_LEDGER_MODEL') != freeze['model']:
        raise ValueError('Configured model differs from preregistration')
    output.mkdir(parents=True, exist_ok=False)
    rows = []
    for case in public['cases']:
        directory = output / case['id']
        started = time.monotonic()
        row = {'id': case['id']}
        try:
            await review_files(case['files'], case['contracts'], directory)
            row['status'] = 'complete'
        except Exception as error:
            row.update(status='failed', error_type=type(error).__name__)
        row['seconds'] = round(time.monotonic() - started, 3)
        rows.append(row)
        (output / 'runs.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
        print(json.dumps(row), flush=True)
    check_frozen(home)
    hashes = {p.relative_to(output).as_posix(): sha(p) for p in output.rglob('*') if p.is_file()}
    save_new(output / 'outputs-lock.json', {'files': hashes, 'public_sha256': sha(public_path),
        'frozen_commit': freeze['frozen_commit'], 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
        'assigned': len(public['cases']), 'complete': sum(r['status'] == 'complete' for r in rows)})


def symbol_at(source, line):
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno <= line <= node.end_lineno:
            return node.name
    return '<module>'


def count_findings(case, labels, findings):
    remaining = list(labels)
    counts = {k: {'tp': 0, 'fp': 0, 'fn': 0} for k in ('security', 'performance', 'style', 'test_gap')}
    matches = []
    for f in findings:
        symbol = symbol_at(case['files'][f['path']]['content'], f['line'])
        match = next((label for label in remaining if (label['category'], label['path'], label['symbol']) ==
                      (f['category'], f['path'], symbol)), None)
        if match:
            remaining.remove(match)
            counts[f['category']]['tp'] += 1
        else:
            counts[f['category']]['fp'] += 1
        matches.append({'finding': f, 'automatic_match': bool(match), 'symbol': symbol})
    for label in remaining:
        counts[label['category']]['fn'] += 1
    return counts, matches


def score(home, public_path, private_path, outputs, destination):
    check_frozen(home)
    lock = read(outputs / 'outputs-lock.json')
    if any(sha(outputs / name) != expected for name, expected in lock['files'].items()):
        raise ValueError('Locked reviewer outputs changed')
    package_lock = read(home / 'package-lock.json')
    if sha(public_path) != lock['public_sha256'] or sha(private_path) != package_lock['private_sha256']:
        raise ValueError('Scoring packages changed')
    public, private = read(public_path), read(private_path)
    answers = {c['id']: c for c in private['cases']}
    rows = {r['id']: r for r in read(outputs / 'runs.json')}
    report = {'frozen_commit': lock['frozen_commit'], 'author_model': private['author_model'], 'case_runs': len(rows),
              'failed_reviews': sum(r['status'] != 'complete' for r in rows.values()), 'modes': {},
              'human_adjudication': 'pending', 'repair_success_measured': False}
    for mode in ('raw', 'filtered'):
        details = []
        total = {k: {'tp': 0, 'fp': 0, 'fn': 0} for k in ('security', 'performance', 'style', 'test_gap')}
        clean = clean_pass = exact = 0
        for case in public['cases']:
            answer = answers[case['id']]
            completed = rows[case['id']]['status'] == 'complete'
            result = read(outputs / case['id'] / 'result.json') if completed else {}
            findings = result.get('accepted_defects', []) if mode == 'filtered' else [f for review in result.get('reviews', {}).values() for f in review['findings'] if f['disposition'] == 'defect']
            counts, matches = count_findings(case, answer['labels'], findings)
            for category in total:
                for key in total[category]: total[category][key] += counts[category][key]
            if not answer['labels']:
                clean += 1
                clean_pass += completed and not findings
            exact += completed and all(c['fp'] == c['fn'] == 0 for c in counts.values())
            details.append({'id': case['id'], 'review_status': rows[case['id']]['status'], 'counts': counts, 'matches': matches})
        for counts in total.values():
            counts['precision'] = counts['tp'] / (counts['tp'] + counts['fp']) if counts['tp'] + counts['fp'] else None
            counts['recall'] = counts['tp'] / (counts['tp'] + counts['fn']) if counts['tp'] + counts['fn'] else None
        aggregate = {k: sum(v[k] for v in total.values()) for k in ('tp', 'fp', 'fn')}
        report['modes'][mode] = {'categories': total, 'totals': aggregate,
            'micro_precision': aggregate['tp'] / (aggregate['tp'] + aggregate['fp']) if aggregate['tp'] + aggregate['fp'] else None,
            'micro_recall': aggregate['tp'] / (aggregate['tp'] + aggregate['fn']) if aggregate['tp'] + aggregate['fn'] else None,
            'macro_precision': statistics.mean(v['precision'] for v in total.values() if v['precision'] is not None) if any(v['precision'] is not None for v in total.values()) else None,
            'macro_recall': statistics.mean(v['recall'] for v in total.values() if v['recall'] is not None),
            'clean_controls': clean, 'clean_controls_without_findings': clean_pass,
            'exact_case_outcomes': exact, 'details': details}
    save_new(destination, report)
    print(json.dumps({mode: {k: v for k, v in summary.items() if k not in {'details', 'categories'}} for mode, summary in report['modes'].items()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['preflight', 'seal', 'run', 'score'])
    parser.add_argument('--home', required=True)
    parser.add_argument('--public', required=True)
    parser.add_argument('--private')
    parser.add_argument('--output')
    parser.add_argument('--preflight')
    parser.add_argument('--outputs')
    args = parser.parse_args()
    home, public = Path(args.home).resolve(), Path(args.public).resolve()
    if args.phase == 'preflight': preflight(home, public, Path(args.private), Path(args.output))
    elif args.phase == 'seal': seal(home, public, Path(args.private), Path(args.preflight))
    elif args.phase == 'run': asyncio.run(run_public(home, public, Path(args.output)))
    else: score(home, public, Path(args.private), Path(args.outputs), Path(args.output))
