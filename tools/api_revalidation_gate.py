#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--strict", action="store_true")
args = ap.parse_args()

state = json.loads((ROOT / "knowledge/api/revalidation_state.json").read_text(encoding="utf-8"))
print("API snapshot:", state.get("api_version"))
print("Stale symbols:", state.get("stale_symbol_count", 0))
print("Stale verified evidence:", state.get("stale_verified_evidence_count", 0))
if state.get("stale_verified_evidence_ids"):
    for item in state["stale_verified_evidence_ids"]:
        print("-", item)
if args.strict and state.get("stale_verified_evidence_count", 0):
    raise SystemExit(1)
