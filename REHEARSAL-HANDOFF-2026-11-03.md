# New-context handoff — timed rehearsal ready, clock NOT started

## Active user request and immediate next step

Lars requested: prepare a fresh run for Thursday 5 November 2026, coach a timed
presentation/demo, preserve verified history, identify every human approval, and
provide an editable Google Drive reflection. He then requested this handoff.

**Setup is complete. The timer has NOT started.** The last instruction was to
open the cue sheet, have a stopwatch ready and say **“ready to start.”** Lars has
not yet said that. Do not repeat setup, regenerate reviews, request the completed
test approval again, or approve the pending fault before its timed cue.

Project: `C:\vc-personal-projects\continuing-education\agents-assignment-6-final-project-submission`.
Shell: PowerShell. Timezone: Australia/Sydney; current local date 3 November.
Presentation: **Thursday 5 November 2026**. Canvas deadline is separately unconfirmed.

Read this file first, then REHEARSAL-SESSION-2026-11-03.md. DEMO-RUNBOOK.md contains
the full speaking/operator script. Earlier handoffs have chronological pending
states which are superseded by this handoff and the current ledgers.

## Fresh active dress-rehearsal run — verified at handoff

Run ID: **`thursday-dress-20261103-01`**.
All its artifacts: `artifacts/runs/thursday-dress-20261103-01/`.

- Fresh four-agent reviews completed, overlapping execution observed.
- Fresh plan validated and seven new characterization tests authored.
- Those exact tests passed a separately simulated Docker preflight, then Lars
  personally approved the real gate. Real operation
  **`eae1ddf125954a0ea3565538bd2f80b3` is VERIFIED**, seven tests passed.
- Test candidate: `candidate-7da399bfc64b-exec-v1`. Its approval is consumed.
  Original patch prefix `2c21598cb9cd` is history, not a pending decision.
- Optimization proposal `lookup-9db457dfc447` is prepared, **not approved or
  executed**. No optimization approval is required for this short stage route;
  its reviewed snapshot and prepared candidate support the independent fault
  branch. Do not add an unnecessary approval here.
- Real fault candidate: **`demo-fault-e292e414e1`**, plan 3. Its real ledger has
  **zero decisions and zero operations**. It is ready for the timed fault gate.
- Fault patch SHA256:
  `99d40a18b4f6c4ec58f633b1951dc9ef3d95f98d55f2b9d625f40702fb55ecee`.
  Its displayed approval text is **`approve 99d40a18b4f6`**.
- An independent simulated preflight confirmed seven tests, one expected
  nested-list TypeError, zero assertion failures and quarantine. Report:
  `artifacts/failure-demo/preflight-fault-e5f0463b/verification.json` beneath the
  new run. This does not constitute real approval or actual fault execution.
- State records: `rehearsal-session.json` and `preparation-audit.json` at run root.
  Current status: `ready_for_timed_rehearsal_waiting_for_user_start`;
  `timer_started: false`; actual duration is null.

Inspect read-only state if needed:

```powershell
.venv\Scripts\python.exe review_ledger.py status --run thursday-dress-20261103-01
```

Status also lists explicitly named simulated candidates. Do not confuse their
VERIFIED/FAILED states with real interactive decisions. The real candidate IDs
above and ledger decision `mode=interactive` distinguish the claims.

## Coach the rehearsal, then prepare a separate Thursday run

First check that Lars has the cue sheet, diagram, prepared review/plan evidence,
corpus comparison and stopwatch ready. When he says ready, give the explicit
**0:00 speaking cue** and have him start the stopwatch at the first sentence.
Do not silently start timing while he is opening windows. Record a coach start
timestamp if useful; the actual stopwatch/recording duration is authoritative.

Opening cue: “Review Ledger proposes code changes with evidence. Human approval
gates every edit. This is a bounded Python prototype.” Show the diagram and
ADK/LangGraph roles. The user speaks the presentation; do not claim to hear or
measure speech that was not supplied.

| Cue | Action |
|---|---|
| 0:45 | Four prepared reviews and exact source-line evidence; label them prepared |
| 1:35 | DAG, VERIFIED characterization, readiness versus authorization |
| **2:20** | **Human approval 2**, disclosed intentionally faulty patch |
| 3:10 | Actual FAILED outcome, nested-list TypeError and quarantine |
| 4:00 | Live replan using this run's actual failure log; plan 3 → 4 |
| **About 5:10** | **Human approval 3**, new repair after real replanning |
| 6:25 | Actual repair outcome, seven tests plus thirteen comparisons |
| 7:10 | Ledger/checkpoint/binding chain; follow-up eligibility is not permission |
| 8:05 | Actual corpus comparison and limitations |
| 9:05–9:30 | Tradeoffs and closing; stop stopwatch at final sentence |

For automatic opening cue pacing, use clock tools and bounded waits of <=60
seconds so the user can interrupt. Do not fabricate elapsed time or a passed
rehearsal. Include human waiting, model/tool latency and chat coaching delay.
If a coached pass exceeds ten minutes, record it and do an uninterrupted take
afterward. Target 9:30, ceiling 10:00. At 8:30 with tools still pending, switch
explicitly to saved fallback and close; do not call saved results live.

### At the 2:20 cue — real human fault decision

```powershell
.venv\Scripts\python.exe review_ledger.py review-fault --run thursday-dress-20261103-01
```

Lars inspects the displayed diff/candidate and personally enters
`approve 99d40a18b4f6` if accepted. Expected real outcome is FAILED with a
nested-list TypeError. This is a deliberately incorrect disposable proposal,
not adoption of bad code. Ask for actual outcome and stopwatch time at the
checkpoint using the user-input tool if needed. Do not tool-enter an approval.

Identical patch bytes can have the same hash in different runs. An old grant
still cannot transfer: run, candidate, parent, plan and policy bindings differ.

### After that actual failure — live replan and new repair

Verify the real interactive decision, log hash and quarantine, then:

```powershell
.venv\Scripts\python.exe review_ledger.py replan --run thursday-dress-20261103-01
```

Use only this run's actual failure, not its simulated preflight or the completed
fallback run. Inspect `current-plan.json`, `replanning-evidence.json`, raw
`replan-attempts/` and the new repair diff. Check stale-grant rejection and that
the follow-up remains blocked until the real repair is VERIFIED. Independently
test a separate simulated copy of the exact repair before asking Lars to approve
it, as in prior work; tag simulation clearly and retain all outputs/failures.

Then Lars runs:

```powershell
.venv\Scripts\python.exe review_ledger.py review-repair --run thursday-dress-20261103-01
```

Give him the **new displayed repair hash**, only after it exists. It is not yet
known. Never reuse a saved repair's prefix/grant or simulate a real decision.
After real VERIFIED, audit bindings/logs/checkpoint/resulting files; derive
follow-up eligibility from real passed operations only. Leave it unexecuted.

Record actual total duration and live/prepared/saved sections in the session
record and cue sheet. There is no screen/audio recording yet. After this dress
rehearsal, prepare **another unique untouched run** for Thursday's live segment;
do not recycle the consumed dress-rehearsal gates or delete history.

## Google Drive reflection — already delivered and verified

Editable native Google Doc:
https://docs.google.com/document/d/14MwdQcZ3z6ONUoEr9QlDLEiG_qClVmj5f0w_7tntvrw/edit?usp=drivesdk

Title: “Review Ledger — Capstone Technical Reflection — Working Draft — Lars Klander”.
In the connected Drive's **ChatGPT** folder (ID `1NexLJ1KP0IRkrs6ftfiSqVMS4yTajHXn`).
Created and populated through the Google Drive plugin; readback verified full
working text and eight native section headings. No public sharing was added.
It is deliberately longer than the final 1–2-page reflection, for Lars to edit.

See REFLECTION-WORKING-COPY.md. **Cloud and local Markdown do not auto-sync.**
Do not overwrite his cloud edits. If editing it later, use the Google Drive/Docs
skills, read current content/revision and make scoped guarded edits. It already
contains the actual failures, correction lessons, corpus tradeoffs and completed
fallback-chain outcome. Add the actual rehearsal timing only after measured.

## Preserved completed fallback and earlier history

Completed fresh fallback run: **`packaging-rehearsal-20261102`**.

| Stage | Real operation | Outcome |
|---|---|---|
| Corrected tests | `a27c01f604c34003a1bb1124713b81d3` | VERIFIED, seven tests |
| Optimization | `14ba9fa431624649bfd5771169957cb3` | VERIFIED, seven + thirteen checks |
| Disclosed fault | `22f6b9be80134420b4d64c92af8659d0` | FAILED as expected; quarantine retained |
| Separate repair | `bde81e424c184be6b33ecd79b92fec35` | VERIFIED, seven + thirteen checks |

Read-only audit matched interactive grants, binding/patch/log hashes, completed
checkpoints and actual files against recorded trees. Core evidence hashes were
unchanged by audit. Report: its `artifacts/failure-demo/completion.json`.
Follow-up is eligible for proposal only, unauthorized/unexecuted and unnecessary
for the demonstration. Earlier unplanned AMBIGUOUS and wrong-test FAILED
attempts remain intact; all 79 evidence files still match. See
FRESH-REHEARSAL-RESULT.md and TEST-EXPECTATION-CORRECTION.md.

The four original older human-approved operations also remain intact. Do not
restart them just to reconfirm history. `saved_evidence.py` defaults to those
older historical records; reopening a completed launcher is saved replay only.

## Implementation, environment and known lessons

- Local source is largely uncommitted on `implementation/first-patch`, design
  base `4c4ca01`; no implementation push/merge/deployment was performed here.
  Disposable source-snapshot commits under ignored artifacts are not main repo
  commits. Preserve all source, `.env`, `.venv`, artifacts and workspaces.
- Python `.venv\Scripts\python.exe` is 3.12.14. Locked ADK 2.13.0, LangGraph
  1.2.18, SQLite checkpointer 3.1.2. Model alias `gemini-3.8-flash` works; key and
  billing already configured. Never print/export secrets or ask to repeat setup.
- Docker Linux engine/pinned image already available. Image:
  `python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f`.
  Appropriate local-process escalation is needed for Git/Docker/asyncio in tool
  execution; user terminals work normally. This is not a login/billing problem.
- Exact patch approvals are interactive, bound, single use, 30 minutes after
  issuance. Pending proposals/deferrals do not acquire an expiry or permission.
  No auto-merge/push/deploy. Separate offline Docker sandbox; no host mounts,
  credentials/network; strict limits. Every real test/repair edit needs approval.
- `runtime_paths.py` separates run artifacts from immutable project assets.
  `operation_paths` uses short UUID workspaces under `artifacts/ws/`, retains
  historical layout compatibility; deep logs use Windows extended paths.
- `proposal_checks.py` statically checks bounded literal expectations (not a
  general evaluator). Rejected author output is retained. Author prompt now
  requests **exactly seven** tests to match the bounded optimization harness;
  this fresh run passed seven independently and under real approval.
- Source normalization trims whitespace outside string literal lines only;
  tests cover preservation. Replanning now retains raw outputs/diagnostics before
  validation. A prior rejected planner attempt's raw output was unavailable;
  that limitation is explicitly recorded, never reconstructed as a quote.
- Latest full clean-clone regression: 42 tests passed in 56.685s (62.375s with
  command startup); 224 exported hashes/frozen corpus hash verified. No reason
  to rerun full tests just for a context change or documentation edits.
- Latest source ZIP predating active rehearsal/copy-link updates:
  `artifacts/packaging/review-ledger-delivery-20261103.zip`.
  Source hash `48aa50bcf5f3dd1865b623651c397afb8767a1b50c98af4f7eda0c5773f97452`.
  Refresh after the actual rehearsal and final document reconciliation. Local
  ignored evidence is intentionally absent from credential-free source exports.

## Evaluation and remaining submission work

Frozen corpus: 16 fixtures (6 development, 6 renamed held-out variants, 4 clean
controls), seed 505, three repeats, parallel and single reviewer: 96/96 reviews.
Held-out macro precision/recall: **0.411/1.000 parallel, 0.510/1.000 single**.
Precision target missed; no claim four specialists improve accuracy. Token totals
101,708 versus 34,945; monetary cost unknown. All original results/labels retained.
Automatic matching needs human semantic adjudication. Corpus patch attempts 0;
full corpus repair/planning and fixed-order baseline remain unmeasured. Sixteen
oracle pairs and two authored mutants are not agent patch-success metrics.

Remaining beyond rehearsal: separate untouched Thursday run, full <=10-minute
recording, condensed/typeset architecture/reflection and page checks, reviewed
implementation publication/instructor access, recording link/Canvas upload,
actual Canvas deadline/page-limit/two-track confirmation. Read
THURSDAY-DEMO-CHECKLIST.md. No need to build the artificial dependent follow-up.

## Paste into the new chat

Continue from REHEARSAL-HANDOFF-2026-11-03.md in this project. The fresh dress run
thursday-dress-20261103-01 is ready, characterization already human-approved
VERIFIED, and fault gate pending with no real decision. Timer has NOT started.
Do not repeat setup or request the test approval again. Read the session cue sheet,
confirm I am physically ready, then coach the 0:00, 0:45, 1:35 and 2:20 cues;
the next personal approval is the deliberate fault at 2:20. Preserve every verified
and failed run and use only this new run's actual failure for live replanning.
After it passes, prepare a separate untouched Thursday run. The editable reflection
is already in Google Drive; preserve my edits and do not auto-sync over them.
