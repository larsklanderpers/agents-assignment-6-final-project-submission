"""Verify original/corrected corpus oracles in the pinned offline container."""
import argparse
import json
import os
from pathlib import Path

import approval_executor as ae
from evaluation.run import sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    manifest = Path('evaluation/manifest.json')
    if sha(manifest) != manifest.with_suffix('.sha256').read_text().strip():
        raise ValueError('Frozen corpus changed')
    ae.preflight()
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    policy = dict(ae.POLICY, minimum_candidate_tests=1)
    rows = []
    for case in json.loads(manifest.read_text())['cases']:
        directory = output / case['id']
        (directory / 'tests').mkdir(parents=True)
        (directory / ae.TARGET).write_bytes(case['hidden_tests'].encode())
        ae.git(directory, 'init', '--initial-branch=main')
        row = {'case': case['id'], 'change_kind': case['change_kind']}
        for phase, field in [('original','source'), ('corrected','corrected')]:
            (directory / ae.SOURCE).write_bytes(case[field].encode())
            ae.git(directory, 'add', '--', ae.SOURCE, ae.TARGET)
            ae.git(directory, '-c', 'user.name=Review Ledger Corpus', '-c',
                   'user.email=corpus@example.invalid', 'commit', '--allow-empty', '-m', phase)
            row[phase + '_commit'] = ae.git(directory, 'rev-parse', 'HEAD').decode().strip()
            row[phase + '_tree'] = ae.git(directory, 'rev-parse', 'HEAD^{tree}').decode().strip()
            row[phase] = ae.container_check(directory, directory / (phase + '.log'), policy=policy)
        expected_original = 'failed' if case['change_kind'] == 'intentional_fix' else 'passed'
        row['oracle_contract_pass'] = row['original']['status'] == expected_original and row['corrected']['status'] == 'passed'
        if case['family'] == 'test_gap':
            (directory / ae.SOURCE).write_bytes(case['source'].replace('else None', 'else 0').encode())
            row['seeded_mutant'] = ae.container_check(directory, directory / 'mutant.log', policy=policy)
            row['oracle_contract_pass'] &= row['seeded_mutant']['status'] == 'failed'
            (directory / ae.SOURCE).write_bytes(case['corrected'].encode())
        rows.append(row)
        (output / 'fixtures.json').write_text(json.dumps(rows, indent=2))
        print(json.dumps({'case': row['case'], 'oracle_contract_pass': row['oracle_contract_pass']}), flush=True)
    if not all(r['oracle_contract_pass'] for r in rows):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
