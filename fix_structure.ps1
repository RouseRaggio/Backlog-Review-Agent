# PowerShell script to fix AI-QA-Agents directory structure
# This fixes the issues with foreach loops and quoting

$base = 'C:\Users\User\Documents\AI-QA-Agents'
Set-Location $base

Write-Host 'Fixing AI-QA-Agents directory structure...' -ForegroundColor Yellow

# Fix agent directories
$agents = @('backlog-review-agent')

$agentLoop = {
    param($agent)
    $agentPath = "apps\$agent"
    
    Write-Host "  Creating $agent structure..." -ForegroundColor Gray
    
    # Create source directories
    New-Item -Path "$agentPath\src\domain\entities" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\domain\rules" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\domain\services" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\application\use_cases" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\infrastructure\configuration" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\infrastructure\jira" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\presentation\cli" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\presentation\html\templates" -ItemType Directory -Force
    New-Item -Path "$agentPath\src\bootstrap" -ItemType Directory -Force
    
    # Create test directories
    New-Item -Path "$agentPath\tests\unit" -ItemType Directory -Force
    New-Item -Path "$agentPath\tests\integration" -ItemType Directory -Force
    New-Item -Path "$agentPath\tests\e2e" -ItemType Directory -Force
    New-Item -Path "$agentPath\tests\fixtures" -ItemType Directory -Force
    
    # Create config directories
    New-Item -Path "$agentPath\config" -ItemType Directory -Force
    New-Item -Path "$agentPath\tools" -ItemType Directory -Force
    New-Item -Path "$agentPath\docs\adr" -ItemType Directory -Force
    New-Item -Path "$agentPath\docs\api" -ItemType Directory -Force
    New-Item -Path "$agentPath\docs\diagrams" -ItemType Directory -Force
    New-Item -Path "$agentPath\docs\sdd" -ItemType Directory -Force
    New-Item -Path "$agentPath\docs\srs" -ItemType Directory -Force
}

# Execute for each agent
foreach ($agent in $agents) {
    & $agentLoop -agent $agent
}

# Fix shared directories
Write-Host '  Fixing shared directories...' -ForegroundColor Gray
New-Item -Path 'shared\domain' -ItemType Directory -Force
New-Item -Path 'shared\contracts' -ItemType Directory -Force
New-Item -Path 'shared\utilities' -ItemType Directory -Force
New-Item -Path 'shared\types' -ItemType Directory -Force

# Fix docs directories
Write-Host '  Fixing docs directories...' -ForegroundColor Gray
New-Item -Path 'docs\sdd' -ItemType Directory -Force
New-Item -Path 'docs\adr' -ItemType Directory -Force
New-Item -Path 'docs\api' -ItemType Directory -Force
New-Item -Path 'docs\diagrams' -ItemType Directory -Force

# Fix opencode directories
Write-Host '  Fixing .opencode directories...' -ForegroundColor Gray
New-Item -Path '.opencode\agents' -ItemType Directory -Force
New-Item -Path '.opencode\prompts' -ItemType Directory -Force
New-Item -Path '.github\workflows' -ItemType Directory -Force
New-Item -Path 'scripts' -ItemType Directory -Force

Write-Host '\nDirectory structure fixed successfully!' -ForegroundColor Green

# Display final structure
Write-Host '\n=== Final Directory Structure ===' -ForegroundColor Cyan
Write-Host 'AI-QA-Agents/' -ForegroundColor Yellow

$agents = @('backlog-review-agent')

foreach ($agent in $agents) {
    Write-Host "  apps/$agent/" -ForegroundColor Green
    Write-Host "    src/" -ForegroundColor White
    Write-Host "      domain/" -ForegroundColor Gray
    Write-Host "        entities/" -ForegroundColor Gray
    Write-Host "        rules/" -ForegroundColor Gray
    Write-Host "        services/" -ForegroundColor Gray
    Write-Host "      application/" -ForegroundColor Gray
    Write-Host "        use_cases/" -ForegroundColor Gray
    Write-Host "      infrastructure/" -ForegroundColor Gray
    Write-Host "        configuration/" -ForegroundColor Gray
    Write-Host "        jira/" -ForegroundColor Gray
    Write-Host "      presentation/" -ForegroundColor Gray
    Write-Host "        cli/" -ForegroundColor Gray
    Write-Host "        html/" -ForegroundColor Gray
    Write-Host "      bootstrap/" -ForegroundColor Gray
    Write-Host "    tests/" -ForegroundColor White
    Write-Host "      unit/" -ForegroundColor Gray
    Write-Host "      integration/" -ForegroundColor Gray
    Write-Host "      e2e/" -ForegroundColor Gray
    Write-Host "    config/" -ForegroundColor Gray
    Write-Host "    tools/" -ForegroundColor Gray
    Write-Host "    docs/" -ForegroundColor Gray
    Write-Host "      adr/" -ForegroundColor Gray
    Write-Host "      api/" -ForegroundColor Gray
    Write-Host "      diagrams/" -ForegroundColor Gray
    Write-Host "      sdd/" -ForegroundColor Gray
    Write-Host "      srs/" -ForegroundColor Gray
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

Write-Host '\n===============================' -ForegroundColor Cyan
