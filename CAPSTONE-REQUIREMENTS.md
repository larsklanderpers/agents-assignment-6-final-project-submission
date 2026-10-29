# Capstone requirements

Source: [Week 6 – Final Projects](https://docs.google.com/document/d/1FPDr1uDqUHj9IdHaRiUd_yI9lq4REdOScZRjcE7vP5k/edit), read 26 October 2026.

We are developing two independent submissions/designs: track 2 (incident response) and track 5 (code review and refactoring). The assignment describes selecting one track; confirm with the instructor how two projects should be submitted. This does not block designing both.

## Mandatory technology and scope

Each project must incorporate at least two of CrewAI, Google ADK, n8n, A2A Protocol, and LangGraph with HITL. Justify each selection and its tradeoffs in the architecture document. LangSmith supports observability but does not count as one of those two frameworks.

- At least three distinct agents, with roles, goals, responsibilities, and boundaries.
- Explicit task decomposition, goal hierarchies, or multi-step reasoning beyond sequential tool calls.
- At least two external APIs, data sources, or tool integrations.
- Meaningful human review, approval, or redirection.
- Inspectable logging/tracing or LangSmith integration.
- Graceful degradation and replanning for failed tools, unavailable APIs, and unexpected agent outputs.
- Record evidence, assumptions, decision summaries, alternatives, and tool outcomes for inspectability.

## Track-specific requirements

Track 2: simulated production incidents; telemetry agent, past-incident knowledge agent, hierarchical remediation planner, coordinator; triage, diagnosis, ranked remediation, post-mortem; human approval gates remediation execution. Emphasis: A2A-style coordination, n8n alerting/routing, LangSmith tracing, communication protocols, partial information.

Track 5: codebase or PR diff input; security, performance, style, and test-gap review; parallel analysis and synthesis; dependency-aware refactoring plan; generate refactored code for review; human approval before every refactoring step. Evaluate against known smells in a test corpus.

## Deliverables and grading

- Runnable GitHub repository with setup README, accessible to instructor; submit link via Canvas.
- Root ARCHITECTURE.md: design, roles, framework justification, data flow, decisions, at least one diagram. Architecture document target: 2–4 pages; technical analysis section target: 1–2 pages (clarify whether included in page total).
- Technical reflection: planning paradigm, coordination alternatives, tradeoffs, limitations, future work.
- Single presentation plus live-demo recording, maximum 10 minutes, including agent interactions, HITL, and at least one failure/edge case; Canvas upload or unlisted YouTube/Loom link in README.
- Due end of Week 5; exact date on Canvas. Document title says Week 6, so verify the actual date rather than infer it. Late penalty: 50 points/day.

Rubric (500): architecture/design 125; planning/reasoning 100; implementation 100; analysis/reflection 75; presentation/demo 100.

Optional bonus (maximum 100, total maximum 600): reusable documented permissively licensed public component +40 (public repo alone insufficient); Docker Compose single-command system with health checks and env configuration +25; reproducible automated evaluation with summary report +20; justified novel integration +15.

AI implementation assistance is permitted; the student must explain every line. Keep original agent logic, architecture, and integration; cite adapted tutorial/documentation/open-source code in comments and README.
