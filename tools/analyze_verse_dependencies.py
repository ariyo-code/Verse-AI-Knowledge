#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/"knowledge/api_catalog.json").read_text())
C=raw.get("entries",{})
if not isinstance(C,dict):
    C={x.get("name"):x for x in C if isinstance(x,dict) and x.get("name")}
U=re.compile(r"^\s*using\s*\{\s*([^}]+)\s*\}",re.M)
CL=re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*class")
DEV=re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*_device)\b")
ap=argparse.ArgumentParser(); ap.add_argument("path"); ap.add_argument("--output",required=True); a=ap.parse_args()
base=ROOT/a.path
files=[base] if base.is_file() else sorted(base.rglob("*.verse"))
decl={}
for p in files:
    for x in CL.findall(p.read_text(encoding="utf-8",errors="ignore")): decl.setdefault(x,[]).append(p)
rows=[]; mods=defaultdict(list); devs=defaultdict(list); apis=defaultdict(list); custom=defaultdict(list)
for p in files:
    t=p.read_text(encoding="utf-8",errors="ignore"); rel=str(p.relative_to(ROOT)).replace("\\","/")
    own=set(CL.findall(t)); cs=sorted(x for x in decl if x not in own and re.search(r"\b"+re.escape(x)+r"\b",t))
    row={"path":rel,"imports":sorted(set(x.strip() for x in U.findall(t))),
         "declared_classes":sorted(own),"device_types":sorted(set(DEV.findall(t))),
         "api_symbols":sorted(x for x in C if x and x in t),"cross_file_custom_dependencies":cs}
    rows.append(row)
    for x in row["imports"]: mods[x].append(rel)
    for x in row["device_types"]: devs[x].append(rel)
    for x in row["api_symbols"]: apis[x].append(rel)
    for x in cs: custom[x].append(rel)
out={"schema_version":1,"scope":a.path,"verse_files":len(rows),"files":rows,
     "indexes":{"modules":dict(mods),"devices":dict(devs),"api_symbols":dict(apis),
                "cross_file_custom_dependencies":dict(custom)},
     "warning":"Static analysis only; UEFN is authoritative."}
dest=ROOT/a.output; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(f"Dependency analysis: {len(rows)} Verse file(s)")
print(f"Modules={len(mods)} Devices={len(devs)} APIs={len(apis)} CustomDeps={len(custom)}")
