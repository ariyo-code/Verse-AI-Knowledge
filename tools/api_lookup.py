#!/usr/bin/env python3
from pathlib import Path
import json, sys, difflib
ROOT=Path(__file__).resolve().parents[1]
entries=json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8"))["entries"]
if len(sys.argv)<2:
    print("Usage: python tools/api_lookup.py <api-name>")
    raise SystemExit(2)
q=" ".join(sys.argv[1:]).strip()
if q in entries:
    print(json.dumps({q:entries[q]},indent=2,ensure_ascii=False))
else:
    matches=difflib.get_close_matches(q,entries.keys(),n=8,cutoff=.35)
    if matches:
        print("No exact match. Closest entries:")
        for x in matches: print("-",x)
    else:
        print("No local match. Verify current Epic Verse API.")
