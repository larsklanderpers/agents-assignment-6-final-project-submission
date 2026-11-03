# Technical reflection

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


Status: original design analysis with observed runtime and evaluation lessons appended below. Target: 1–2 typeset pages; confirm whether included in the architecture page limit.

## Planning paradigm and original contribution

The planning model is hierarchical decomposition combined with a validated dependency DAG and evidence-driven revision. The top goal is preserving intended behavior while reducing evidenced defects. Subgoals establish characterization tests, repair specific findings and demonstrate acceptance. An LLM proposes the decomposition, but deterministic code checks edge validity, cycles, readiness and approval bindings. This is more than chaining tools: a failed precondition can change the goal and invalidate descendants while leaving unrelated evidence usable.

The proposed original contribution is the approval-bound evidence ledger: every change carries an explicit chain from source evidence to finding, assumption, plan revision, exact patch, human decision and validation result. Originality is a design intention, not a claim that no comparable research or product exists. A successful demo should show why a previously approved action became invalid after new evidence, rather than only showing four agents returning text.

## Coordination alternatives

Fixed specialist roles allow parallel independent analysis and an explicit synthesis barrier. A free-form debate or supervisor that dynamically delegates every turn might discover unexpected concerns, but introduces variable cost and makes coverage difficult to assess. Our approach can still request focused re-review when evidence changes. Independence is conditional: four agents using the same model can share blind spots, so agreement is not treated as proof. Deterministic tools, behavioral tests and human judgment supply different forms of evidence.

ADK and LangGraph overlap in orchestration capability. Keeping the lifecycle solely in LangGraph avoids competing approval state machines; ADK sessions are subordinate review invocations. This separation costs serialization and context-management work but makes trust boundaries explicit. ADK's parallel workflow and LangGraph's interrupt/persistence capabilities are documented; their combination is a custom integration now exercised by the compatibility spike and real approved operations. We deliberately avoid assuming a native bridge or that structured output plus tools works identically on every model.

A single framework would be simpler to debug, but the assignment requires two from its named list. CrewAI with LangGraph remains a viable substitute if ADK integration proves disproportionately costly. A2A would provide a deployment boundary for external reviewers, but the prototype has no independent service requirement. n8n would be justified for organizational routing or notifications, not merely to increase the framework count. LangSmith is optional observability and cannot substitute for a required framework.

## HITL, safety and tradeoffs

Approval of intent is weaker than approval of the executable change. Binding approval to the parent tree, patch digest, plan revision and policy prevents a revised candidate from inheriting permission. The consequence is reviewer effort: every step needs a fresh decision. Small, well-scoped diffs with acceptance criteria reduce that burden; batch approval is excluded from the MVP because it weakens the explicit per-step requirement.

Generating a proposed diff in memory does not change code. Applying it in an isolated workspace is the gated operation. A Git worktree provides revision isolation, not protection from hostile tests. The separate execution sandbox is therefore part of correctness, and a missing sandbox disables execution while preserving read-only review. Failed runs leave a review artifact rather than an apparently successful repair.

Checkpointing preserves progress but does not make external side effects atomic. The operation ledger, tree comparison and workspace reconstruction make replay observable and recoverable. An ambiguous application stops or reconstructs; silently retrying mutations would be an unsound convenience. Human redirection can also create a new semantic goal, which requires revised tests and fresh approvals rather than pretending it is a mechanical refactor.

## Limitations, evaluation and future work

The MVP limits language, scope and repository size. It does not establish whole-program safety, reliable exploitability, or performance improvement from static inspection alone. A seeded corpus risks rewarding recognition of our chosen smells; held-out variants, clean controls and reviewer adjudication are necessary. Repeated model runs report variability and cost instead of hiding failed trials. Test success is evidence of preserved sampled behavior, not a proof of equivalence.

The first expansion should follow measured failure modes: better dependency extraction if planning misses prerequisites, better characterization tests if behavior regresses, or additional domain specialists if findings are missed. Later work could add multi-language parsers, independent reviewer models, A2A services and organizational approval policies. Those additions should retain exact patch authorization and evidence provenance. Optional reusable components, Compose packaging and automated evaluation are bonus candidates only after the core workflow is explainable, reproducible and complete.

## Observed evaluation and delivery lessons — 2 November

The live bounded chain demonstrated four real, separate human approvals: tests,
optimization, a disclosed negative-case failure, and a guarded repair after
actual-log replanning. Keeping failed workspaces and exact bindings made failure
inspectable without changing the approved successful branch. New-run packaging
exposed a separate issue: historical paths and fixed IDs are unsuitable for a fresh
clone. Run manifests now isolate every demonstration while preserving local history.

Parallel specialists did not outperform the general reviewer on the frozen tiny
corpus: held-out automatic macro precision was 0.411 versus 0.510, with recall
1.000 for both. The parallel mode reported 31 unmatched control findings versus
15 and used 101,708 provider-reported total tokens versus 34,945. Precision misses
the 0.80 target; role separation provides inspectable coverage but does not
establish superior accuracy. These sparse labels need human semantic adjudication;
valid extra discoveries may exist. The unamended scores remain published.

All sixteen original/corrected fixture contracts passed in the offline runner,
and two harness-authored mutants were detected. Those checks establish oracle
behavior, not successful agent-generated corpus repairs. The current patch-success
and recovery evidence is the original bounded human-approved chain, not sixteen
repair cases. Full corpus repair, a fixed-order non-replanning comparison, stronger
label review and arbitrary PR intake remain outside the observed results.

Fresh setup also exposed environment-level failures and line-ending changes.
The bootstrap pip route and explicit LF checkout policy now have local validation.
A full spoken demo still requires Lars's real decisions and stopwatch measurement;
a 9:30 schedule is a target, not a measured completed recording.

## Rehearsal failures: authorization, correctness and reviewer effort

The fresh rehearsal exposed two different failures that the original successful
fixture had not revealed. First, the approved patch was applied, but Windows path
lengths prevented the executor from seeing its test file. The operation stopped
as AMBIGUOUS and quarantined the workspace. Short UUID workspace paths and
long-path-safe evidence handling addressed that portability problem. A separate
diagnostic also exposed Docker output interleaving: a valid result marker could
appear inside a partial progress line. Parsing now tolerates that ordering while
rejecting duplicate result markers. These were execution and packaging defects,
not evidence that the proposed production behavior was wrong.

The next human-approved attempt reached the tests and failed for a different
reason: the model-generated test expected `[1, 1, 1, 3]` for an input whose
order-preserving result is `[1, 1, 3, 1]`. The production function was correct for
that example. The earlier review had checked syntax, patch applicability and
authorization, but missed the semantic error in the expected value. This shows
why generated tests are proposals rather than an independent source of truth:
changing correct production code to satisfy that assertion would introduce a
regression. Exact-patch approval establishes permission; it does not establish
correctness. Human review needs a clear behavioral contract and trustworthy
acceptance evidence as well as an inspectable diff.

Repeated approval requests also have a real cost. Two unsuccessful human-approved attempts preceded a third that reached a
VERIFIED characterization result. The
improvement was to move inexpensive semantic checks earlier: a static guard now
checks bounded literal examples against the documented membership contract, and
the corrected test bytes passed all seven tests in a separate, explicitly
simulated Git/Docker verification before another human gate was prepared. The
guard covers six concrete examples, not arbitrary Python or complete test
correctness. The updated 39-test regression suite passed. The simulation provides
evidence for review; it neither creates a real human approval nor transfers an
earlier consumed grant, and the real gated operation must still verify its own
result. The general lesson is to reduce avoidable review work without weakening
the authorization boundary.

Both unsuccessful attempts remain part of the record: AMBIGUOUS for the first,
FAILED for the second. All 79 files in their evidence directories and quarantined
workspace matched before and after the correction. Preserving them made it
possible to distinguish infrastructure failure, an incorrect test oracle and the
eventual correction without rewriting history. These were actual unplanned
rehearsal failures, separate from the intentionally disclosed negative-case
optimization demonstration. [Correction evidence](TEST-EXPECTATION-CORRECTION.md)
and [packaging validation](PACKAGING-VALIDATION.md) retain the details.

For the final reflection, retain these observed lessons alongside the weaker
parallel-review precision and higher token usage. Do not present only successful
runs or infer that more agents, more tests or more approval prompts necessarily
improve outcomes. The corrected human-gated run subsequently passed all seven tests, independently
of its earlier simulated verification. The full spoken rehearsal remains
pending; incorporate its measured outcome before submission.
This working reflection still needs selection and condensation to the agreed
1–2 typeset pages, with the supporting evidence kept in the linked documents.

A later fresh-run preparation also exposed a path assumption: the trusted
optimization harness was being resolved from the artifact directory. Separating
immutable project assets from per-run data fixed the lookup, with a regression
that changes the artifact root. The interrupted model proposal and reviews were
retained; where its original rationale had not been persisted, the record says
so and labels the developer summary. Durable evidence should capture model
outputs before later packaging steps can fail. The optimization then passed
seven tests plus thirteen checks in an explicitly simulated preapproval run;
its subsequent real human-approved operation also passed all seven tests and
thirteen checks. This provides two distinct evidence records without treating
the simulation as human authorization. The separate deliberate-failure and recovery chain subsequently completed
with real approvals, as recorded below. See
[FRESH-REHEARSAL-RESULT.md](FRESH-REHEARSAL-RESULT.md).

## Fresh replanning observations - 3 November

The deliberately faulty patch subsequently failed under real human approval,
and its actual TypeError log drove a live plan revision from 3 to 4. The first
planner response was rejected because it did not satisfy derived repair readiness
and dependent blocking. No gate or revised authoritative plan was created from
that response. Its raw output had not been retained, so its precise defect cannot
be retrospectively claimed; only the observed rejection is recorded. Raw model
outputs and diagnostics are now saved before subsequent validation. Clarifying
that readiness means permission to propose, not permission to execute, produced
a plan that passed the unchanged dependency checks.

The repair author then produced trailing whitespace on two blank lines. Strict
Git validation rejected it before approval. Whitespace outside string-literal
lines was normalized, with AST equivalence checked and string-preservation tests
added; the raw author response remains available. This separates a harmless
formatting repair from changing an agent's semantic proposal or weakening policy.
The full regression suite passed 42 tests. The repair's independent simulated
preflight passed seven tests plus thirteen checks, and its subsequent real
human-approved operation passed those checks independently. The follow-up is now
eligible for proposal, but remains unauthorized and unexecuted. Stale approval replay was
rejected without a new operation. These preparation failures and missing initial
raw output belong in the reliability discussion alongside the successful plan
revision; they should not be hidden by showing only the final candidate.

## Completed chain and final reflection - 3 November

The real repair reached VERIFIED in operation
`bde81e424c184be6b33ecd79b92fec35`, completing the bounded test, optimization,
deliberate failure, live replanning and separately approved recovery chain.
Read-only inspection matched every stage's interactive approval binding,
consumption record, patch/log hashes, terminal checkpoint and actual files to its
recorded tree. Manifests, patches, ledgers and checkpoints had identical hashes
before and after the audit. The earlier unsuccessful attempts' 79 evidence files
also remained unchanged. This makes the transition history inspectable without
turning a replay into a new demonstration.

The real repair passed seven tests and thirteen additional checks. Its single
2,500-integer workload measured median elapsed times of 97.368 ms before and
0.539 ms after (five warmups, twenty trials), with extra memory. These results
support this bounded case, not whole-program equivalence, a general workload
speedup or successful repair across the corpus. The preserved automatic corpus
scores still miss the precision target and favor the single reviewer over the
parallel reviewers on this small dataset. Those findings and the unsuccessful
preparation attempts remain part of the final analysis.

A completed execution chain is different from a completed presentation. The
spoken duration, legibility, human waiting time, fallback transition and final
recording have not yet been measured together. A new run is required for a fresh
live segment; this completed run is saved evidence. The working reflection must
now be condensed to the agreed page limit while retaining the measured tradeoffs,
missed expectation, rejected plan, missing initial raw output and cost of repeated
human review. The final rehearsal's actual duration and outcome should be added
before submission. See THURSDAY-DEMO-CHECKLIST.md.

## Assessment baseline and additional hardening — 3 November

The rehearsal and primary recording will follow the established rubric-focused demonstration using the checkpointed, bounded implementation and its verified evidence. The read-only dashboard makes that evidence easier to inspect; approvals remain in the terminal. The baseline's limitations and missed precision target will be stated explicitly, rather than presented as resolved.

In parallel, I have started a separate hardening branch to address three additional development objectives: intake of small Python repositories and eventually PRs; end-to-end evaluation of agent-generated plans, patches and recovery; and better finding precision through stronger context and evidence requirements. Assignment 5 will provide a real repository for development and evaluation. Because it has already been inspected, it will not be represented as an unseen holdout. These additions address material limitations of the prototype; describing them as additional work does not establish that they are complete or exempt them from assessment.

The verified baseline, failed runs and original evaluation results are preserved independently. Rehearsal is temporarily paused while hardening starts; the prepared rehearsal clock has not started. If all three additions are implemented and independently verified within the available time, I intend to make a second recording showing the expanded implementation, clearly distinguishing its new results from the first recording. Any supplemental or replacement submission will follow the instructor's rules and the recording time limit. Until that verification exists, the first recording and reflection will make only the claims supported by the baseline evidence.

## Blinded cross-model holdout — 4 November

I froze the Gemini review implementation at commit 6d3b314 before asking a fresh-context Luna agent to author twelve synthetic Python cases: eight labelled defects and four intended clean controls. Luna did not receive the implementation, previous prompts, examples or scores. Source, visible tests and contracts formed the public package; labels, corrected references and acceptance checks stayed in a separate private package. The tool-free Gemini reviewer received only the public inputs. All twelve original/reference consistency checks passed after one private packaging correction, and all reviewer outputs were hash-locked before scoring. This is accurately described as a separately authored, blinded holdout evaluation of a frozen Gemini-based system using Luna-generated cases and labels, with independent human adjudication pending.

The frozen system matched all eight labelled defects. Its filtered output contained three additional findings, giving provisional micro precision of 0.727, macro precision of 0.850 and recall of 1.000 against the original key. Three of four intended clean controls received no accepted findings. All additional findings concerned missing tests. Post-score isolated checks supported all three coverage gaps, including one in an intended clean control. This exposed incomplete author labels: checking that intended defects fail and reference corrections pass does not establish that an answer key captures every valid finding. I retained the original key and scores rather than silently relabelling the cases to obtain a perfect result.

These results measure review findings, not repair success. They involve one repetition, eight labelled defects, synthetic cases and a hosted model alias; different author and reviewer models do not guarantee independent errors. The unmatched findings and semantic matches still require human adjudication. The macro target was numerically exceeded against this provisional key, but overall precision was lower and label completeness is unresolved, so I do not claim that general accuracy is fixed. The earlier results remain unchanged, and this set is no longer unseen if used for subsequent tuning. The primary rehearsal and recording retain the established rubric-focused baseline; this holdout is additional evidence for a possible second recording under the instructor's submission rules.

## Human adjudication of the additional findings — 4 November

After reviewing the code, visible tests and isolated diagnostic results, I accepted all three additional findings as valid test-coverage gaps within the supplied files. Case 01 lacks a negative test for another tenant's document; its original production code is correct, but the visible test fails to catch removal of the tenant check. Case 05 lacks an inactive-publisher test, and case 10 lacks a disabled-owner test; in both cases, the missing tests allow an existing security defect to pass the visible suite. The security defects and their missing regression tests are related but distinct findings because the system explicitly evaluates security and test gaps separately. This acceptance does not count them as three additional production bugs.

This is my post-score adjudication as the project author, based on the walkthrough and retained execution evidence, not a blinded external review. The original answer key, locked model outputs and automatic scores remain unchanged, with this decision recorded separately. The three disputed coverage findings are now accepted; this does not establish independent review of every original label, every semantic match, or complete corpus coverage.

## Original and adjudicated holdout scores — 4 November

The comparison below concerns the filtered reviewer output from the same frozen run. No model was rerun or tuned. The original column uses Luna's initial answer key; the adjudicated column adds the three coverage findings I accepted after reviewing their evidence.

| Metric | Original key | Adjudicated |
|---|---:|---:|
| Known findings | 8 | 11 |
| True positives | 8 | 11 |
| False positives | 3 | 0 |
| False negatives | 0 | 0 |
| Overall precision | 72.7% | 100% |
| Macro precision | 85.0% | 100% |
| Recall (overall / macro) | 100% / 100% | 100% / 100% |

The adjudicated results meet the 0.80 precision and recall targets on this set. Original macro precision already exceeded 0.80; original overall precision did not. This remains twelve synthetic cases with one repetition. My adjudication was post-score and as project author, not a blinded external review; it resolved only the three disputed coverage findings, not an independent audit of every original label or semantic match. Recall is measured against eleven known findings and does not prove that no other issues were missed. These findings include missing tests, not eleven production bugs. Neither general repository accuracy nor repair success is established. The original answer key, locked outputs and automatic scores remain unchanged; the adjudicated comparison is a separate record.
