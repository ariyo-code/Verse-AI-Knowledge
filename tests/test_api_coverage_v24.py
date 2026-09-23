#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
rows = [json.loads(x) for x in (ROOT / "knowledge/api/symbols.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
coverage = json.loads((ROOT / "knowledge/api/coverage.json").read_text(encoding="utf-8"))
queue = json.loads((ROOT / "knowledge/api/verification_queue.json").read_text(encoding="utf-8"))

assert coverage["symbol_count"] == len(rows)
assert coverage["coverage"]["presence"]["count"] == len(rows)
assert coverage["coverage"]["signature_verified"]["count"] == sum(bool(r.get("exact_signature_claim_allowed")) for r in rows)
assert queue["pending_count"] == sum(not bool(r.get("exact_signature_claim_allowed")) for r in rows)
assert "total Epic" not in coverage.get("note", "")

v23 = ROOT / "reports/api-coverage/v23.json"
v24 = ROOT / "reports/api-coverage/v24.json"
assert v23.exists() and v24.exists()
b = json.loads(v23.read_text(encoding="utf-8"))
c = json.loads(v24.read_text(encoding="utf-8"))
assert c["coverage"]["signature_verified"]["count"] >= b["coverage"]["signature_verified"]["count"]

proc = subprocess.run(
    [sys.executable, str(ROOT / "tools/api_coverage_diff.py"), str(v23), str(v24)],
    cwd=ROOT,
    capture_output=True,
    text=True,
)
assert proc.returncode == 0
assert "Coverage diff" in proc.stdout
assert "not total Epic API coverage" in proc.stdout

print("V24 API coverage tests OK")
