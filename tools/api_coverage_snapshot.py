#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--release")
ap.add_argument("--output")
args = ap.parse_args()

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
coverage = json.loads((ROOT / "knowledge/api/coverage.json").read_text(encoding="utf-8"))
release = args.release or manifest.get("release", {}).get("version", "unknown")
snapshot = {
    "schema_version": 1,
    "generated_by": "tools/api_coverage_snapshot.py",
    "release": release,
    "api_version": coverage.get("api_version"),
    "symbol_count": coverage.get("symbol_count"),
    "module_count": coverage.get("module_count"),
    "coverage": coverage.get("coverage"),
    "source_trust_breakdown": coverage.get("source_trust_breakdown"),
    "validation_breakdown": coverage.get("validation_breakdown"),
    "claim_state_breakdown": coverage.get("claim_state_breakdown"),
    "revalidation": coverage.get("revalidation"),
    "note": coverage.get("note"),
}
out = Path(args.output) if args.output else ROOT / "reports/api-coverage" / f"v{release.split('.')[0]}.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
