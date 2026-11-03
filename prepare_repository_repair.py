"""Review and prepare the FIRST bounded repository step; never grant approval."""
import argparse
import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv
from evaluation.end_to_end import run_tests
from evaluation.repository_end_to_end import propose_plan, propose_change
from repository_review import review_repository
from repository_intake import freeze, validate
from repository_repair import prepare, validate_plan, write_json


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--repo', type=Path)
    source.add_argument('--pr-intake', type=Path)
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--path', action='append', dest='paths')
    parser.add_argument('--contracts', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    load_dotenv()
    if args.repo:
        snapshot = freeze(args.repo, args.revision, args.paths)
        if snapshot['working_tree_changes_excluded']:
            raise ValueError('Live preparation requires a clean source checkout')
        origin = {'kind': 'local', 'repo': str(args.repo.resolve()), 'revision': args.revision,
                  'paths': list(snapshot['files']), 'commit': snapshot['commit']}
    else:
        snapshot = validate(json.loads((args.pr_intake / 'snapshot.json').read_text(encoding='utf-8')))
        origin = json.loads((args.pr_intake / 'origin.json').read_text(encoding='utf-8'))
        if snapshot['commit'] != origin['head'] or snapshot['base_commit'] != origin['base']:
            raise ValueError('PR provenance mismatch')
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output / 'snapshot.json', snapshot)
    contracts = json.loads(args.contracts.read_text(encoding='utf-8'))
    baseline = run_tests(snapshot['files'], None, args.output / 'baseline')
    if baseline['status'] != 'passed':
        raise ValueError('Selected stdlib unittest baseline must pass; retained diagnostics explain failure')
    review = await review_repository(snapshot['files'], contracts, args.output / 'review')
    if not review['accepted_defects']:
        write_json(args.output / 'result.json', {'status': 'no_supported_findings', 'approval_required': False})
        return
    plan = await propose_plan(snapshot['files'], contracts, review, baseline, args.output / 'planner')
    validate_plan(plan, snapshot['files'], contracts)
    write_json(args.output / 'plan.json', plan.model_dump())
    step = plan.steps[0]
    proposal = await propose_change(snapshot['files'], contracts, plan, step, None, args.output / 'author')
    manifest = prepare(args.output / 'candidate', snapshot['files'], contracts, review, plan, step.id,
                       proposal, baseline, origin=origin)
    print(json.dumps({'status': 'AWAITING_PERSONAL_TERMINAL_APPROVAL', 'candidate': str(args.output / 'candidate'),
                      'scope': manifest['scope'], 'later_steps': len(plan.steps)-1}, indent=2))


if __name__ == '__main__': asyncio.run(main())
