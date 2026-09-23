#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"
CURRENT=ROOT/"lab/current_candidate.json"

q=json.loads(QUEUE.read_text(encoding="utf-8"))
entries=q.get("entries",[])
counts=Counter(e.get("queue_status","unknown") for e in entries)

print("=== VerseLab Status ===")
print(f"Total: {len(entries)}")
for k in [
    "pending","staged","compiling","compile-failed",
    "blocked-environment","compiled","runtime-pending",
    "verified","multiplayer-verified","skipped"
]:
    if counts[k]:
        print(f"{k}: {counts[k]}")

if CURRENT.exists():
    c=json.loads(CURRENT.read_text(encoding="utf-8"))
    print()
    print("Active candidate:")
    print(c["candidate_id"])
    print(c["source_path"])
else:
    print()
    print("Active candidate: none")
