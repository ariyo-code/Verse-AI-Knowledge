#!/usr/bin/env python3
"""Compatibility shim for old automation. V24 is the current integrity model."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
print("V22 integrity validator is deprecated; delegating to V24.")
raise SystemExit(subprocess.run([sys.executable,str(ROOT/"tools/validate_v24_integrity.py")],cwd=ROOT).returncode)
