param(
    [Parameter(Mandatory=$true)]
    [string]$VerseDir
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Python = "python"

& $Python (Join-Path $RepoRoot "tools\prepare_next_candidate.py") `
    --uefn-verse-dir $VerseDir

Write-Host ""
Write-Host "Le prochain candidat est prêt."
Write-Host "Compile maintenant Verse dans UEFN."
Write-Host "Puis utilise tools\lab_result.py."
