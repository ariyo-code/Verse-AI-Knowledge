#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("baseline")
ap.add_argument("candidate")
args = ap.parse_args()
b = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
c = json.loads(Path(args.candidate).read_text(encoding="utf-8"))

keys = sorted(set((b.get("coverage") or {}).keys()) | set((c.get("coverage") or {}).keys()))
print(f"Coverage diff: {b.get('release')} -> {c.get('release')}")
print(f"Known symbols: {b.get('symbol_count')} -> {c.get('symbol_count')}")
for key in keys:
    bv = ((b.get("coverage") or {}).get(key) or {}).get("count", 0)
    cv = ((c.get("coverage") or {}).get(key) or {}).get("count", 0)
    delta = cv - bv
    sign = "+" if delta >= 0 else ""
    print(f"- {key}: {bv} -> {cv} ({sign}{delta})")
print("Note: this compares repository-known evidence, not total Epic API coverage.")
