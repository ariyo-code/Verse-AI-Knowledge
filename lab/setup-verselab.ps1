param(
    [Parameter(Mandatory=$true)]
    [string]$VerseDir
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = "python"

Write-Host "=== VerseLab Setup ==="

if (-not (Get-Command $Python -ErrorAction SilentlyContinue)) {
    throw "Python n'est pas disponible dans PATH."
}

New-Item -ItemType Directory -Force -Path $VerseDir | Out-Null

$Corpus = Join-Path $RepoRoot "external\corpus\uefncentral-examples"

if (-not (Test-Path $Corpus)) {
    Write-Host "Synchronisation du corpus UEFN Central..."
    & $Python (Join-Path $RepoRoot "tools\sync_external_sources.py") `
        --source uefncentral-examples `
        --verse-only
}

Write-Host "Reconstruction du RAG..."
& $Python (Join-Path $RepoRoot "tools\rag_build_index.py")

$Queue = Join-Path $RepoRoot "lab\compile_queue.json"
if (-not (Test-Path $Queue)) {
    & $Python (Join-Path $RepoRoot "tools\curate_external_examples.py") `
        --source uefncentral-examples `
        --limit 100

    & $Python (Join-Path $RepoRoot "tools\build_compile_queue.py") `
        --limit 50
}

& $Python (Join-Path $RepoRoot "tools\build_compile_batches.py")
& $Python (Join-Path $RepoRoot "tools\lab_doctor.py") `
    --verse-dir $VerseDir

Write-Host ""
Write-Host "VerseLab prêt."
Write-Host "Commande suivante:"
Write-Host ".\lab\next-candidate.ps1 -VerseDir `"$VerseDir`""
