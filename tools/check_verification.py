#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

for path in (ROOT / "verification").rglob("*.json"):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        continue

    validation = data.get("validation") or data.get("status")
    checks = data.get("checks", {})
    static_checked = bool(checks.get("static_checked", True if validation in {"compiled", "verified", "multiplayer-verified"} else False))
    compiled = bool(checks.get("compiled"))
    runtime = bool(checks.get("runtime_tested"))
    multiplayer = bool(checks.get("multiplayer_tested"))

    if validation in {"static-checked", "compiled", "verified", "multiplayer-verified"} and not static_checked:
        errors.append(f"{path.relative_to(ROOT)}: {validation} requires static_checked=true")
    if validation in {"compiled", "verified", "multiplayer-verified"} and not compiled:
        errors.append(f"{path.relative_to(ROOT)}: {validation} requires compiled=true")
    if validation in {"verified", "multiplayer-verified"} and not runtime:
        errors.append(f"{path.relative_to(ROOT)}: {validation} requires runtime_tested=true")
    if validation == "multiplayer-verified" and not multiplayer:
        errors.append(f"{path.relative_to(ROOT)}: multiplayer-verified requires multiplayer_tested=true")

if errors:
    print("Verification evidence FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)
print("Verification evidence OK")
