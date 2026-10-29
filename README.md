# Track 5 — Review Ledger: Code Review & Refactoring Pipeline

Personal-computer continuation: [CURRENT-STATE-HANDOFF.md](CURRENT-STATE-HANDOFF.md).

Status: **design complete for review; implementation has not started**. No runnable system, evaluation results or recording is claimed.

[Shared assignment requirements](CAPSTONE-REQUIREMENTS.md) preserve the technology, deliverable and submission obligations. This track uses **Google ADK and LangGraph with HITL** as its proposed architecture. Official documentation supports the selected capabilities; exact package/model compatibility requires the first implementation spike.

## Design artifacts

- [DESIGN-REVIEW.md](DESIGN-REVIEW.md): 27 October requirement audit, resolved gaps and remaining completion gates.
- [IMPLEMENTATION-CONTRACT.md](IMPLEMENTATION-CONTRACT.md): concrete intake, CLI, authorization, replay, sandbox and first-slice acceptance rules.
- [ARCHITECTURE.md](ARCHITECTURE.md): system diagram, six agent roles and contracts, state and approval lifecycle, adaptive dependency planning, integrations, evidence ledger, recovery and documented framework feasibility.
- [TECHNICAL-REFLECTION.md](TECHNICAL-REFLECTION.md): planning paradigm, coordination alternatives, tradeoffs, limitations and future work; target 1–2 typeset pages.
- [EVALUATION.md](EVALUATION.md): reproducible known-smell corpus specification, hidden controls, metrics, baselines and fault scenarios. Targets are not measured results.
- [DELIVERY-PLAN.md](DELIVERY-PLAN.md): requirement mapping, milestones, submission controls, open choices and a 9:30 failure-inclusive presentation/demo script.

The architecture targets 2–4 typeset pages; clarify whether reflection is included, then typeset and verify page counts. If submitted as a standalone repository, this directory becomes its root with ARCHITECTURE.md at that root. Work in the other capstone remains separate.

## Key decisions

Specialists review security, performance, style and test gaps concurrently through ADK. LangGraph owns the persistent state machine and per-step human approval. An application adapter links them; a native cross-framework bridge is not assumed. Evidence-driven replanning updates a dependency DAG and invalidates affected approvals.

Every approval binds to an exact patch, parent tree and plan version. Code changes happen only in disposable workspaces after approval; untrusted tests require a separate sandbox. Outputs are patches and evidence for human review. There is no automatic merge, push or deployment.

GitHub/Git snapshot intake and local analysis/test tools provide at least two integrations. Local structured tracing is required; optional LangSmith is observability and does not count toward the two-framework requirement.

## Next completion gates

Follow the milestones in DELIVERY-PLAN.md: framework compatibility spike, intake/evidence, planning/HITL, isolated execution, evaluation, then submission rehearsal. Future setup instructions and recording links belong here when verified. The instructor must have access to the runnable GitHub repository; submit its link through Canvas and provide one presentation plus live-demo recording of at most 10 minutes including a failure. Confirm the actual deadline on Canvas and how two tracks may be submitted.

AI implementation assistance is permitted, but the student must explain every line. Cite any adapted code in comments and this README. The design's official documentation sources are linked beside the corresponding claims in ARCHITECTURE.md; no tutorial code has been copied into this project.
