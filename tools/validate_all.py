#!/usr/bin/env python3
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

required=[
    "AGENTS.md","manifest.json","lab/compile_queue.json",
    "tests/test_cli_contracts.py","tools/validate_integrity.py",
    "tools/build_claim_ledger.py","schemas/claim_ledger.schema.json",
    "tools/preflight.py","docs/architecture/CLAIM_LEDGER.md"
]
for rel in required:
    if not (ROOT/rel).exists():
        errors.append("missing: "+rel)

m=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
if m.get("schema_version",0)<19:
    errors.append("schema_version < 19")

q=json.loads((ROOT/"lab/compile_queue.json").read_text(encoding="utf-8"))
if len(q.get("entries",[]))!=50:
    errors.append(f"expected 50 queue entries, got {len(q.get('entries',[]))}")

# Static CLI checks.
cli={
    "tools/scan_verse_project.py":["--output"],
    "tools/corpus_coverage.py":["--json"],
    "tools/analyze_verse_dependencies.py":["--output"],
    "tools/rag_context_compiler.py":["--output"],
    "tools/build_claim_ledger.py":["--evidence","--output"],
}
for rel,flags in cli.items():
    p=ROOT/rel
    if not p.exists():
        errors.append("missing script: "+rel)
        continue
    text=p.read_text(encoding="utf-8",errors="ignore")
    for f in flags:
        if f not in text:
            errors.append(f"{rel}: missing flag {f}")

# Status integrity.
for e in q.get("entries",[]):
    st=e.get("queue_status")
    v=e.get("local_verification",{})
    if st in {"compiled","verified","multiplayer-verified"} and not v.get("compiled"):
        errors.append(f"{e.get('candidate_id')}: invalid compiled status")
    if st=="multiplayer-verified" and not v.get("multiplayer_tested"):
        errors.append(f"{e.get('candidate_id')}: invalid multiplayer status")

if errors:
    print("Validation suite FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)

print("Validation suite PASS")
