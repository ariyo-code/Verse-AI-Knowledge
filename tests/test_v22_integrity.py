#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
print("V22 compatibility test delegates to current V23 integrity tests.")
raise SystemExit(subprocess.run([sys.executable,str(ROOT/"tests/test_v23_integrity.py")],cwd=ROOT).returncode)
