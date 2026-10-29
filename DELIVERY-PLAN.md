# Delivery plan and requirement coverage

Status: design only. Milestones are exit-criterion based; confirm actual Canvas date before assigning calendar dates.

## Milestones

| Milestone | Deliverable and exit criterion |
|---|---|
| M0 Design review | Review architecture, implementation contract, scope, ambiguity register and evaluation plan; see DESIGN-REVIEW.md for the requirement audit |
| M1 Feasibility spike | Pin Python, ADK, LangGraph, checkpointer and model versions; four schema-validated concurrent reviews; persisted interrupt survives restart; adapter contract demonstrated. Cite adapted code |
| M2 Evidence and intake | Pinned local/PR snapshots; GitHub pagination/error handling; immutable artifacts; validated findings and trace links |
| M3 Planning and HITL | DAG validation, candidate-only generation, human approve/reject/redirect/defer, stale approval rejection and dependent invalidation demonstrated |
| M4 Isolated changes | Disposable workspaces plus test sandbox, bounded tools, per-step patch bundles, crash reconciliation and failed-patch discard verified |
| M5 Evaluation | Frozen corpus and held-out labels; reproducible harness; baseline comparison and complete report including faults and all repeated runs |
| M6 Submission rehearsal | Fresh-clone setup succeeds; architecture/reflection typeset to agreed length; student explains every line; <=10 minute presentation/live-demo recording; links checked |

M1 is a go/no-go gate: if the bridge fails, document a smaller adapter or a justified framework substitution while preserving two named technologies and per-change HITL. Do not quietly remove either requirement.

## Requirement-to-component/evidence mapping

| Assignment requirement | Proposed component | Completion evidence |
|---|---|---|
| Two from named framework list | ADK specialists + LangGraph with HITL | M1 pinned environment and working cross-framework run |
| >=3 distinct agents | Four specialists, planner, patch author | Role contracts and interaction traces |
| Codebase or PR diff input | Local Git, GitHub and supplied-diff snapshot adapters | Same corpus case through all three complete-context paths; bare-diff partial mode explicitly tested |
| Security, performance, style, test-gap review | Four specialists and synthesis barrier | Category metrics, concurrent spans, clean controls |
| Parallel analysis and synthesis | ADK concurrent review, deterministic validation/join | Timed branch spans and reconciled findings |
| Dependency-aware planning beyond tool chaining | Goal hierarchy, DAG and evidence-triggered replanning | Prerequisite test plus revised descendants after failure |
| Generate refactored code for review | In-memory candidate + reviewed workspace diff bundle | Human-readable patch and acceptance evidence |
| Human approval before every refactoring step | Exact-patch gate, single-use approval, stale checks | Zero unapproved mutations, rejection/redirection demo |
| >=2 external APIs/data/tools | GitHub REST/Git; pytest/coverage/Ruff/benchmark runner | Recorded adapter inputs, versions and outcomes |
| Inspectable tracing | Mandatory local ledger; optional LangSmith | Complete decision/evidence chains |
| Graceful degradation and replanning | Retry budgets, partial status, reconstruction, DAG invalidation | Fault suite F1–F12 |
| Known-smell test corpus | Frozen labeled original Python fixtures | Per-category metrics and held-out results |
| Root ARCHITECTURE.md + diagram | Dedicated project root design | This directory exported as submission repo if needed |
| Technical analysis/reflection | TECHNICAL-REFLECTION.md | Planning, alternatives, limitations and future work |
| Runnable GitHub repo + setup README | Future M6 packaging | Fresh-clone install/run instructions, instructor access, Canvas repository link |
| Single presentation + live-demo recording <=10 min with failure | Script below | Final recording link in README; Canvas upload or unlisted YouTube/Loom |
| Due end Week 5, late penalty 50 points/day | Instructor/Canvas confirmation | Actual deadline recorded; Week 6 title not used to infer date |
| AI assistance permitted; explain every line | Original logic + explicit adaptation citations | README/comments attribute sources; student walkthrough |
| Rubric 500 points | Design 125; planning 100; implementation 100; reflection 75; presentation/demo 100 | Evidence across M0–M6; design alone does not satisfy implementation |

Optional bonuses, capped at +100 / 600 total: reusable documented permissively licensed public component (+40; public repo alone insufficient), Docker Compose single command with health checks/env configuration (+25), reproducible automated evaluation with summary report (+20), justified novel integration (+15). Proposed priorities are evaluation first, then packaging. Public release/licensing and novel-integration claims require later review; nothing is published by this design task.

## Demo: one presentation plus live demonstration, 9:30 total

| Time | Action and evidence |
|---|---|
| 0:00–0:45 | State problem and scope; show architecture diagram and two required frameworks |
| 0:45–1:20 | Open a pinned corpus PR/local snapshot; show known baseline behavior and run identity |
| 1:20–2:30 | Run four specialists concurrently; show security/performance/style/test-gap findings, source evidence and a disagreement |
| 2:30–3:20 | Show synthesis and DAG: characterization test before lookup optimization; explain why dependencies exist |
| 3:20–4:30 | Inspect exact first diff and acceptance checks; human approves; isolated apply and verification; show approval digest match |
| 4:30–5:30 | Inspect next candidate; human redirects overly broad patch; regenerated narrow candidate waits for fresh approval |
| 5:30–6:45 | Inject deterministic verification failure on approved candidate; show failed test, discarded workspace, invalidated descendant and revised plan |
| 6:45–7:45 | Human reviews and approves corrected patch; verify and display review bundle without merging |
| 7:45–8:40 | Show evidence chain and restart/stale-approval fault result; distinguish recorded test artifacts from current live action |
| 8:40–9:30 | Present actual evaluation summary, limitations, framework tradeoffs and next work |

Reserve 30 seconds below the 10-minute ceiling. Use tiny fixtures and preflight dependencies to keep the live path bounded. If network fails, switch explicitly to the pinned local case and show degraded status. If live execution cannot finish, disclose it and show a labeled prior recording; do not represent replay as live. Do not hide human waiting or failed attempts by presenting invented timings. A final rehearsal must measure the complete combined recording.

## Open choices and submission controls

- Confirm whether architecture's 2–4 pages includes reflection's 1–2 pages; current Markdown is a design source, not a verified page-count artifact.
- Confirm how two independent tracks may be submitted when the assignment requests one selected track.
- Confirm actual Canvas deadline, repository destination and instructor permissions.
- Select model after M1 schema/tool compatibility, availability and cost measurements; pin an exact version when possible.
- Validate container support on the demo host; without isolation, keep review/patch proposal available but block execution.
- Decide source/artifact retention and optional LangSmith export policy before testing on private repositories.
- Add setup commands, environment variable names without secrets, dependency locks, license/attribution and final recording link only once they exist. Design placeholders must never imply runnable status.
