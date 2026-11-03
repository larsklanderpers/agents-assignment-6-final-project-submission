param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& $Python -c 'import sys; assert sys.version_info[:2] == (3,12), "Python 3.12 required"'
if ($LASTEXITCODE -ne 0) { throw 'Select a Python 3.12 interpreter with -Python.' }
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & $Python -m venv --without-pip .venv
    if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed.' }
}
# Supports the bundled runtime whose ensurepip is unavailable.
& $Python -m pip --python '.venv\Scripts\python.exe' install -r requirements-spike.lock
if ($LASTEXITCODE -ne 0) { throw 'Locked dependency installation failed.' }
& $Python -m pip --python '.venv\Scripts\python.exe' check
if ($LASTEXITCODE -ne 0) { throw 'Dependency compatibility check failed.' }
if (-not (Test-Path -LiteralPath '.env')) { Copy-Item -LiteralPath '.env.example' -Destination '.env' }
Write-Host 'Dependencies installed. Configure .env locally, start Docker Desktop, then run review_ledger.py doctor.'
