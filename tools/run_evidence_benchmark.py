#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
T=json.loads((ROOT/"benchmarks/evidence_composition.json").read_text())["tasks"]
rows=[]
for t in T:
    rel=f"rag/generated/{t['id']}.md"
    subprocess.run([sys.executable,str(ROOT/"tools/rag_context_compiler.py"),t["query"],"--output",rel],
                   stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    p=(ROOT/rel).with_suffix(".json")
    d=json.loads(p.read_text()) if p.exists() else {}
    roles={x["role"] for x in d.get("sources",[])}
    miss=[x for x in t["required"] if x not in roles]
    rows.append({"id":t["id"],"passed":not miss,"missing":miss})
passed=sum(x["passed"] for x in rows)
(ROOT/"benchmarks/evidence_composition_result.json").write_text(json.dumps({"passed":passed,"total":len(rows),"tasks":rows},indent=2))
print(f"Evidence benchmark: {passed}/{len(rows)}")
for x in rows: print(x["id"],"PASS" if x["passed"] else "FAIL",x["missing"])
if passed!=len(rows): raise SystemExit(1)
