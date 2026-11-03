"""Run-specific operator entrypoint. Never supplies a human approval."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import uuid

PROJECT = Path(__file__).resolve().parent


def run_home(identity):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', identity):
        raise ValueError('Run ID must be 1-80 letters, digits, underscores or hyphens')
    return PROJECT / 'artifacts/runs' / identity


def status(home):
    """Read-only: SQLite URI mode=ro never creates a missing ledger."""
    result = {'run': json.loads((home / 'run.json').read_text()), 'candidates': []}
    for path in sorted(home.glob('artifacts/**/manifest.json')):
        m = json.loads(path.read_text())
        row = {'path': str(path.parent.relative_to(home)), 'candidate_id': m['candidate_id'],
               'patch_sha256': m['patch_sha256'], 'plan_version': m['plan_version'],
               'patch_hash_matches': hashlib.sha256((path.parent / 'candidate.patch').read_bytes()).hexdigest() == m['patch_sha256'],
               'operations': []}
        db = path.parent / 'ledger.sqlite'
        if db.exists():
            with sqlite3.connect(db.as_uri() + '?mode=ro', uri=True) as connection:
                row['operations'] = [dict(zip(('id', 'state', 'post_tree'), r)) for r in
                    connection.execute('SELECT id,state,post_tree FROM operations')]
        result['candidates'].append(row)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['new', 'status', 'doctor', 'reviews', 'plan', 'propose-tests', 'replace-tests',
        'review-tests', 'prepare-optimization', 'review-optimization', 'prepare-failure',
        'review-fault', 'replan', 'review-repair'])
    parser.add_argument('--run')
    args = parser.parse_args()
    if args.action == 'doctor':
        import approval_executor as ae
        from dotenv import load_dotenv
        load_dotenv(PROJECT / '.env')
        checks = {'python_312': sys.version_info[:2] == (3, 12),
                  'git': subprocess.run(['git', '--version'], capture_output=True).returncode == 0,
                  'key_configured': bool(os.environ.get('GOOGLE_API_KEY')),
                  'model_configured': bool(os.environ.get('REVIEW_LEDGER_MODEL'))}
        try:
            ae.preflight()
            checks['docker_and_pinned_image'] = True
        except Exception as error:
            checks['docker_and_pinned_image'] = False
            checks['docker_error_type'] = type(error).__name__
        print(json.dumps(checks, indent=2))
        return 0 if all(v for k, v in checks.items() if k != 'docker_error_type') else 1
    if args.action == 'new':
        identity = args.run or 'demo-' + uuid.uuid4().hex[:12]
        home = run_home(identity)
        home.mkdir(parents=True, exist_ok=False)
        (home / 'run.json').write_text(json.dumps({'schema': 1, 'run_id': identity,
            'mode': 'live_human', 'first_candidate': None}, indent=2))
        print(identity)
        return 0
    if not args.run:
        parser.error('--run is required for an existing run')
    home = run_home(args.run)
    record = json.loads((home / 'run.json').read_text())
    if args.action == 'status':
        print(json.dumps(status(home), indent=2))
        return 0
    os.environ['REVIEW_LEDGER_RUN_HOME'] = str(home)
    if args.action == 'replace-tests':
        import approval_executor as ae
        from runtime_paths import first_candidate
        previous = first_candidate()
        old = ae.validate(previous)
        with sqlite3.connect((previous / 'ledger.sqlite').as_uri() + '?mode=ro', uri=True) as db:
            states = [row[0] for row in db.execute('SELECT state FROM operations')]
        if len(states) != 1 or states[0] not in {'AMBIGUOUS', 'FAILED', 'CANCELLED'}:
            raise ValueError('Replacement requires exactly one terminal unsuccessful operation')
        original = previous.with_name(previous.name.split('-exec-', 1)[0])
        directory = ae.prepare(original, replacement=True)
        record.setdefault('prior_first_candidates', []).append(record['first_candidate'])
        record['first_candidate'] = str(directory.relative_to(home))
        (home / 'run.json').write_text(json.dumps(record, indent=2))
        return 0
    commands = {'reviews': ['spike_live.py', 'start', '--run', args.run],
                'plan': ['spike_plan.py', 'start', '--run', args.run],
                'propose-tests': ['prepare_first_patch.py']}
    if args.action in commands:
        if args.action == 'propose-tests' and record['first_candidate']:
            raise ValueError('Tests already proposed; inspect or create a new run')
        proposals = list((home / 'artifacts/first-patch').glob('candidate-*/manifest.json')) if args.action == 'propose-tests' else []
        if not proposals:
            subprocess.run([sys.executable, *commands[args.action]], cwd=PROJECT, check=True)
        if args.action == 'propose-tests':
            import approval_executor as ae
            candidates = [p for p in (home / 'artifacts/first-patch').glob('candidate-*/manifest.json') if '-exec-' not in p.parent.name]
            if len(candidates) != 1:
                raise ValueError('Expected exactly one new test proposal')
            directory = ae.prepare(candidates[0].parent)
            record['first_candidate'] = str(directory.relative_to(home))
            (home / 'run.json').write_text(json.dumps(record, indent=2))
        return 0
    if args.action == 'review-tests':
        from runtime_paths import first_candidate
        import approval_executor as ae
        ae.review(first_candidate())
    elif 'optimization' in args.action or args.action == 'prepare-failure':
        import optimization_step as opt
        if args.action == 'prepare-optimization':
            from dotenv import load_dotenv
            import asyncio
            load_dotenv(PROJECT / '.env')
            asyncio.run(opt.build())
        elif args.action == 'review-optimization':
            opt.ae.review(opt.HOME / 'candidate', validate_fn=opt.validate, execute_fn=opt.execute)
        else:
            import failure_demo as failure
            failure.prepare()
    else:
        import failure_demo as failure
        if args.action == 'replan':
            from dotenv import load_dotenv
            import asyncio
            load_dotenv(PROJECT / '.env')
            asyncio.run(failure.replan())
        else:
            phase = 'fault' if args.action == 'review-fault' else 'repair'
            failure.ae.review(failure.HOME / phase, validate_fn=failure.validate, execute_fn=failure.execute)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        reason = str(error)[:800] if isinstance(error, (ValueError, FileNotFoundError)) else 'Inspect the retained run evidence; no acceptance result is implied.'
        for name in ('GOOGLE_API_KEY', 'GEMINI_API_KEY'):
            value = os.environ.get(name)
            if value:
                reason = reason.replace(value, '[REDACTED]')
        reason = re.sub(r'AIza[\w-]+', '[REDACTED]', reason)
        print(json.dumps({'stopped': True, 'error_type': type(error).__name__, 'reason': reason}))
        sys.exit(1)
