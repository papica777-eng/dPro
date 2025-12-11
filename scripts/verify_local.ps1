#!/usr/bin/env pwsh
param(
    [string]$BaseUrl = "http://localhost:5000/api"
)

function Check-Health {
    Write-Host "Checking /health at $BaseUrl..."
    $healthUrl = $BaseUrl.TrimEnd('/').Replace('/api','') + "/health"
    try {
        $resp = Invoke-RestMethod -Uri $healthUrl -Method GET -UseBasicParsing -TimeoutSec 10
        Write-Host "Health: $($resp | ConvertTo-Json -Depth 2)"
    } catch {
        Write-Error "Health check failed: $_"
    }
}

function Check-GetProjects {
    Write-Host "GET /projects"
    try {
        $resp = Invoke-RestMethod -Uri "$BaseUrl/projects" -Method GET -UseBasicParsing -TimeoutSec 30
        Write-Host "Projects: $($resp | ConvertTo-Json -Depth 4)"
    } catch {
        Write-Error "Failed to get projects: $_"
    }
}

function Check-PostProject {
    Write-Host "POST /project"
    $payload = @{ project_name = "Smoke Test"; target_url = "https://example.com"; selected_goals = @{ "Performance Metrics & Load Times" = $true } } | ConvertTo-Json
    try {
        $resp = Invoke-RestMethod -Uri "$BaseUrl/project" -Method POST -Body $payload -ContentType 'application/json' -UseBasicParsing -TimeoutSec 60
        Write-Host "Create response: $($resp | ConvertTo-Json -Depth 4)"
    } catch {
        Write-Error "Failed to create project: $_"
    }
}

Check-Health
Check-GetProjects
Check-PostProject
