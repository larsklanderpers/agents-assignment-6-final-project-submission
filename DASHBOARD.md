# Local evidence dashboard

Optional read-only presentation layer on `feature/read-only-dashboard`.
The pre-UI assessed implementation is commit `7bfe8ef`, tagged
`checkpoint/pre-dashboard-20261103`. This is an implementation checkpoint,
not a declaration that remaining submission deliverables are complete.

Double-click `start-dashboard.cmd`, or run:

```powershell
.venv\Scripts\python.exe dashboard.py
```

Open http://127.0.0.1:8765 in your browser. Keep the launcher running while
using the dashboard; Ctrl+C stops it. Requires only Python's standard library.
If the port is busy, use `--port 8766` and open the printed address.

Select a run, inspect the prepared agent findings and dependency plan, expand
candidate diffs and outcome evidence, and read the frozen corpus comparison.
Refresh manually or enable five-second refresh during the demonstration.
The default selection is the prepared Thursday dress rehearsal when present.
No UI action starts the rehearsal clock, launches agents, replans, approves,
executes, or edits evidence. All approvals remain in the interactive terminal.

Real operations are distinguished by their ledger decision mode. Simulated
checks appear in a separate expandable section. Unexecuted source proposals
can appear alongside their executable candidates; neither is an approval.
Evidence is grouped by candidate, not globally ordered by time. The displayed
plan readiness is recorded proposal classification, not recomputed permission.
Patch hash checks alone do not establish full provenance or log integrity.

The server binds only to loopback, accepts only local Host headers, exposes
fixed read routes, and opens ledgers in SQLite read-only mode. It does not serve
arbitrary project files. Missing/partially written evidence is reported instead
of inventing an outcome. A source-only clone has no private historical runs;
it shows an empty-state message until runs exist locally.

Local history recovery archive and SHA256 inventory are under ignored
`artifacts/checkpoints/pre-dashboard-20261103/`. Original evidence stays in
place. Google Docs edits are independent and are not synchronized or changed.

Before rehearsal: open the selected run and terminal, keep the timer stopped,
then tell the coach you are ready. Characterization is already VERIFIED. The
next real decision remains the disclosed fault at 2:20; do not repeat setup.
