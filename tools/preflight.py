#!/usr/bin/env python3
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
checks=[]

def check(name,ok,detail):
    checks.append({"name":name,"passed":bool(ok),"detail":detail})

m=json.loads((ROOT/"manifest.json").read_text(encoding="utf-8"))
check("schema",m.get("schema_version",0)>=19,f"schema={m.get('schema_version')}")

q=json.loads((ROOT/"lab/compile_queue.json").read_text(encoding="utf-8"))
check("compile queue",len(q.get("entries",[]))==50,f"entries={len(q.get('entries',[]))}")

cm=json.loads((ROOT/"external/corpus_manifest.json").read_text(encoding="utf-8"))
base=ROOT/"external/corpus"/cm["source_id"]/cm["source_revision"]/"examples"
local=len(list(base.rglob("*.verse"))) if base.exists() else 0
check("starter corpus",local>0,f"local examples={local}/{cm['expected_examples']}")


check("evidence compiler",(ROOT/"tools/rag_context_compiler.py").exists(),"context compiler present")
check("claim ledger",(ROOT/"tools/build_claim_ledger.py").exists(),"claim ledger present")

ok=all(x["passed"] for x in checks)
dest=ROOT/"reports/PREFLIGHT.json"
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps({"passed":ok,"checks":checks},indent=2,ensure_ascii=False),encoding="utf-8")

print("Preflight:", "PASS" if ok else "FAIL")
for x in checks:
    print(f"[{'PASS' if x['passed'] else 'FAIL'}] {x['name']} - {x['detail']}")
if not ok:
    sys.exit(1)
