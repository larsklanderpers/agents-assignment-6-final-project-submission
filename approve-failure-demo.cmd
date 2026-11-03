@echo off
echo HISTORICAL RUN: this launcher targets saved evidence, not a fresh demonstration.
echo For a new run use review_ledger.py new and its --run commands.
title Review Ledger - Deliberate Failure Demonstration
cd /d "%~dp0"
".venv\Scripts\python.exe" "failure_demo.py" review-fault
echo.
echo FAILED is the expected negative-case result. Return to Codex for evidence inspection and replanning.
pause
