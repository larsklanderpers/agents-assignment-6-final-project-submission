"""Verify a corrected proposal in simulation BEFORE creating a new human gate.

No real approval is entered, copied or consumed here. Existing terminal attempts
are read-only inputs. The simulated ledger and real Docker logs are retained.
"""
import argparse
import difflib
import json
import os
from pathlib import Path
import sqlite3
import uuid

from review_ledger import run_home
from proposal_checks import validate_collection_examples


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', required=True)
    parser.add_argument('--content-file', type=Path, required=True)
    parser.add_argument('--reason', required=True)
    args = parser.parse_args()
    home = run_home(args.run)
    os.environ['REVIEW_LEDGER_RUN_HOME'] = str(home)
    import approval_executor as ae
    from runtime_paths import first_candidate
    previous = first_candidate()
    manifest = ae.validate(previous)
    with sqlite3.connect((previous / 'ledger.sqlite').as_uri() + '?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        rows = [dict(r) for r in db.execute('SELECT * FROM operations')]
    if len(rows) != 1 or rows[0]['state'] != 'FAILED':
        raise ValueError('Correction requires one recorded FAILED operation; nothing is overwritten')
    failed = rows[0]
    old_result = json.loads(failed['result'])
    old_operation, _, _ = ae.operation_paths(previous, failed['id'])
    log_hash = ae.digest((old_operation / 'candidate.log').read_bytes())
    if log_hash != old_result['candidate']['log_sha256']:
        raise ValueError('Failed test log hash changed')
    content = (args.content_file.read_text(encoding='utf-8').replace('\r\n', '\n').rstrip() + '\n').encode()
    checks = validate_collection_examples(content.decode('utf-8'))
    patch = ''.join(difflib.unified_diff([], content.decode().splitlines(keepends=True),
        fromfile='/dev/null', tofile='b/' + ae.TARGET)).encode()
    if ae.patch_content(patch) != content or ae.digest(patch) == manifest['patch_sha256']:
        raise ValueError('A changed, allowlisted test proposal is required')
    ae.preflight()
    identity = uuid.uuid4().hex[:12]
    verification = home / 'artifacts' / ('check-' + identity)
    verification.mkdir()
    base = verification / 'base'
    source_base = home / 'artifacts/first-patch/baseline'
    ae.git(source_base, 'clone', '--no-hardlinks', str(source_base), str(base))
    if ae.git(base, 'rev-parse', 'HEAD').decode().strip() != manifest['parent_commit']:
        raise ValueError('Simulation parent does not match the reviewed parent')
    candidate = verification / 'candidate'
    candidate.mkdir()
    (candidate / 'candidate.patch').write_bytes(patch)
    simulated = dict(manifest, candidate_id='simulated-' + identity, run_id='simulated-' + identity,
        patch_sha256=ae.digest(patch), new_file_sha256=ae.digest(content))
    (candidate / 'manifest.json').write_text(json.dumps(simulated, indent=2), encoding='utf-8')
    ledger = ae.Ledger(candidate / 'ledger.sqlite')
    try:
        grant = ledger.decision(simulated, 'explicit-test-simulator', 'approve', simulated=True)

        def validate_simulation(directory):
            if ae.patch_content((directory / 'candidate.patch').read_bytes()) != content:
                raise ValueError('Simulation test bytes changed')
            if ae.git(base, 'rev-parse', 'HEAD^{tree}').decode().strip() != manifest['parent_tree_hash']:
                raise ValueError('Simulation parent tree changed')
            return simulated

        outcome = ae.execute(candidate, simulated, ledger, grant, 'explicit-test-simulator', simulated=True,
            validate_fn=validate_simulation, baseline_repo=base)
    finally:
        ledger.db.close()
    report = {'mode': 'simulated_preapproval_test_verification', 'real_approval_issued': False,
        'failed_candidate': manifest['candidate_id'], 'failed_operation': failed['id'],
        'failed_log_sha256': log_hash, 'corrected_patch_sha256': ae.digest(patch),
        'corrected_content_sha256': ae.digest(content), 'literal_checks': checks,
        'outcome': outcome, 'reason': args.reason}
    report_path = verification / 'verification.json'
    report_path.write_text(json.dumps(report, indent=2), encoding='utf-8')
    if outcome['state'] != 'VERIFIED':
        raise ValueError('Corrected tests did not pass; no human gate was prepared')
    # Only after real container verification, create an independent unapproved gate.
    original = home / 'artifacts/first-patch' / ('candidate-' + identity)
    original.mkdir()
    corrected = dict(manifest, candidate_id=original.name, run_id=original.name,
        patch_sha256=ae.digest(patch), new_file_sha256=ae.digest(content), model=None,
        original_author_model=manifest.get('model'), proposal_origin='developer_corrected_expectation',
        rationale=args.reason, approval_status='pending', execution_authorized=False,
        correction_of={'candidate': manifest['candidate_id'], 'operation': failed['id'],
                       'failed_log_sha256': log_hash},
        preapproval_verification={'mode': report['mode'], 'path': str(report_path.relative_to(home)),
                                 'sha256': ae.digest(report_path.read_bytes())},
        checks={'python_syntax': 'pass', 'literal_examples': checks,
                'independent_simulated_tests': str(outcome['evidence']['candidate']['tests']) + ' passed in Docker',
                'human_run_execution': 'not_run'})
    (original / 'candidate.patch').write_bytes(patch)
    (original / 'manifest.json').write_text(json.dumps(corrected, indent=2), encoding='utf-8')
    directory = ae.prepare(original)
    record = json.loads((home / 'run.json').read_text())
    if home / record['first_candidate'] != previous:
        raise ValueError('Selected candidate changed; new gate retained but not selected')
    record.setdefault('prior_first_candidates', []).append(record['first_candidate'])
    record['first_candidate'] = str(directory.relative_to(home))
    (home / 'run.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps({'verification': str(report_path), 'outcome': outcome['state'],
        'new_pending_candidate': directory.name, 'patch_sha256': ae.digest(patch),
        'approval_command': 'approve ' + ae.digest(patch)[:12]}))


if __name__ == '__main__':
    main()
