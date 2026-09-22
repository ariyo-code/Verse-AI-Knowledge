#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8"))
entries=data["entries"]
by_verification=Counter(v.get("verification","unspecified") for v in entries.values())
by_module=Counter(v.get("module","unspecified") for v in entries.values())
print(f"Verse API snapshot: {data.get('verse_api_version')}")
print(f"Last verified: {data.get('last_verified')}")
print(f"Catalog entries: {len(entries)}")
print("Verification classes:")
for k,n in sorted(by_verification.items()):
    print(f"- {k}: {n}")
print("Top modules:")
for k,n in by_module.most_common(10):
    print(f"- {k}: {n}")
