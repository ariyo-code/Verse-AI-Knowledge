@echo off
setlocal EnableExtensions
cd /d "%~dp0\.."

echo.
echo ============================================
echo   Verse-AI-Knowledge - VerseLab One Click
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [ERREUR] Python n'est pas disponible dans PATH.
  pause
  exit /b 1
)

python tools\detect_uefn_verse_dir.py --interactive
if errorlevel 1 (
  echo.
  echo [ERREUR] Aucun dossier Verse valide n'a ete selectionne.
  pause
  exit /b 1
)

for /f "usebackq delims=" %%i in ("lab\generated\verse_dir.txt") do set "VERSE_DIR=%%i"

echo.
echo Dossier Verse:
echo %VERSE_DIR%
echo.

python tools\lab_doctor.py --verse-dir "%VERSE_DIR%"
if errorlevel 1 (
  echo.
  echo [INFO] Le corpus complet n'est peut-etre pas synchronise.
  echo Le Batch 001 embarque est quand meme disponible.
)

echo.
echo Preparation du prochain candidat...
python tools\prepare_next_candidate.py --uefn-verse-dir "%VERSE_DIR%"
if errorlevel 1 (
  echo.
  echo [ERREUR] Impossible de preparer le candidat.
  pause
  exit /b 1
)

python tools\generate_active_candidate_instructions.py

echo.
echo ============================================
echo   CANDIDAT PRET
echo ============================================
echo.
echo 1. Ouvre UEFN.
echo 2. Lance "Build Verse Code".
echo 3. Reviens ici et ouvre:
echo    lab\generated\AFTER_COMPILE.txt
echo.
pause
endlocal
