#!/usr/bin/env python3
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

for path in (ROOT/"verification").glob("*.json"):
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.name}: invalid JSON: {exc}")
        continue

    status=data.get("status")
    checks=data.get("checks",{})
    compiled=bool(checks.get("compiled"))
    runtime=bool(checks.get("runtime_tested"))
    multi=bool(checks.get("multiplayer_tested"))

    if status in {"compiled","verified","multiplayer-verified"} and not compiled:
        errors.append(f"{path.name}: {status} requires compiled=true")
    if status in {"verified","multiplayer-verified"} and not runtime:
        errors.append(f"{path.name}: {status} requires runtime_tested=true")
    if status=="multiplayer-verified" and not multi:
        errors.append(f"{path.name}: multiplayer-verified requires multiplayer_tested=true")

if errors:
    print("Verification evidence FAILED")
    for e in errors: print("-",e)
    sys.exit(1)

print("Verification evidence OK")
