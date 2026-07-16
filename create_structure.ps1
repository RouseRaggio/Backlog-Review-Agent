@"
PowerShell Script for AI-QA-Agents Directory Structure
===============================================

This script creates the complete directory structure for the AI-QA-Agents project
following Clean Architecture principles.

@author: AI Assistant
@date: $(Get-Date -Format 'yyyy-MM-dd')

@@ - Start of Script @@

# Set base path and change to it
$basePath = "C:\Users\User\Documents\AI-QA-Agents"
Set-Location -Path $basePath

Write-Host "Creating AI-QA-Agents directory structure..." -ForegroundColor Cyan

# Create main apps directory
Write-Host "Creating apps directory..." -ForegroundColor Yellow
New-Item -Path "apps" -ItemType Directory -Force | Out-Null

# Define all agents
$agents = @('backlog-review-agent', 'unit-test-agent', 'performance-test-agent')

# Create directories for each agent
Write-Host "\nCreating agent directories..." -ForegroundColor Yellow
foreach ($agent in $agents) {
    Write-Host "  Creating $agent..." -ForegroundColor Green
    
    # Create source directories
    $srcPath = "apps\$agent\src"
    New-Item -Path "$srcPath" -ItemType Directory -Force | Out-Null
    New-Item -Path "$srcPath\domain" -ItemType Directory -Force | Out-Null
    New-Item -Path "$srcPath\use-cases" -ItemType Directory -Force | Out-Null
    New-Item -Path "$srcPath\infrastructure" -ItemType Directory -Force | Out-Null
    
    # Create test directories
    $testsPath = "apps\$agent\tests"
    New-Item -Path "$testsPath" -ItemType Directory -Force | Out-Null
    New-Item -Path "$testsPath\unit" -ItemType Directory -Force | Out-Null
    New-Item -Path "$testsPath\integration" -ItemType Directory -Force | Out-Null
    New-Item -Path "$testsPath\e2e" -ItemType Directory -Force | Out-Null
    
    # Create configuration and prompt directories
    New-Item -Path "apps\$agent\config" -ItemType Directory -Force | Out-Null
    New-Item -Path "apps\$agent\prompts" -ItemType Directory -Force | Out-Null
    New-Item -Path "apps\$agent\docs\sdd" -ItemType Directory -Force | Out-Null
}

# Create shared directories
Write-Host "\nCreating shared directories..." -ForegroundColor Yellow
New-Item -Path "shared\domain" -ItemType Directory -Force | Out-Null
New-Item -Path "shared\contracts" -ItemType Directory -Force | Out-Null
New-Item -Path "shared\utilities" -ItemType Directory -Force | Out-Null
New-Item -Path "shared\types" -ItemType Directory -Force | Out-Null

# Create documentation directories
Write-Host "\nCreating documentation directories..." -ForegroundColor Yellow
New-Item -Path "docs\sdd" -ItemType Directory -Force | Out-Null
New-Item -Path "docs\adr" -ItemType Directory -Force | Out-Null
New-Item -Path "docs\api" -ItemType Directory -Force | Out-Null
New-Item -Path "docs\diagrams" -ItemType Directory -Force | Out-Null

# Create operational directories
Write-Host "\nCreating operational directories..." -ForegroundColor Yellow
New-Item -Path ".opencode\agents" -ItemType Directory -Force | Out-Null
New-Item -Path ".opencode\prompts" -ItemType Directory -Force | Out-Null
New-Item -Path ".github\workflows" -ItemType Directory -Force | Out-Null
New-Item -Path "scripts" -ItemType Directory -Force | Out-Null

# Display the created structure
Write-Host "\n===== Created Directory Structure =====" -ForegroundColor Cyan
Write-Host "AI-QA-Agents/" -ForegroundColor Yellow

foreach ($agent in $agents) {
    Write-Host "  apps/$agent/" -ForegroundColor Green
    Write-Host "    src/" -ForegroundColor White
    Write-Host "      domain/" -ForegroundColor Gray
    Write-Host "      use-cases/" -ForegroundColor Gray
    Write-Host "      infrastructure/" -ForegroundColor Gray
    Write-Host "    tests/" -ForegroundColor White
    Write-Host "      unit/" -ForegroundColor Gray
    Write-Host "      integration/" -ForegroundColor Gray
    Write-Host "      e2e/" -ForegroundColor Gray
    Write-Host "    config/" -ForegroundColor Gray
    Write-Host "    prompts/" -ForegroundColor Gray
    Write-Host "    docs/sdd/" -ForegroundColor Gray
}

Write-Host "  shared/" -ForegroundColor Green
Write-Host "    domain/" -ForegroundColor Gray
Write-Host "    contracts/" -ForegroundColor Gray
Write-Host "    utilities/" -ForegroundColor Gray
Write-Host "    types/" -ForegroundColor Gray

Write-Host "  docs/" -ForegroundColor Green
Write-Host "    sdd/" -ForegroundColor Gray
Write-Host "    adr/" -ForegroundColor Gray
Write-Host "    api/" -ForegroundColor Gray
Write-Host "    diagrams/" -ForegroundColor Gray

Write-Host "  .opencode/" -ForegroundColor Green
Write-Host "    agents/" -ForegroundColor Gray
Write-Host "    prompts/" -ForegroundColor Gray

Write-Host "  .github/workflows/" -ForegroundColor Green
Write-Host "  scripts/" -ForegroundColor Gray

Write-Host "\n===============================" -ForegroundColor Cyan
Write-Host "Directory structure created successfully!" -ForegroundColor Green

# End of Script
@@ - End of Script @@
