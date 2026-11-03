@echo off
echo HISTORICAL RUN: this launcher targets saved evidence, not a fresh demonstration.
echo For a new run use review_ledger.py new and its --run commands.
title Review Ledger - Optimization Approval
cd /d "%~dp0"
".venv\Scripts\python.exe" "optimization_step.py" review
echo.
echo Return to Codex after reviewing the result.
pause
