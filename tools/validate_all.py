#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
checks=[
 'tools/validate_v22_integrity.py','tools/validate_integrity.py','tools/check_verification.py',
 'tools/check_generated_drift.py','tests/test_cli_contracts.py','tests/test_lab_state.py',
 'tests/test_v22_integrity.py','tests/test_cli_v22.py'
]
failed=[]
for rel in checks:
    p=ROOT/rel
    if not p.exists(): failed.append((rel,'missing')); continue
    proc=subprocess.run([sys.executable,str(p)],cwd=ROOT)
    if proc.returncode: failed.append((rel,f'exit={proc.returncode}'))
if failed:
    print('Validation suite FAILED')
    for rel,why in failed: print('-',rel,why)
    raise SystemExit(1)
print('Validation suite OK')
print('UEFN compile status: NOT TESTED')
