#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
proc = subprocess.run(
    [sys.executable, str(ROOT / "evals/llm/runner.py")],
    cwd=ROOT,
    capture_output=True,
    text=True,
)
assert proc.returncode == 0
assert "SKIPPED" in proc.stdout
assert "PASS" not in proc.stdout
print("V24 LLM eval runner default-skip test OK")
