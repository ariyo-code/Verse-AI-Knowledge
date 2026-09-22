#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))
from rag_query import score_doc,excerpt
I=json.loads((ROOT/"rag/index.json").read_text())
def role(d):
    p=d["path"].lower()
    if p.startswith("projects/"): return "project_context"
    if "docs/api/" in p or p.endswith("api_catalog.json") or p.endswith("module_catalog.json"): return "api_evidence"
    if p.startswith("errors/"): return "error_memory"
    if p.startswith("patterns/") or "lifecycle" in p or "async" in p: return "lifecycle"
    if p.startswith("mcp/") or p.startswith("lab/") or "verification" in p or "quality" in p: return "verification"
    if p.startswith("external/corpus/"): return "external_examples"
    return "supporting"
def required(q):
    q=q.lower(); r={"api_evidence","verification"}
    if any(x in q for x in ["system","vehicle","inventory","staff","cage","rp","ui"]): r.add("project_context")
    if "error" in q or "compiler" in q: r.add("error_memory")
    if any(x in q for x in ["cleanup","lifecycle","leave","join","respawn","async","race","spawn"]): r.add("lifecycle")
    return sorted(r)
ap=argparse.ArgumentParser(); ap.add_argument("query"); ap.add_argument("--output",default="rag/generated/EVIDENCE_PACK.md"); a=ap.parse_args()
rows=[]
for d in I["documents"]:
    s,m=score_doc(a.query,d)
    if s>0: rows.append((s,d,m))
rows.sort(key=lambda x:(-x[0],x[1]["path"]))
req=required(a.query); chosen=[]; used=set()
for rr in req:
    cand=next((x for x in rows if role(x[1])==rr and x[1]["path"] not in used),None)
    if cand: chosen.append((rr,*cand)); used.add(cand[1]["path"])
for rr in ["project_context","api_evidence","lifecycle","error_memory","verification","external_examples"]:
    if len(chosen)>=10: break
    cand=next((x for x in rows if role(x[1])==rr and x[1]["path"] not in used),None)
    if cand: chosen.append((rr,*cand)); used.add(cand[1]["path"])
for x in rows:
    if len(chosen)>=12: break
    if x[1]["path"] not in used: chosen.append((role(x[1]),*x)); used.add(x[1]["path"])
packed=[]
for rr,s,d,m in chosen:
    packed.append({"role":rr,"score":round(s,3),"trust":round(m["trust"],2),"path":d["path"],
                   "title":d["title"],"status":d.get("status"),"verification":d.get("verification"),
                   "excerpt":excerpt(d["path"],a.query,max_chars=1500)})
present={x["role"] for x in packed}; missing=[x for x in req if x not in present]
lines=["# Evidence Pack","",f"Query: `{a.query}`","",f"Required: {', '.join(req)}",f"Missing: {', '.join(missing) or 'none'}","",
       "## Claim guard","",
       "- Planned docs do not prove exact API signatures.",
       "- Module-index evidence proves presence only.",
       "- External examples are not local compile proof.",
       "- UEFN compiler/runtime overrides repository claims.",""]
for i,x in enumerate(packed,1):
    lines += [f"## {i}. {x['role']} — `{x['path']}`","",f"- trust: `{x['trust']}`",
              f"- verification: `{x['verification']}`","", "```text",x["excerpt"],"```",""]
out=ROOT/a.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\n".join(lines))
out.with_suffix(".json").write_text(json.dumps({"query":a.query,"required_roles":req,"missing_required_roles":missing,
                                                "sources":[{k:v for k,v in x.items() if k!="excerpt"} for x in packed]},indent=2))
print(f"Evidence sources: {len(packed)}")
print(f"Missing roles: {missing}")
if missing: raise SystemExit(2)
