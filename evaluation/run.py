"""Execute frozen finding evaluation; no proposals, approvals or host test execution."""
import argparse
import ast
import asyncio
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import statistics
import subprocess
import time

from dotenv import load_dotenv
from spike_live import review_source

PROJECT = Path(__file__).resolve().parents[1]
CATEGORIES = ('security', 'performance', 'style', 'test_gap')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def symbol_at(source, line):
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.lineno <= line <= node.end_lineno:
            return node.name
    return '<module>'


def score(case, result):
    unmatched = list(case['labels'])
    counts = {category: {'tp': 0, 'fp': 0, 'fn': 0} for category in CATEGORIES}
    for review in result.get('reviews', {}).values():
        for finding in review['findings']:
            label = {'category': finding['category'], 'symbol': symbol_at(case['source'], finding['line'])}
            if label in unmatched:
                unmatched.remove(label)
                counts[label['category']]['tp'] += 1
            else:
                counts[label['category']]['fp'] += 1
    for label in unmatched:
        counts[label['category']]['fn'] += 1
    return counts


def summarize(cases, rows):
    summaries = {}
    for split in ('development', 'held_out', 'control'):
        selected = [r for r in rows if r['split'] == split]
        totals = {c: {k: sum(r['counts'][c][k] for r in selected) for k in ('tp','fp','fn')} for c in CATEGORIES}
        for c in CATEGORIES:
            t = totals[c]
            t['precision'] = t['tp'] / (t['tp'] + t['fp']) if t['tp'] + t['fp'] else None
            t['recall'] = t['tp'] / (t['tp'] + t['fn']) if t['tp'] + t['fn'] else None
        summaries[split] = {'fixtures': sum(c['split'] == split for c in cases), 'runs': len(selected),
            'failed_runs': sum(r['status'] != 'complete' for r in selected), 'categories': totals,
            'macro_precision': statistics.mean(v['precision'] for v in totals.values() if v['precision'] is not None) if any(v['precision'] is not None for v in totals.values()) else None,
            'macro_recall': statistics.mean(v['recall'] for v in totals.values() if v['recall'] is not None) if any(v['recall'] is not None for v in totals.values()) else None}
    return summaries


async def evaluate(args):
    reviewer = review_source
    if args.mode == 'single':
        from evaluation.single_reviewer import review_source as reviewer
    manifest = Path(args.manifest)
    if sha(manifest) != manifest.with_suffix('.sha256').read_text().strip():
        raise ValueError('Frozen manifest digest differs')
    corpus = json.loads(manifest.read_text())
    if args.seed != corpus['seed'] or args.repeats < 1:
        raise ValueError('Use frozen seed 505 and positive repeats')
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    load_dotenv(PROJECT / '.env')
    meta = {'manifest_sha256': sha(manifest), 'seed': args.seed, 'repeats': args.repeats,
        'mode': args.mode, 'approval_actor': 'none; no patches attempted',
        'python': platform.python_version(), 'platform': platform.platform(), 'cpu': platform.processor(),
        'model': os.environ.get('REVIEW_LEDGER_MODEL'), 'lock_sha256': sha(PROJECT / 'requirements-spike.lock'),
        'reviewer_code_and_prompt_sha256': sha(PROJECT / 'spike_live.py'),
        'harness_sha256': sha(Path(__file__)),
        'single_baseline_code_sha256': sha(PROJECT / 'evaluation/single_reviewer.py'),
        'git_revision': subprocess.run(['git','rev-parse','HEAD'], cwd=PROJECT, capture_output=True, text=True).stdout.strip(),
        'sampling': {'temperature': 0, 'max_output_tokens_per_specialist': 2048},
        'limitations': ['Category/symbol matching is automatic; semantic evidence adjudication pending.',
            'Labels are original machine-authored, frozen before evaluation; independent human label review pending.',
            'Held-out variants are small renamed variants, not an independent external dataset.',
            'No corpus patch/planning/baseline comparison is measured; behavior and approval metrics N/A.',
            'Dependency/conflict are fixture families scored by test_gap/security finding category only.',
            'No calibrated pricing: cost unknown; failures may incur unreported provider usage.']}
    (output / 'metadata.json').write_text(json.dumps(meta, indent=2))
    rows = []
    for case in corpus['cases']:
        for repeat in range(1, args.repeats + 1):
            started = time.monotonic()
            row = {'case': case['id'], 'split': case['split'], 'repeat': repeat}
            try:
                result = await reviewer(case['source'], case['visible_tests'])
                row.update(status='complete', counts=score(case, result))
                (output / f'{case["id"]}-{repeat}.json').write_text(json.dumps(result, indent=2))
            except Exception as error:
                row.update(status='failed', error_type=type(error).__name__,
                    http_code=getattr(error, 'code', None), counts=score(case, {}))
            row['active_seconds'] = round(time.monotonic() - started, 3)
            rows.append(row)
            with (output / 'runs.jsonl').open('a') as stream:
                stream.write(json.dumps(row) + '\n')
            print(json.dumps({k: row[k] for k in ('case','repeat','status','active_seconds')}), flush=True)
    summary = summarize(corpus['cases'], rows)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2))
    with (output / 'runs.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['case','split','repeat','status','active_seconds'])
        writer.writeheader()
        writer.writerows({k: r[k] for k in writer.fieldnames} for r in rows)
    report = ['# Frozen corpus finding evaluation', '',
        f'Manifest SHA256: `{meta["manifest_sha256"]}`. Seed 505. {len(rows)} runs; 16 fixtures.', '',
        'These are automatic category/symbol matches with exact source-line validation, pending semantic human adjudication.', '',
        '| Split | Category | TP | FP | FN | Precision | Recall |', '|---|---|---:|---:|---:|---:|---:|']
    fmt = lambda value: 'N/A' if value is None else f'{value:.3f}'
    for split, entry in summary.items():
        for category, values in entry['categories'].items():
            report.append(f'| {split} | {category} | {values["tp"]} | {values["fp"]} | {values["fn"]} | {fmt(values["precision"])} | {fmt(values["recall"])} |')
    for split, entry in summary.items():
        report.extend(['', f'{split}: {entry["fixtures"]} fixtures, {entry["runs"]} runs, {entry["failed_runs"]} failed. Macro precision {fmt(entry["macro_precision"])}, recall {fmt(entry["macro_recall"])}.', ''])
    durations = sorted(r['active_seconds'] for r in rows)
    report.extend([f'Active review latency p50: {statistics.median(durations):.3f}s; p95 nearest rank: {durations[max(0, __import__("math").ceil(.95*len(durations))-1)]:.3f}s.', '',
        f'All attempts and failures are in runs.jsonl; no automatic retries or dropped repeats. Mode: {args.mode}. Complete parallel reviews use four calls; single-reviewer baseline uses one call with the same 8192 aggregate output-token limit. Token metadata is retained per response; monetary cost is unknown.', '',
        '## Limits', '', *['- '+s for s in meta['limitations']], '',
        'No acceptance target is claimed met from these provisional scores. Frozen labels were not modified after seeing outputs. Unsupported or duplicate category/symbol matches count as FP; missing outputs count as FN. Zero denominators are N/A.', '',
        'Corpus patch attempts: 0. Behavior preservation, mutation-test usefulness, trace completeness for corpus mutations and corpus recovery: N/A. See separate verified human operations and safety regression tests; those are not corpus outcomes.'])
    (output / 'REPORT.md').write_text('\n'.join(report) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default='evaluation/manifest.json')
    parser.add_argument('--seed', type=int, default=505)
    parser.add_argument('--repeats', type=int, default=3)
    parser.add_argument('--output', required=True)
    parser.add_argument('--mode', choices=['parallel', 'single'], default='parallel')
    asyncio.run(evaluate(parser.parse_args()))


if __name__ == '__main__':
    main()
