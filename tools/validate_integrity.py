#!/usr/bin/env python3
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

q=json.loads((ROOT/"lab/compile_queue.json").read_text(encoding="utf-8"))
for e in q.get("entries",[]):
    status=e.get("queue_status")
    v=e.get("local_verification",{})
    if status in {"compiled","verified","multiplayer-verified"} and not v.get("compiled"):
        errors.append(f"{e.get('candidate_id')}: {status} but compiled=false")
    if status=="verified" and not v.get("runtime_tested"):
        errors.append(f"{e.get('candidate_id')}: verified but runtime_tested=false")
    if status=="multiplayer-verified" and not v.get("multiplayer_tested"):
        errors.append(f"{e.get('candidate_id')}: multiplayer-verified but multiplayer_tested=false")

compiled=ROOT/"examples/compiled"
if compiled.exists():
    for p in compiled.rglob("metadata.json"):
        m=json.loads(p.read_text(encoding="utf-8"))
        if m.get("status")=="compiled" and not m.get("local_verification",{}).get("compiled"):
            errors.append(f"{p.relative_to(ROOT)}: compiled without local evidence")

if errors:
    print("Integrity validation FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)

print("Integrity validation OK")
