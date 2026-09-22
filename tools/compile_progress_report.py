#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"

q=json.loads(QUEUE.read_text(encoding="utf-8"))
entries=q.get("entries",[])
status=Counter(x.get("queue_status","unknown") for x in entries)
by_cat=defaultdict(Counter)

for x in entries:
    by_cat[x.get("category","unknown")][x.get("queue_status","unknown")]+=1

print(f"Candidates: {len(entries)}")
for k,n in sorted(status.items()):
    print(f"- {k}: {n}")

print()
print("By category:")
for cat,c in sorted(by_cat.items()):
    summary=", ".join(f"{k}={v}" for k,v in sorted(c.items()))
    print(f"- {cat}: {summary}")
