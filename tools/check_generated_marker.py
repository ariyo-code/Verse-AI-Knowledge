#!/usr/bin/env python3
from pathlib import Path
import argparse
import re

PAT = re.compile(r"<!--\s*verse-ai-generated:v24;([^>]*)-->")
STATUS = {"draft", "static-checked", "compiled", "verified", "multiplayer-verified"}
FORBIDDEN = (
    "\u200b", "\u200c", "\u200d", "\u2060", "\ufeff",
    "\u202a", "\u202b", "\u202c", "\u202d", "\u202e",
    "\u2066", "\u2067", "\u2068", "\u2069",
)

def as_bool(value):
    return str(value).lower() == "true"

ap = argparse.ArgumentParser()
ap.add_argument("file", nargs="?")
args = ap.parse_args()
files = [Path(args.file)] if args.file else list(Path(".").rglob("*.md"))
errors = []
found = 0

for path in files:
    text = path.read_text(encoding="utf-8", errors="ignore")
    for ch in FORBIDDEN:
        if ch in text:
            errors.append(f"{path}: forbidden invisible/bidi Unicode U+{ord(ch):04X}")
    for n, match in enumerate(PAT.finditer(text), 1):
        found += 1
        before = text[max(0, match.start() - 4000):match.start()]
        if "Verse AI Knowledge · V24" not in before:
            errors.append(f"{path}: marker {n}: visible V24 provenance block not found before hidden marker")
        data = {}
        for token in match.group(1).split(";"):
            if "=" in token:
                k, v = token.split("=", 1)
                data[k.strip()] = v.strip()
        status = data.get("status")
        compiled = as_bool(data.get("compiled"))
        runtime = as_bool(data.get("runtime"))
        multiplayer = as_bool(data.get("multiplayer"))
        try:
            uncertain = int(data.get("uncertain_api_count", "0") or 0)
        except ValueError:
            errors.append(f"{path}: marker {n}: invalid uncertain_api_count")
            uncertain = 0
        if status not in STATUS:
            errors.append(f"{path}: marker {n}: invalid status {status}")
        if status in {"compiled", "verified", "multiplayer-verified"} and not compiled:
            errors.append(f"{path}: marker {n}: {status} requires compiled=true")
        if status in {"verified", "multiplayer-verified"} and not runtime:
            errors.append(f"{path}: marker {n}: {status} requires runtime=true")
        if status == "multiplayer-verified" and not multiplayer:
            errors.append(f"{path}: marker {n}: multiplayer-verified requires multiplayer=true")
        if runtime and not compiled:
            errors.append(f"{path}: marker {n}: runtime=true requires compiled=true")
        if multiplayer and not runtime:
            errors.append(f"{path}: marker {n}: multiplayer=true requires runtime=true")
        if uncertain > 0 and data.get("api_verify_required") != "true":
            errors.append(f"{path}: marker {n}: unresolved API count requires api_verify_required=true")
        if data.get("claim_resolution") != "field-level":
            errors.append(f"{path}: marker {n}: claim_resolution must be field-level")

if errors:
    print("Generated marker validation FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print(f"Generated marker validation OK ({found} V24 marker(s) inspected)")
