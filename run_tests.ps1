# run_tests.ps1
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Installing dependencies (pytest, requests)…"
pip install pytest requests

Write-Host "Running pytest -v…"
pytest -v

Write-Host "All done!"
