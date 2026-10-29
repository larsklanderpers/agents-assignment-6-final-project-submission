# Current-state handoff — 30 October 2026

Repository: larsklanderpers/agents-assignment-6-final-project-submission | Branch: main
Track 5: Code Review & Refactoring

## Verified current state

Design reviewed 27 October; packaged as a standalone repository 30 October. Implementation has not started. No runnable application, dependency lock, executed evaluations, workflow exports or recording exists. Planned runner commands are not executable today. Framework documentation checks date to 26 October; validate current compatibility in the first spike.

The original capstone folder was moved to this repository root. CAPSTONE-REQUIREMENTS.md is included and its relative links repaired. No dependency on the previous parent folder remains. Inspect git log for the initial design commit SHA.

## Continue on the personal computer

Authenticate GitHub CLI for larsklanderpers, then run:
    gh repo clone larsklanderpers/agents-assignment-6-final-project-submission
    cd agents-assignment-6-final-project-submission
    git status
    git log -1 --oneline

If a clone already exists, inspect its status, remotes and history before updating; preserve local work. Open this repository in Codex/your editor and read applicable local AGENTS.md instructions. Credentials and machine sessions are not transferred. Configure secrets locally without committing them.

Read README.md, CAPSTONE-REQUIREMENTS.md, ARCHITECTURE.md, DESIGN-REVIEW.md, IMPLEMENTATION-CONTRACT.md, DELIVERY-PLAN.md, TECHNICAL-REFLECTION.md and EVALUATION.md.

## Technologies and invariants

Google ADK and LangGraph with HITL; local structured tracing required, LangSmith optional. LangSmith does not count toward the mandatory minimum of two course-listed frameworks.

Approvals bind exact patch, parent tree and plan version; 30-minute expiry, single use. Every plan revision invalidates pending approvals. All four specialists must complete before edits. Every edit including tests/recovery requires approval. Disposable workspaces and a separate container for untrusted tests are required. No automatic merge, push or deployment.

Each project requires at least three distinct agents, explicit planning, two tool/data/API integrations, meaningful HITL, inspectable evidence and decision summaries, and graceful failure handling.

## Immediate next development gate

Pin Python, ADK, LangGraph, checkpointer and model versions. Prove four concurrent schema-validated specialists, the custom ADK/LangGraph adapter and a persisted human interrupt surviving restart. Then build one slice: intake, reviews, dependency plan, exact-patch approval, isolated apply and verification.

Document actual compatibility results and justified revisions. Add setup commands only after verification. Execute the specified gate/recovery tests and evaluation scenarios; targets are not achieved scores. Cite adapted code and ensure the student can explain every line.

## Remaining deliverables

Runnable instructor-accessible GitHub repository and fresh-clone setup; root ARCHITECTURE.md with diagram and technical analysis; reflection updated with observed outcomes; reproducible evaluation; combined presentation/live demo <=10 minutes including agent interactions, HITL and a failure. Put the recording link in README or upload to Canvas.

Confirm the Canvas deadline, whether reflection counts within architecture page limits, and two-track submission handling. A private repository does not grant the instructor access automatically. Optional bonuses are recorded in CAPSTONE-REQUIREMENTS.md.

## Paste into a new development chat

Continue UCLA capstone track 5 in this repository. Read CURRENT-STATE-HANDOFF.md and its referenced documents; inspect Git state and applicable local instructions. Start the bounded feasibility spike, preserving the selected frameworks and approval invariants. Implement and verify the first vertical slice, then update documents with actual results, limitations and next steps. The existing design is not a runnable system.

