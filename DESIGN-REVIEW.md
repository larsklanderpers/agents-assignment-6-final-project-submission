# Track 5 design review — 27 October 2026

> Current implementation status — 2 November 2026: ADK 2.13.0 + LangGraph 1.2.18
> and SQLite checkpointer 3.1.2 are exercised under Python 3.12.14. Four historical
> human-approved operations are preserved (test/optimization/failure/repair).
> New demos have isolated run manifests and exact-patch gates. The frozen 16-fixture
> finding evaluation and single-reviewer comparison are executed; see
> [observed results](results/COMPARISON.md), [setup](README.md),
> [packaging proof](PACKAGING-VALIDATION.md) and [Thursday runbook](DEMO-RUNBOOK.md).
> Statements below using “proposed” or “unverified” describe the original design
> unless explicitly reconciled by these observed results. Arbitrary PR intake,
> corpus patch evaluation, human adjudication, publication and full spoken rehearsal
> remain open; no production-safety or completed-submission claim is made.


Reviewed against [CAPSTONE-REQUIREMENTS.md](CAPSTONE-REQUIREMENTS.md), the repository's shared requirement baseline. Scope: design readiness; no implementation, runtime compatibility, benchmark or security certification is implied. The prior official-document feasibility citations remain in ARCHITECTURE.md; this review adds application-policy decisions, not new framework API claims.

## Result

Every mandatory requirement has a design allocation. The design is ready to guide the bounded M1 feasibility spike and first vertical slice. Implementation, instructor access, evaluation results, page-count verification and recording remain future completion gates. The original architecture was broadly aligned; the following ambiguities could otherwise have produced a superficially compliant implementation.

| Gap found | Tightened decision | Where |
|---|---|---|
| Local revision versus PR diff semantics unclear | Three complete-context intake modes; bare diff remains partial/read-only | ARCHITECTURE §1; IMPLEMENTATION-CONTRACT |
| Only four specialists had explicit framework ownership | All six reasoning agents use ADK; planner performs semantic synthesis after deterministic validation/join | ARCHITECTURE §2; IMPLEMENTATION-CONTRACT |
| Partial specialist failure could allow unsafe scope inference | All four must complete before any change in the MVP; narrowing requires rerunning all four | ARCHITECTURE failure table; IMPLEMENTATION-CONTRACT |
| Human interface, actor identity and expiry unspecified | Local operator CLI, bound session, 30-minute approval validity, explicit decisions and separate simulated evaluation mode | IMPLEMENTATION-CONTRACT |
| Global plan version versus selective approval reuse inconsistent | Every plan revision invalidates pending approvals; every next patch uses latest parent tree | IMPLEMENTATION-CONTRACT |
| Test edits/recovery could bypass refactoring gate | Every edit needs exact-patch approval; auto-fix commands prohibited | ARCHITECTURE §3; IMPLEMENTATION-CONTRACT |
| Consumed approvals and crash retries underspecified | Atomic approval consumption/operation intent; explicit operation states; reconciliation only; fresh approval after failure | IMPLEMENTATION-CONTRACT; EVALUATION F11 |
| Ordinary subprocess could be mistaken for security isolation | Container required for baseline and candidate execution; unavailable boundary blocks execution | IMPLEMENTATION-CONTRACT |
| Security fix conflicts with unconditional behavior preservation | Case manifest defines approved intentional delta; legitimate behavior preserved and malicious behavior corrected | EVALUATION |
| Duplicate findings, abstentions and tiny repeated samples distort scores | One-to-one matching, N/A denominators, per-fixture variability, attempted-step and complete-case patch success | EVALUATION |
| Design did not define a minimal demonstrable implementation | One real cross-framework, human-approved, failure/recovery vertical slice with code patches | IMPLEMENTATION-CONTRACT |

## Mandatory coverage audit

| Requirement | Design evidence | Implementation proof still needed |
|---|---|---|
| Two named technologies, with justification | ADK + LangGraph HITL; architecture §7 and reflection alternatives | Pin compatible versions; execute both meaningfully in M1 |
| At least three distinct agents | Four specialists plus planner and patch author, architecture §3 | Agent traces, boundary enforcement and validated contracts |
| Nontrivial planning | Goal hierarchy, dependency DAG, conditions and replanning, architecture §5 | Demonstrate failure invalidating a dependent proposal |
| Two external integrations | GitHub/Git intake and local test/analysis toolchain, architecture §6 | Real adapter outcomes; local and GitHub paths exercised |
| Meaningful HITL | Per-patch CLI decision; reject/redirect/defer/cancel; bound authorization | Human demonstration and zero unauthorized edits |
| Inspectable tracing | Structured local ledger and complete evidence chain | Actual artifacts with assumptions, alternatives and tool outcomes |
| Failure handling | Bounded retries, partial results, blocked mutation, recovery and replanning | Reproducible fault suite F1–F12 |
| Track 5 input and four review categories | Complete-context modes and parallel four-specialist barrier | Input tests, concurrent spans and category findings |
| Synthesis and dependency-aware plan | Semantic planner after validated join; DAG validation | Conflict resolution trace and valid ordered plan |
| Refactored code for human review | Exact individual/cumulative diffs, acceptance and unresolved findings | Actual patches, not recommendations alone |
| Approval before every step | All edits gated, including tests and recovery | Gate tests, expiry/stale/replay checks and human recording |
| Known-smell corpus | Six development, six held-out, four clean controls; frozen labels | Original fixtures, manifest, hidden oracles and measured report |
| Root architecture and diagram | Dedicated-root ARCHITECTURE.md with Mermaid | Typeset page check; root placement in final submission repo |
| Technical reflection | Separate reflection on planning, alternatives, tradeoffs, limits, future work | Consolidate into technical-analysis section if required; reflect on actual measured results |
| Runnable GitHub repository and setup README | Delivery M6 and README completion gates | Fresh clone, instructor access, Canvas repository link |
| One presentation/live-demo recording <=10 minutes incl. failure | Delivery plan 9:30 script | Rehearsed combined recording and Canvas or unlisted link in README |
| Deadline and attribution | Delivery controls retain Week 5/Week 6 discrepancy, penalty and source obligations | Confirm Canvas date; cite adaptations; student explains every line |

Optional bonuses remain explicitly optional and retain their original point values in DELIVERY-PLAN.md. LangSmith is optional observability and never counted as a mandatory framework. Track 2 requirements do not apply to this separate Track 5 design.

## Remaining choices and release gates

Instructor confirmation is still needed for page-count interpretation, actual deadline and submission of two tracks. These do not block the feasibility spike. Repository destination and instructor access must be settled before submission. Exact model/package versions, container settings and restart behavior must be demonstrated before claiming implementation readiness beyond the spike. Do not begin with optional A2A, n8n, remote identity or public-component bonuses.

Architecture text remains a Markdown source with a target page range, not a page-count-certified deliverable. Keep this audit, implementation contract, evaluation and delivery details as supporting material so the final architecture narrative can fit the agreed limit. The technical reflection must be revised after implementation to distinguish observed tradeoffs from design expectations.
