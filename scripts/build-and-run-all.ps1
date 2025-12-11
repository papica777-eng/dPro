#!/usr/bin/env pwsh
# Builds both Flask images (root and DP/dwashesp-main) and brings them up with docker-compose

param()

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

Write-Host "Building root dpro-flask image..."
docker build -t dpro-flask -f Dockerfile .

Write-Host "Building DP/dwashesp-main image..."
docker build -t dwashesp-main -f DP/dwashesp-main/Dockerfile DP/dwashesp-main

Write-Host "Starting both services via docker-compose (this will rebuild if needed)..."
docker-compose up --build
