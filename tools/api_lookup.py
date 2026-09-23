#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.api_index import lookup  # noqa: E402

if len(sys.argv) < 2:
    print("Usage: python tools/api_lookup.py <api-name>")
    raise SystemExit(2)
query = " ".join(sys.argv[1:]).strip()
row, suggestions = lookup(query, ROOT)
if row:
    print(json.dumps(row, indent=2, ensure_ascii=False))
    if row.get("signature") and not row.get("exact_signature_claim_allowed"):
        print("WARNING: exact signature not verified. TODO(API VERIFY)")
else:
    print("No exact structured match.")
    for item in suggestions:
        print("-", item)
    print("TODO(API VERIFY)")
    raise SystemExit(2)
