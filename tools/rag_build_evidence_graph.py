#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
I=json.loads((ROOT/"rag/index.json").read_text())
nodes=[]; edges=[]; seen=set()
def add(x):
    if x["id"] not in seen: seen.add(x["id"]); nodes.append(x)
for d in I["documents"]:
    did="doc:"+d["id"]; add({"id":did,"kind":"document","path":d["path"],"title":d["title"]})
    for api in d.get("api_symbols",[]):
        aid="api:"+api; add({"id":aid,"kind":"api","name":api}); edges.append({"from":did,"to":aid,"type":"mentions_api"})
out={"schema_version":1,"node_count":len(nodes),"edge_count":len(edges),"nodes":nodes,"edges":edges}
(ROOT/"rag/evidence_graph.json").write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(f"Evidence graph: {len(nodes)} nodes, {len(edges)} edges")
