# Technical reflection

Status: prospective technical analysis, not a report of implementation results. Target: 1–2 typeset pages; confirm whether included in the architecture page limit.

## Planning paradigm and original contribution

The planning model is hierarchical decomposition combined with a validated dependency DAG and evidence-driven revision. The top goal is preserving intended behavior while reducing evidenced defects. Subgoals establish characterization tests, repair specific findings and demonstrate acceptance. An LLM proposes the decomposition, but deterministic code checks edge validity, cycles, readiness and approval bindings. This is more than chaining tools: a failed precondition can change the goal and invalidate descendants while leaving unrelated evidence usable.

The proposed original contribution is the approval-bound evidence ledger: every change carries an explicit chain from source evidence to finding, assumption, plan revision, exact patch, human decision and validation result. Originality is a design intention, not a claim that no comparable research or product exists. A successful demo should show why a previously approved action became invalid after new evidence, rather than only showing four agents returning text.

## Coordination alternatives

Fixed specialist roles allow parallel independent analysis and an explicit synthesis barrier. A free-form debate or supervisor that dynamically delegates every turn might discover unexpected concerns, but introduces variable cost and makes coverage difficult to assess. Our approach can still request focused re-review when evidence changes. Independence is conditional: four agents using the same model can share blind spots, so agreement is not treated as proof. Deterministic tools, behavioral tests and human judgment supply different forms of evidence.

ADK and LangGraph overlap in orchestration capability. Keeping the lifecycle solely in LangGraph avoids competing approval state machines; ADK sessions are subordinate review invocations. This separation costs serialization and context-management work but makes trust boundaries explicit. ADK's parallel workflow and LangGraph's interrupt/persistence capabilities are documented; their combination is a custom integration and requires a compatibility spike. We deliberately avoid assuming a native bridge or that structured output plus tools works identically on every model.

A single framework would be simpler to debug, but the assignment requires two from its named list. CrewAI with LangGraph remains a viable substitute if ADK integration proves disproportionately costly. A2A would provide a deployment boundary for external reviewers, but the prototype has no independent service requirement. n8n would be justified for organizational routing or notifications, not merely to increase the framework count. LangSmith is optional observability and cannot substitute for a required framework.

## HITL, safety and tradeoffs

Approval of intent is weaker than approval of the executable change. Binding approval to the parent tree, patch digest, plan revision and policy prevents a revised candidate from inheriting permission. The consequence is reviewer effort: every step needs a fresh decision. Small, well-scoped diffs with acceptance criteria reduce that burden; batch approval is excluded from the MVP because it weakens the explicit per-step requirement.

Generating a proposed diff in memory does not change code. Applying it in an isolated workspace is the gated operation. A Git worktree provides revision isolation, not protection from hostile tests. The separate execution sandbox is therefore part of correctness, and a missing sandbox disables execution while preserving read-only review. Failed runs leave a review artifact rather than an apparently successful repair.

Checkpointing preserves progress but does not make external side effects atomic. The operation ledger, tree comparison and workspace reconstruction make replay observable and recoverable. An ambiguous application stops or reconstructs; silently retrying mutations would be an unsound convenience. Human redirection can also create a new semantic goal, which requires revised tests and fresh approvals rather than pretending it is a mechanical refactor.

## Limitations, evaluation and future work

The MVP limits language, scope and repository size. It does not establish whole-program safety, reliable exploitability, or performance improvement from static inspection alone. A seeded corpus risks rewarding recognition of our chosen smells; held-out variants, clean controls and reviewer adjudication are necessary. Repeated model runs report variability and cost instead of hiding failed trials. Test success is evidence of preserved sampled behavior, not a proof of equivalence.

The first expansion should follow measured failure modes: better dependency extraction if planning misses prerequisites, better characterization tests if behavior regresses, or additional domain specialists if findings are missed. Later work could add multi-language parsers, independent reviewer models, A2A services and organizational approval policies. Those additions should retain exact patch authorization and evidence provenance. Optional reusable components, Compose packaging and automated evaluation are bonus candidates only after the core workflow is explainable, reproducible and complete.
