#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
systems_dir=ROOT/"projects/rp-framework/systems"

nodes=[]
edges=[]

for manifest in sorted(systems_dir.glob("*/system.json")):
    data=json.loads(manifest.read_text(encoding="utf-8"))
    sid=data["id"]
    nodes.append({
        "id":sid,
        "name":data.get("name"),
        "status":data.get("status")
    })
    for dep in data.get("dependencies",[]):
        edges.append({
            "from":sid,
            "to":dep,
            "type":"depends-on"
        })

graph={"nodes":nodes,"edges":edges}
out=ROOT/"projects/rp-framework/dependency_graph.json"
out.write_text(json.dumps(graph,indent=2,ensure_ascii=False),encoding="utf-8")
print(f"{len(nodes)} systems, {len(edges)} dependency edges")
