# Guided dress rehearsal — 3 November 2026

Fresh run: **`thursday-dress-20261103-01`**.
Completed run `packaging-rehearsal-20261102` and original historical runs remain
saved fallback evidence. This dress-rehearsal run will be consumed by rehearsal;
prepare another unique run for the live Thursday segment after rehearsal passes.

## Preparation and approval schedule

Fresh four-agent reviews completed with overlapping execution, the new plan
passed validation, and exactly seven new characterization tests were authored.
The exact proposal passed seven tests in a **separate simulated** Docker
verification. This did not approve or execute the real candidate.

### Approval 1 — completed during preparation

```powershell
.venv\Scripts\python.exe review_ledger.py review-tests --run thursday-dress-20261103-01
```

Candidate `candidate-7da399bfc64b-exec-v1` is now VERIFIED under real interactive
approval, operation `eae1ddf125954a0ea3565538bd2f80b3`: seven tests passed. Its
binding and both log hashes were checked. The original approval is consumed;
reopening `review-tests` shows saved evidence. The timer has not started.

After that real result, Codex checks the saved evidence and prepares this run's
optimization proposal and deliberate failure gate. **No optimization approval is
needed for this short stage route**; its prepared candidate supplies the reviewed
snapshot/provenance needed by the independent negative-case branch. The completed
prior optimization may be shown as explicitly saved evidence.

### Approval 2 — about 2:20 into the timed segment

The pending fault gate must be prepared before starting the stopwatch. At the
cue below, run `review-fault` for this run, inspect the disclosed intentionally
incorrect set-conversion diff, and enter its **then-displayed** approval prefix
only if accepted. Expected outcome: FAILED, nested-list TypeError, quarantine.
Prepared candidate: `demo-fault-e292e414e1`. Its displayed decision text is
**`approve 99d40a18b4f6`**. Use this only with the currently selected fresh run.
Identical patch bytes can have the same hash as another run; the old approval
grant cannot transfer because its run, parent and plan bindings differ.

At the 2:20 cue:

```powershell
.venv\Scripts\python.exe review_ledger.py review-fault --run thursday-dress-20261103-01
```

The exact negative-case proposal passed its independent expected-failure check in
a separately simulated fixture. The real fault ledger remains unapproved.

### Approval 3 — about 5:10, after actual replanning

Run this run's live `replan` against its actual failed logs, then `review-repair`.
Inspect the newly authored patch, version-4 plan and verified parent. Enter its
new displayed approval prefix only if accepted. Expected acceptance: seven tests
plus thirteen checks. Do not reuse the fault grant or a saved repair's prefix.

Approve only after personal review. Rejection, deferral or cancellation is a valid
decision; it does not execute the step. Tell the coach the actual outcome rather
than advancing the script as though approval occurred.

## Before starting the clock

Wait until Codex confirms that the new fault gate is pending and checks the new
proposal's expected failure independently. Open the diagram, prepared reviews,
ranked plan, corpus comparison and saved fallback summary. Use readable text and
keep credentials out of view. Tell the coach when those screens are ready.

Use a stopwatch or recording timestamps. Start at the first spoken sentence and
stop at the last; include human waiting, model/tool latency and any chat coaching
delay. The target is **9:30**, maximum **10:00**. A partial walkthrough or estimated
word count does not establish the full duration. If coached chat pauses exceed
the limit, record that honestly, then do an uninterrupted timed take afterward.

## Timed cue sheet

| Clock | Say/show | Approval/action |
|---|---|---|
| 0:00–0:45 | “Review Ledger proposes code changes with evidence. Human approval gates every edit. This is a bounded Python prototype.” Show diagram and ADK/LangGraph roles. | No approval |
| 0:45–1:35 | Show four prepared reviews and source-line evidence. “These reviews were generated during preparation; their agreement is not proof.” | No approval |
| 1:35–2:20 | Show DAG and VERIFIED characterization. “Readiness means eligible to propose. A score cannot authorize execution.” | No approval |
| 2:20–3:10 | Show disclosed faulty diff. “This deliberately incorrect proposal is isolated on its own branch and is not for adoption.” | **Approval 2:** `review-fault`; inspect and decide |
| 3:10–4:00 | Show actual TypeError, FAILED outcome and quarantine. Explain the failed hashability assumption. | Report actual result |
| 4:00–5:10 | Run live `replan`. Show plan 3 → 4, failed action deferred and descendant redirected to repair. | No patch approval during planning |
| 5:10–6:25 | Show new guarded repair diff and last VERIFIED parent. “The old grant cannot authorize this new patch.” | **Approval 3:** `review-repair`; inspect and decide |
| 6:25–7:10 | Show actual repair result, tests and thirteen comparisons. Timing applies only to the integer fixture and uses extra memory. | If not VERIFIED, state the real outcome |
| 7:10–8:05 | Show bindings/ledger and checkpoint evidence. “A consumed grant cannot apply another patch. The follow-up is eligible only for proposal.” | No follow-up approval |
| 8:05–9:05 | Corpus: 16 fixtures, three repeats; parallel precision 0.411 versus single reviewer 0.510, recall 1.000. Explain provisional matching, over-reporting and missing corpus-repair coverage. | No approval |
| 9:05–9:30 | Tradeoffs: two frameworks add integration cost; model-generated tests and plans still need independent checks. State next work. | Stop timer at final sentence |

During a coached pass, report your stopwatch time and the actual operation result
at the failure and repair checkpoints. Never omit waiting from the total or call
a saved result live. If a model stalls more than the 45-second stage budget,
state it and switch explicitly to the completed saved case. At 8:30 with tools
still pending, use the saved fallback and close before the ceiling.

## Rehearsal record — fill from observations

| Field | Actual |
|---|---|
| Setup test approval | VERIFIED: eae1ddf125954a0ea3565538bd2f80b3; seven passes |
| Fault gate ready before timer | Prepared and independently checked; real ledger has no approval/operation |
| First sentence time | Not started |
| Fault decision/outcome and elapsed time | Not started |
| Repair decision/outcome and elapsed time | Not started |
| Last sentence / total elapsed | Not measured |
| Live / prepared / saved sections | Record during run |
| <=10:00 full take | Not established |
| Recording location/link | Not recorded |

Full operating details and error routes remain in DEMO-RUNBOOK.md. Edit the
reflection through the verified link in REFLECTION-WORKING-COPY.md; it is an
editable copy, not an automatic mirror of the local file.

## Coaching entry point

Open this cue sheet, the architecture diagram, the new run's review/plan evidence,
and the published corpus comparison. Have a stopwatch ready. Tell the coach
"ready to start" once those screens are available. Start the stopwatch only at
the explicit 0:00 speaking cue. The coach will advance the opening cues at 0:45,
1:35 and 2:20. At the fault checkpoint report the real outcome and your elapsed
time; the next phase uses only that actual failure for replanning.
