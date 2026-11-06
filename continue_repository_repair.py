"""Prepare the next live plan step, or a fresh retry after failure; no approval granted."""
import argparse
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
import approval_executor as ae
from evaluation.end_to_end import run_tests
from evaluation.repository_end_to_end import propose_change
from repository_intake import digest
from repository_repair import RepairPlan, prepare, validate, write_json


async def continuation(previous, output):
    manifest = validate(previous)
    if manifest['mode'] != 'interactive':
        raise ValueError('Live continuation cannot use simulated evidence')
    bundle = json.loads((previous / 'bundle.json').read_text(encoding='utf-8'))
    ledger = ae.Ledger(previous / 'ledger.sqlite')
    try:
        operation = ledger.db.execute('SELECT * FROM operations WHERE binding=?', (ae.binding(manifest),)).fetchone()
        if not operation or operation['state'] not in {'VERIFIED', 'FAILED'}:
            raise ValueError('A completed personal approval and verification are required')
        outcome = json.loads(operation['result'])
    finally:
        ledger.db.close()
    plan = RepairPlan.model_validate(bundle['plan'])
    index = next(i for i,s in enumerate(plan.steps) if s.id == bundle['step_id'])
    completed = dict(bundle['completed'])
    files = json.loads(json.dumps(bundle['files']))
    failure = None
    if outcome['state'] == 'VERIFIED':
        # Reconstruct from approved inputs, never trust an editable export as the next parent.
        for change in bundle['proposal']['changes']:
            files[change['path']]['content'] = change['content']
            files[change['path']].pop('sha256', None)
            files[change['path']].pop('git_blob', None)
        completed[bundle['step_id']] = digest({'manifest': manifest, 'outcome': outcome})
        index += 1
        if index == len(plan.steps):
            return {'status': 'PLAN_COMPLETE', 'original_repository_unchanged': True}
    else:
        failure = {'test_counts': outcome['tests'], 'previous_proposal': bundle['proposal'],
                   'guidance': 'Failed proposal quarantined. Reconsider from unchanged step parent.'}
    output.mkdir(parents=True, exist_ok=False)
    baseline = run_tests(files, None, output / 'baseline')
    write_json(output / 'parent-evidence.json', {'directory': str(previous.resolve()), 'manifest': manifest, 'outcome': outcome})
    step = plan.steps[index]
    proposal = await propose_change(files, bundle['contracts'], plan, step, failure, output / 'author')
    prepare(output / 'candidate', files, bundle['contracts'], bundle['review'], plan, step.id, proposal,
            baseline, completed=completed, origin=bundle['origin'])
    return {'status': 'AWAITING_PERSONAL_TERMINAL_APPROVAL', 'candidate': str(output / 'candidate'), 'step': step.id}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous-candidate', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    load_dotenv()
    print(json.dumps(asyncio.run(continuation(args.previous_candidate, args.output)), indent=2))
