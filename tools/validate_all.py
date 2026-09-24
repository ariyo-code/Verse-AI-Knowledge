#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
checks=['tools/validate_v25_integrity.py','tools/validate_integrity.py','tools/check_verification.py','tools/check_generated_drift.py','tools/check_internal_paths.py','tools/scan_secrets.py','tools/api_revalidation_gate.py','tests/test_cli_contracts.py','tests/test_lab_state.py','tools/run_hallucination_evals.py','tests/test_epic_url_security.py']
failed=[]
for rel in checks:
 p=ROOT/rel
 if not p.exists(): failed.append((rel,'missing')); continue
 rc=subprocess.run([sys.executable,str(p)],cwd=ROOT).returncode
 if rc: failed.append((rel,f'exit={rc}'))
# Pytest new V25 suites if pytest is available
try:
 import pytest
 rc=subprocess.run([sys.executable,'-m','pytest','-q','tests/prompts','tests/security','tests/api','tests/cli','tests/retrieval'],cwd=ROOT).returncode
 if rc: failed.append(('pytest-v25',f'exit={rc}'))
except Exception: print('pytest-v25: SKIPPED — pytest not installed')
if failed:
 print('Validation suite FAILED'); [print('-',a,b) for a,b in failed]; raise SystemExit(1)
print('Validation suite OK'); print('UEFN compile status: NOT TESTED'); print('LLM end-to-end benchmark: SKIPPED unless explicitly configured')
