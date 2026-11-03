@echo off
echo HISTORICAL RUN: this launcher targets saved evidence, not a fresh demonstration.
echo For a new run use review_ledger.py new and its --run commands.
title Review Ledger - First Patch Approval
cd /d "%~dp0"
".venv\Scripts\python.exe" "approval_executor.py" review
echo.
echo Return to Codex after reviewing the result.
pause
