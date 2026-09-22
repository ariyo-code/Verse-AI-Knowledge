param(
    [Parameter(Mandatory=$true)]
    [string]$ProjectPath,

    [Parameter(Mandatory=$true)]
    [string]$ProjectName,

    [int]$ContextBudget = 18000
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = "python"

Write-Host ""
Write-Host "=== Verse AI Knowledge — Real Project Bridge ==="
Write-Host "Project: $ProjectName"
Write-Host "Path:    $ProjectPath"
Write-Host ""

if (-not (Test-Path $ProjectPath)) {
    throw "Project path does not exist: $ProjectPath"
}

$Generated = Join-Path $RepoRoot "bridge\generated"
New-Item -ItemType Directory -Force -Path $Generated | Out-Null

$Scan = Join-Path $Generated "project_scan.json"

& $Python (Join-Path $RepoRoot "tools\scan_verse_project.py") `
    $ProjectPath `
    --output $Scan

& $Python (Join-Path $RepoRoot "tools\create_project_profile.py") `
    $Scan `
    --name $ProjectName `
    --output-dir (Join-Path $Generated "project_profile")

& $Python (Join-Path $RepoRoot "tools\rag_build_index.py")

$Task = "Understand and safely work on UEFN project: $ProjectName. Prioritize actual project files, project lifecycle, current Verse API, known errors, and multiplayer correctness."

& $Python (Join-Path $RepoRoot "tools\rag_context_pack.py") `
    $Task `
    --budget $ContextBudget `
    --output (Join-Path $Generated "PROJECT_CONTEXT.md")

& $Python (Join-Path $RepoRoot "tools\bridge_status.py") `
    --project-path $ProjectPath `
    --project-name $ProjectName `
    --scan $Scan `
    --output (Join-Path $Generated "BRIDGE_STATUS.json")

Write-Host ""
Write-Host "Bridge ready."
Write-Host "Read:"
Write-Host "  bridge\generated\PROJECT_CONTEXT.md"
Write-Host "  bridge\generated\BRIDGE_STATUS.json"
Write-Host ""
