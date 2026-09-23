#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.claims import resolve_claim  # noqa: E402

ap = argparse.ArgumentParser(description="Resolve one Verse API claim against V24 field-level evidence.")
ap.add_argument("symbol")
ap.add_argument("--field", default="presence", choices=[
    "presence", "module", "kind", "signature", "parameters",
    "return_type", "effects", "event_names", "event_payloads", "member_names"
])
ap.add_argument("--json", action="store_true")
args = ap.parse_args()

result = resolve_claim(args.symbol, args.field, root=ROOT)
if args.json:
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print(f"{result['symbol']} :: {result['field']} -> {result['decision']}")
    print(result["reason"])
    if result.get("evidence_ids"):
        print("Evidence:", ", ".join(result["evidence_ids"]))
    if result.get("suggestions"):
        print("Closest known symbols:")
        for item in result["suggestions"]:
            print("-", item)
raise SystemExit(0 if result["supported"] else 2)
