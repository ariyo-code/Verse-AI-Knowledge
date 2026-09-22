#!/usr/bin/env python3
from pathlib import Path
import json
from rag_query import retrieve

ROOT=Path(__file__).resolve().parents[1]
cases=json.loads((ROOT/"rag/retrieval_benchmark.json").read_text(encoding="utf-8"))["cases"]

passed=0
for case in cases:
    rows=retrieve(case["query"],10)
    paths=[doc["path"] for _,doc,_ in rows]
    ok=any(x in paths for x in case["must_include_any"])
    print(("PASS" if ok else "FAIL"),case["id"],case["query"])
    if not ok:
        print(" expected one of:",case["must_include_any"])
        print(" got:",paths[:10])
    passed+=int(ok)

print(f"{passed}/{len(cases)} retrieval cases passed")
raise SystemExit(0 if passed==len(cases) else 1)
