"""Publish synthetic evaluation evidence without touching retained raw artifacts."""
import csv
import json
import math
from pathlib import Path
import shutil
import statistics

ROOT = Path(__file__).resolve().parents[1]


def main():
    target = ROOT / 'results'
    target.mkdir(exist_ok=False)
    comparison = ['# Parallel specialists versus single general reviewer', '',
        'Frozen manifest `730e71e27e42ee349bf02185a608d4c2add52ac0f4d0c6507351ed01e1e3ad70`, seed 505. '
        'Six development fixtures, six renamed held-out variants, four clean controls; three repeats each. '
        'There are 16 fixtures, not 48 independent fixtures per mode. Labels were frozen before evaluation and were not tuned.', '',
        '| Measure | Parallel specialists | Single reviewer |', '|---|---:|---:|']
    entries = {}
    for mode, folder in [('parallel','frozen-505-20261102'), ('single','single-505-20261102')]:
        original = ROOT / 'artifacts/evaluation' / folder
        destination = target / mode
        shutil.copytree(original, destination)
        summary = json.loads((original / 'summary.json').read_text())
        rows = [json.loads(line) for line in (original / 'runs.jsonl').read_text().splitlines()]
        usage = [u for path in original.glob('*.json') for u in json.loads(path.read_text()).get('usage_metadata', [])]
        totals = {key: sum(u.get(key) or 0 for u in usage) for key in
                  ('prompt_token_count','candidates_token_count','thoughts_token_count','total_token_count')}
        durations = sorted(r['active_seconds'] for r in rows)
        entries[mode] = {'completed': sum(r['status'] == 'complete' for r in rows),
            'failed': sum(r['status'] != 'complete' for r in rows), 'actual_call_responses_with_usage': len(usage),
            'usage_totals': totals, 'p50_seconds': statistics.median(durations),
            'p95_seconds': durations[math.ceil(.95*len(durations))-1],
            'held_out_macro_precision': summary['held_out']['macro_precision'],
            'held_out_macro_recall': summary['held_out']['macro_recall'],
            'control_unmatched_findings': sum(v['fp'] for v in summary['control']['categories'].values()),
            'total_active_seconds': sum(durations)}
        fields = ['case','split','repeat','status','active_seconds'] + [f'{c}_{k}' for c in
            ('security','performance','style','test_gap') for k in ('tp','fp','fn')]
        with (destination / 'metrics.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                flat = {key: row[key] for key in fields[:5]}
                flat.update({f'{c}_{k}': v for c, counts in row['counts'].items() for k, v in counts.items()})
                writer.writerow(flat)
        # Repair Markdown table layout in published copy only, retaining numeric content.
        report = (destination / 'REPORT.md').read_text()
        report = report.replace('\n\n| held_out', '\n\n| Split | Category | TP | FP | FN | Precision | Recall |\n|---|---|---:|---:|---:|---:|---:|\n| held_out')
        report = report.replace('\n\n| control', '\n\n| Split | Category | TP | FP | FN | Precision | Recall |\n|---|---|---:|---:|---:|---:|---:|\n| control')
        report += '\nPublication note: table formatting repaired; raw report retained locally. The single-reviewer comparison is in ../COMPARISON.md; original run metadata limits are preserved verbatim.\n'
        (destination / 'REPORT.md').write_text(report)
    for field in ('completed','failed','actual_call_responses_with_usage','held_out_macro_precision',
                  'held_out_macro_recall','control_unmatched_findings','p50_seconds','p95_seconds','total_active_seconds'):
        comparison.append(f'| {field} | {entries["parallel"][field]:.3f} | {entries["single"][field]:.3f} |')
    for key in entries['parallel']['usage_totals']:
        comparison.append(f'| {key} | {entries["parallel"]["usage_totals"][key]} | {entries["single"]["usage_totals"][key]} |')
    comparison.extend(['',
        'The single reviewer produced fewer unmatched findings and used fewer calls on this tiny corpus. '
        'Both modes missed the >=0.80 held-out precision target. Neither result supports a claim that '
        'four specialists improve accuracy. All 96 attempts completed without dropped runs or retries.', '',
        'Scores are provisional automatic category/symbol matches after exact source-line validation. '
        'Matching does not prove a finding is substantively correct. Sparse frozen labels may omit valid '
        'discoveries; all unmatched and duplicate findings count as FP in the original score. '
        'Human label review and blinded semantic adjudication remain pending; any amended score must be '
        'published alongside this original score. Clean-control alerts (especially test coverage/style) '
        'show over-reporting under the frozen rubric and require inspection.', '',
        'The model and temperature are identical. Each mode has an aggregate 8192 output-token ceiling '
        'per snapshot; specialists have four calls and separate role prompts, the baseline has one call '
        'and a combined prompt. Actual token usage differs; this is a matched maximum-output-budget '
        'comparison, not a matched monetary-cost experiment. Token metadata includes provider-reported '
        'thinking where supplied. Missing counts are not invented; no monetary estimate is available.', '',
        'Raw synthetic responses, source-linked evidence, spans, usage and per-run counts are included '
        'in each mode directory. metadata.json records environment, model alias, lock/prompt/harness hashes '
        'and the design-base Git revision. Source was locally uncommitted during execution; do not mistake '
        'the design-base revision for a commit containing the implementation. Original raw outputs remain '
        'under ignored artifacts/evaluation/. Reporting/packaging code was refined while the first run '
        'was in progress; the recorded invocation hashes identify the code used at launch.', '',
        '## Coverage and denominators', '',
        '- Live corpus reviews: 96 attempts, 96 complete; 192 specialist calls and 48 general-reviewer calls.',
        '- Authored corpus oracle verification: 16/16 original/corrected contract pairs; 32 container runs. '
        'Original SQL/tenant vulnerabilities intentionally fail hidden regression assertions; their corrected variants pass.',
        '- Authored test usefulness: 2/2 seeded mutants detected in two test-gap fixtures, using two additional container runs. '
        'These are harness-authored tests, not agent-authored test success.',
        '- Agent corpus patch attempts: 0. Accepted-patch behavior preservation, corpus approval integrity, '
        'corpus mutation trace completeness, corpus recovery and per-complete-case repair success are N/A.',
        '- Dependency/conflict fixture findings are evaluated; no corpus planning/DAG quality score or '
        'fixed-order non-replanning baseline is available. Separate planning and safety tests do not fill those denominators.',
        '- Original four human-approved operations and regression simulations remain separate evidence; '
        'there was no corpus approval simulator because no corpus edits were attempted.', '',
        'No held-out acceptance target, production safety certification or general performance speedup is claimed.'])
    (target / 'COMPARISON.md').write_text('\n'.join(comparison)+'\n')
    (target / 'comparison.json').write_text(json.dumps(entries, indent=2))
    oracle = ROOT / 'artifacts/evaluation/oracle-check-20261102'
    (target / 'oracles').mkdir()
    shutil.copyfile(oracle / 'fixtures.json', target / 'oracles/fixtures.json')
    for path in oracle.glob('*/*.log'):
        (target / 'oracles' / path.parent.name).mkdir(exist_ok=True)
        shutil.copyfile(path, target / 'oracles' / path.parent.name / path.name)


if __name__ == '__main__':
    main()
