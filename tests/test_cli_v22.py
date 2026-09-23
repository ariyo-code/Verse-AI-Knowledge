#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
print("V22 CLI compatibility test delegates to current V23 CLI tests.")
raise SystemExit(subprocess.run([sys.executable,str(ROOT/"tests/test_cli_v23.py")],cwd=ROOT).returncode)
