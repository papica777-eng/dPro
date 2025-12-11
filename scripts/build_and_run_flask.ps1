#!/usr/bin/env pwsh
# Build and run the Flask Docker image for dPro
# Usage:
# 1) With a mounted serviceAccountKey.json (local Docker)
#    Edit the $KeyPath variable below, then run this script in PowerShell.
# 2) With base64 credentials (for CI or platforms that pass large env vars):
#    Set $env:GOOGLE_CREDENTIALS_BASE64 before running, and the container will decode it.

param()

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Write-Host "Building Docker image 'dpro-flask' from repo root..."
docker build -t dpro-flask -f Dockerfile .

Write-Host "To run with a mounted service account JSON (local):"
Write-Host "  docker run --rm -p 5000:5000 -v \"C:\\path\\to\\serviceAccountKey.json:/app/serviceAccountKey.json:ro\" -e \"USE_FIREBASE=true\" --name dpro-flask dpro-flask"

Write-Host "Or, to run passing base64 creds from your PowerShell session (no file mount):"
Write-Host "  # In PowerShell:  $env:GOOGLE_CREDENTIALS_BASE64 = '[base64-string]'"
Write-Host "  docker run --rm -p 5000:5000 -e \"USE_FIREBASE=true\" -e \"GOOGLE_CREDENTIALS_BASE64=$($env:GOOGLE_CREDENTIALS_BASE64)\" --name dpro-flask dpro-flask"

Write-Host "Note: For large base64 strings you may prefer to set the env var in your container platform rather than passing inline."
