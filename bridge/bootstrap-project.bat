@echo off
setlocal

if "%~2"=="" (
  echo Usage:
  echo   bootstrap-project.bat "C:\Path\To\UEFNProject" "Project Name"
  exit /b 1
)

powershell -ExecutionPolicy Bypass -File "%~dp0bootstrap-project.ps1" ^
  -ProjectPath "%~1" ^
  -ProjectName "%~2"

endlocal
