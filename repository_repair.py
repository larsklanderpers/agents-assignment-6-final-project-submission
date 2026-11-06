"""Bounded Python repair candidates: immutable inputs, terminal approval, offline tests.

No checkout is modified. Verified output is an export for subsequent human review.
"""
import argparse
import ast
import difflib
import getpass
import hashlib
import json
from pathlib import Path
import sys
import uuid

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
from pydantic import BaseModel
import approval_executor as ae
from evaluation.end_to_end import run_tests
from repository_intake import digest, freeze, safe_path, validate as validate_snapshot


class Step(BaseModel):
    id: str
    goal: str
    paths: list[str]
    depends_on: list[str]
    contract_ids: list[str]


class RepairPlan(BaseModel):
    rationale: str
    steps: list[Step]


class Change(BaseModel):
    path: str
    content: str


class RepairProposal(BaseModel):
    rationale: str
    changes: list[Change]


def validate_plan(plan, files, contracts):
    seen = {'baseline'}
    if not 1 <= len(plan.steps) <= 3:
        raise ValueError('One to three bounded steps required')
    for step in plan.steps:
        if not step.id or step.id in seen or not step.depends_on or not set(step.depends_on) <= seen:
            raise ValueError('Dependencies must identify prior completed steps or baseline')
        if not step.contract_ids or not set(step.contract_ids) <= set(contracts):
            raise ValueError('Unknown contract')
        if not 1 <= len(step.paths) <= 4 or len(set(step.paths)) != len(step.paths):
            raise ValueError('Select one to four distinct source files per step')
        for name in step.paths:
            safe_path(name)
            if name not in files or files[name]['role'] != 'source' or not name.endswith('.py'):
                raise ValueError('Only existing production Python files may change')
        seen.add(step.id)


def patch_for(proposal, step, files):
    if not proposal.changes or len({c.path for c in proposal.changes}) != len(proposal.changes):
        raise ValueError('Empty or duplicate changes')
    if set(c.path for c in proposal.changes) != set(step.paths):
        raise ValueError('Proposal must exactly match approved plan step scope')
    patches = []
    for change in sorted(proposal.changes, key=lambda c: c.path):
        old = files[change.path]['content']
        if len(change.content.encode()) > 32768:
            raise ValueError('Source too large')
        before, after = ast.parse(old), ast.parse(change.content)
        def api(tree):
            return [(n.name, ast.dump(n.args)) for n in ast.walk(tree)
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        def imports(tree):
            return sorted(ast.dump(n) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom)))
        if api(before) != api(after) or imports(before) != imports(after):
            raise ValueError('Function signatures and imports must remain unchanged')
        if old == change.content:
            raise ValueError('Every selected file must change')
        patches.append(''.join(difflib.unified_diff(old.splitlines(True), change.content.splitlines(True),
                       fromfile='a/' + change.path, tofile='b/' + change.path)))
    return ''.join(patches)


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2)


def freshness(origin):
    if not origin:
        return
    if origin['kind'] == 'local':
        current = freeze(origin['repo'], origin['revision'], origin['paths'])
        if current['commit'] != origin['commit'] or current['working_tree_changes_excluded']:
            raise ValueError('Repository changed or is dirty; prepare a new candidate')
    elif origin['kind'] == 'github_pr':
        from pr_intake import metadata
        current = metadata(origin['url'])
        if current['head'] != origin['head'] or current['base'] != origin['base'] or current['state'] != 'open':
            raise ValueError('PR base/head/state changed; prepare a new candidate')
    else:
        raise ValueError('Unknown repository origin')


def prepare(directory, files, contracts, review, plan, step_id, proposal, baseline,
            *, completed=None, origin=None, simulated=False, acceptance=None):
    if not 1 <= len(files) <= 40 or sum(len(f['content'].encode()) for f in files.values()) > 100000:
        raise ValueError('Executable selection exceeds 40 files / 100KB')
    for name in files:
        safe_path(name)
    if acceptance is not None and 'tests/test_acceptance.py' in files:
        raise ValueError('Private acceptance path would overwrite a supplied test')
    validate_plan(plan, files, contracts)
    step = next(s for s in plan.steps if s.id == step_id)
    completed = completed or {'baseline': digest(baseline)}
    if not set(step.depends_on) <= set(completed):
        raise ValueError('Dependencies not completed')
    if baseline.get('status') != 'passed':
        raise ValueError('Visible baseline must pass before proposing a repair')
    if not simulated and (not origin or acceptance is not None):
        raise ValueError('Live candidates require repository provenance and visible tests only')
    freshness(origin)
    patch = patch_for(proposal, step, files)
    bundle = {'files': files, 'contracts': contracts, 'review': review, 'plan': plan.model_dump(),
              'step_id': step_id, 'proposal': proposal.model_dump(), 'baseline': baseline,
              'completed': completed, 'origin': origin, 'acceptance': acceptance}
    identity = uuid.uuid4().hex
    manifest = {'schema': 1, 'kind': 'bounded_repository_repair', 'run_id': identity,
                'candidate_id': identity, 'mode': 'simulated' if simulated else 'interactive',
                'bundle_sha256': digest(bundle), 'patch_sha256': hashlib.sha256(patch.encode()).hexdigest(),
                'policy_sha256': digest(ae.POLICY), 'scope': step.paths}
    directory.mkdir(parents=True, exist_ok=False)
    write_json(directory / 'bundle.json', bundle)
    write_json(directory / 'manifest.json', manifest)
    (directory / 'candidate.patch').write_text(patch, encoding='utf-8', newline='')
    ledger = ae.Ledger(directory / 'ledger.sqlite')
    try:
        with SqliteSaver.from_conn_string(str(directory / 'checkpoint.sqlite')) as saver:
            ae.graph_for(directory, saver, ledger, 'pending', execute_fn=execute).invoke(
                {'candidate': manifest}, {'configurable': {'thread_id': identity}})
    finally:
        ledger.db.close()
    return manifest


def validate(directory):
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    bundle = json.loads((directory / 'bundle.json').read_text(encoding='utf-8'))
    if manifest['kind'] != 'bounded_repository_repair' or manifest['mode'] not in {'interactive', 'simulated'}:
        raise ValueError('Unsupported candidate')
    if digest(bundle) != manifest['bundle_sha256'] or digest(ae.POLICY) != manifest['policy_sha256']:
        raise ValueError('Candidate inputs or policy changed')
    plan = RepairPlan.model_validate(bundle['plan'])
    validate_plan(plan, bundle['files'], bundle['contracts'])
    step = next(s for s in plan.steps if s.id == bundle['step_id'])
    if not set(step.depends_on) <= set(bundle['completed']):
        raise ValueError('Unmet dependencies')
    patch = patch_for(RepairProposal.model_validate(bundle['proposal']), step, bundle['files'])
    if (patch.encode() != (directory / 'candidate.patch').read_bytes() or
            hashlib.sha256(patch.encode()).hexdigest() != manifest['patch_sha256'] or step.paths != manifest['scope']):
        raise ValueError('Exact patch binding changed')
    freshness(bundle['origin'])
    return manifest


def execute(directory, manifest, ledger, approval, actor, *, simulated=False):
    if validate(directory) != manifest or manifest['mode'] != ('simulated' if simulated else 'interactive'):
        raise ValueError('Candidate or approval mode mismatch')
    op = ledger.consume(approval, manifest, actor, simulated=simulated)
    if op['state'] in {'VERIFIED', 'FAILED'}:
        return json.loads(op['result'])
    if op['state'] != 'PREPARED':
        raise ValueError('Interrupted operation requires inspection; never replay automatically')
    ledger.update(op['id'], 'RUNNING')
    bundle = json.loads((directory / 'bundle.json').read_text(encoding='utf-8'))
    files = json.loads(json.dumps(bundle['files']))
    for change in bundle['proposal']['changes']:
        files[change['path']]['content'] = change['content']
        files[change['path']]['sha256'] = hashlib.sha256(change['content'].encode()).hexdigest()
        files[change['path']].pop('git_blob', None)
    try:
        tests = run_tests(files, bundle['acceptance'], directory / 'verification')
        outcome = {'state': 'VERIFIED' if tests['status'] == 'passed' else 'FAILED',
                   'operation_id': op['id'], 'tests': tests, 'mode': manifest['mode'],
                   'original_repository_unchanged': True}
        write_json(directory / ('verified-export.json' if outcome['state'] == 'VERIFIED' else 'quarantined-export.json'), files)
        write_json(directory / 'outcome.json', outcome)
        ledger.update(op['id'], outcome['state'], outcome)
        return outcome
    except BaseException as error:
        ledger.update(op['id'], 'AMBIGUOUS', {'error_type': type(error).__name__})
        raise


def simulate(directory):
    manifest = validate(directory)
    if manifest['mode'] != 'simulated':
        raise ValueError('Simulation cannot approve a live candidate')
    actor = 'evaluation-simulator-not-a-person'
    ledger = ae.Ledger(directory / 'ledger.sqlite')
    try:
        with ae.run_lock(directory), SqliteSaver.from_conn_string(str(directory / 'checkpoint.sqlite')) as saver:
            def run(*args): return execute(*args, simulated=True)
            graph = ae.graph_for(directory, saver, ledger, actor, execute_fn=run)
            config = {'configurable': {'thread_id': manifest['run_id']}}
            if graph.get_state(config).next != ('gate',):
                raise ValueError('Simulation already started')
            grant = ledger.decision(manifest, actor, 'approve', simulated=True)
            graph.invoke(Command(resume=grant), config)
            return graph.get_state(config).values['outcome']
    finally:
        ledger.db.close()


def review(directory):
    if not sys.stdin.isatty():
        raise ValueError('Personal terminal decision required; no piped approval')
    with ae.run_lock(directory), SqliteSaver.from_conn_string(str(directory / 'checkpoint.sqlite')) as saver:
        manifest = validate(directory)
        if manifest['mode'] != 'interactive':
            raise ValueError('This is an evaluation candidate, not a live approval')
        bundle = json.loads((directory / 'bundle.json').read_text(encoding='utf-8'))
        actor = getpass.getuser()
        ledger = ae.Ledger(directory / 'ledger.sqlite')
        try:
            graph = ae.graph_for(directory, saver, ledger, actor, execute_fn=execute)
            config = {'configurable': {'thread_id': manifest['run_id']}}
            state = graph.get_state(config)
            if state.values.get('candidate') != manifest:
                raise ValueError('Checkpoint mismatch')
            if state.values.get('outcome'):
                print(json.dumps(state.values['outcome'], indent=2)); return
            if state.next != ('gate',):
                raise ValueError('Operation interrupted; inspect retained evidence')
            prior = ledger.db.execute('SELECT decision FROM decisions ORDER BY rowid DESC LIMIT 1').fetchone()
            if prior and prior['decision'] in {'reject', 'redirect', 'cancel'}:
                raise ValueError('New candidate required after rejection, redirection or cancellation')
            ae.preflight()
            print('BOUNDED REPOSITORY REPAIR — PERSONAL DECISION')
            print(json.dumps({'origin': bundle['origin'], 'plan': bundle['plan'], 'step': bundle['step_id'],
                              'baseline': bundle['baseline'], 'policy': ae.POLICY}, indent=2))
            print((directory / 'candidate.patch').read_text(encoding='utf-8'))
            print('Approval tests this exact patch in offline Docker. No checkout changes, pushes or merges.')
            print('Passing visible tests is not proof of full correctness. Evidence:', directory)
            expected = 'approve ' + manifest['patch_sha256'][:12]
            choice = input(expected + ' | reject | redirect | defer | cancel: ').strip()
            decision = 'approve' if choice == expected else choice
            if decision not in {'approve', 'reject', 'redirect', 'defer', 'cancel'} or choice == 'approve':
                raise ValueError('Unrecognized decision')
            comment = input('New constraints: ').strip() if decision == 'redirect' else ''
            if decision == 'redirect' and not comment:
                raise ValueError('Constraints required')
            if validate(directory) != manifest:
                raise ValueError('Candidate changed while waiting')
            grant = ledger.decision(manifest, actor, decision, comment)
            if decision == 'approve':
                graph.invoke(Command(resume=grant), config)
                print(json.dumps(graph.get_state(config).values['outcome'], indent=2))
            else:
                print('Recorded:', decision)
        finally:
            ledger.db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['review', 'validate'])
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    if args.action == 'review': review(args.directory)
    else: print(json.dumps(validate(args.directory), indent=2))
