#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = [
    "tools/validate_v24_integrity.py",
    "tools/validate_integrity.py",
    "tools/check_verification.py",
    "tools/check_generated_drift.py",
    "tools/check_internal_paths.py",
    "tools/scan_secrets.py",
    "tools/api_revalidation_gate.py",
    "tests/test_cli_contracts.py",
    "tests/test_lab_state.py",
    "tests/test_v24_integrity.py",
    "tests/test_claim_resolution_v24.py",
    "tests/test_api_coverage_v24.py",
    "tests/test_generated_provenance_v24.py",
    "tests/test_epic_url_security.py",
    "tests/test_llm_eval_runner_v24.py",
    "tests/test_cli_v24.py",
    "tools/run_hallucination_evals.py",
]
failed = []
for rel in checks:
    path = ROOT / rel
    if not path.exists():
        failed.append((rel, "missing"))
        continue
    rc = subprocess.run([sys.executable, str(path)], cwd=ROOT).returncode
    if rc:
        failed.append((rel, f"exit={rc}"))

if failed:
    print("Validation suite FAILED")
    for rel, detail in failed:
        print("-", rel, detail)
    raise SystemExit(1)

print("Validation suite OK")
print("UEFN compile status: NOT TESTED")
print("LLM end-to-end benchmark: SKIPPED unless explicitly configured")
