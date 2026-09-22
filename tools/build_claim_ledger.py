#!/usr/bin/env python3
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[1]

ap=argparse.ArgumentParser()
ap.add_argument("--evidence",default="rag/generated/EVIDENCE_PACK.json")
ap.add_argument("--output",default="rag/generated/CLAIM_LEDGER.json")
a=ap.parse_args()

src=ROOT/a.evidence
if not src.exists():
    raise SystemExit(f"Missing evidence manifest: {src}")

d=json.loads(src.read_text(encoding="utf-8"))
sources=d.get("sources",[])
roles={}
for s in sources:
    roles.setdefault(s.get("role"),[]).append(s)

def paths(role):
    return [x.get("path") for x in roles.get(role,[]) if x.get("path")]

claims=[]

for claim,role,reason in [
    ("project_intent","project_context","Project sources/manifests support project intent/current structure."),
    ("api_presence","api_evidence","API evidence supports presence according to its verification level."),
    ("lifecycle_guidance","lifecycle","Lifecycle sources support cleanup/lifecycle guidance."),
    ("observed_error","error_memory","Only stored observed errors support an error-memory claim."),
    ("verification_procedure","verification","Verification sources explain how to validate."),
    ("external_pattern","external_examples","External examples support patterns/upstream claims only.")
]:
    p=paths(role)
    claims.append({"claim_type":claim,"supported_by":p,"allowed":bool(p),"reason":reason})

sig=[
    s.get("path") for s in roles.get("api_evidence",[])
    if (s.get("verification") or "").lower() in {"signature-verified","api-page-verified"}
    and s.get("path")
]
claims.append({
    "claim_type":"exact_api_signature",
    "supported_by":sig,
    "allowed":bool(sig),
    "reason":"Exact signatures require signature-verified or api-page-verified evidence."
})

local=[]
for s in sources:
    p=(s.get("path") or "").lower()
    st=(s.get("status") or "").lower()
    if st in {"compiled","verified","multiplayer-verified"} and (
        p.startswith("verification/") or p.startswith("lab/results/") or p.startswith("examples/compiled/")
    ):
        local.append(s.get("path"))
claims.append({
    "claim_type":"locally_compiled",
    "supported_by":[x for x in local if x],
    "allowed":bool(local),
    "reason":"Local compile claims require actual local UEFN evidence."
})

out={
    "schema_version":1,
    "query":d.get("query",""),
    "claims":claims,
    "unsupported_claims":[x["claim_type"] for x in claims if not x["allowed"]]
}
dest=ROOT/a.output
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
print(f"Claim ledger written: {dest}")
