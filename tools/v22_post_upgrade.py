#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
TESTS=[
    'tools/validate_v22_integrity.py',
    'tools/check_generated_drift.py',
    'tools/self_test.py',
    'tests/test_v22_integrity.py',
    'tests/test_cli_contracts.py',
    'tests/test_lab_state.py',
    'tests/test_cli_v22.py',
    'tools/validate_integrity.py',
    'tools/check_verification.py',
    'tools/validate_repo.py',
    'tools/preflight.py',
    'tools/rag_benchmark.py',
    'tools/run_evidence_benchmark.py',
    'tools/run_hallucination_evals.py',
]
rows=[]
for rel in TESTS:
    path=ROOT/rel
    if not path.exists():
        rows.append({'test':rel,'passed':False,'returncode':None,'stdout':'','stderr':'missing file'})
        continue
    proc=subprocess.run([sys.executable,str(path)],cwd=ROOT,capture_output=True,text=True)
    rows.append({'test':rel,'passed':proc.returncode==0,'returncode':proc.returncode,'stdout':proc.stdout[-6000:],'stderr':proc.stderr[-6000:]})
    print(f"[{'PASS' if proc.returncode==0 else 'FAIL'}] {rel}")
passed=sum(x['passed'] for x in rows); failed=len(rows)-passed
report={
    'release':'22.0.0',
    'generated_at':datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
    'tests_executed':len(rows),
    'tests_passed':passed,
    'tests_failed':failed,
    'uefn_tests_actually_performed':0,
    'uefn_compile_status':'NOT TESTED',
    'tests':rows,
}
reports=ROOT/'reports'; reports.mkdir(exist_ok=True)
(reports/'V22_UPGRADE_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
md=['# V22 Upgrade Test Report','',f"- Tests executed: **{len(rows)}**",f"- Passed: **{passed}**",f"- Failed: **{failed}**",'- UEFN tests actually performed: **0**','- UEFN compile status: **NOT TESTED**','','## Results','']
for row in rows: md.append(f"- {'PASS' if row['passed'] else 'FAIL'} — `{row['test']}`")
(reports/'V22_UPGRADE_REPORT.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(reports/'V22_UPGRADE_REPORT.md')
if failed: raise SystemExit(1)
