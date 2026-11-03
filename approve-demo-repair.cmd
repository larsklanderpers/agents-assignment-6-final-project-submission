@echo off
echo HISTORICAL RUN: this launcher targets saved evidence, not a fresh demonstration.
echo For a new run use review_ledger.py new and its --run commands.
title Review Ledger - Replanned Repair Approval
cd /d "%~dp0"
".venv\Scripts\python.exe" "failure_demo.py" review-repair
echo.
echo Return to Codex after reviewing the result.
pause
