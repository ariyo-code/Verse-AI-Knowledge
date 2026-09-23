#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "knowledge/api_catalog.json").read_text(encoding="utf-8"))
entries = data["entries"]
trust = Counter(v.get("source_trust", "unknown") for v in entries.values())
validation = Counter(v.get("validation", "draft") for v in entries.values())
legacy_basis = Counter(v.get("evidence_basis", v.get("verification", "unspecified")) for v in entries.values())
print(f"Verse API snapshot: {data.get('verse_api_version')}")
print(f"Last verified: {data.get('last_verified')}")
print(f"Catalog entries: {len(entries)}")
print("Source trust:")
for key, count in sorted(trust.items()):
    print(f"- {key}: {count}")
print("Local validation:")
for key, count in sorted(validation.items()):
    print(f"- {key}: {count}")
print("Legacy/evidence basis:")
for key, count in sorted(legacy_basis.items()):
    print(f"- {key}: {count}")
