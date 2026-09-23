#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.api_index import load_symbols  # noqa: E402
from verse_ai_knowledge.policy import exact_signature_allowed  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--evidence", default="rag/generated/EVIDENCE_PACK.json")
ap.add_argument("--output", default="rag/generated/CLAIM_LEDGER.json")
args = ap.parse_args()

src = ROOT / args.evidence
if not src.exists():
    raise SystemExit(f"Missing evidence manifest: {src}")

data = json.loads(src.read_text(encoding="utf-8"))
sources = data.get("sources", [])
roles = {}
for source in sources:
    roles.setdefault(source.get("role"), []).append(source)


def paths(role_name: str) -> list[str]:
    return [x.get("path") for x in roles.get(role_name, []) if x.get("path")]


claims = []
for claim, role_name, reason in [
    ("project_intent", "project_context", "Project sources/manifests support project intent/current structure."),
    ("api_presence", "api_evidence", "API evidence supports presence according to its source-trust scope."),
    ("lifecycle_guidance", "lifecycle", "Lifecycle sources support cleanup/lifecycle guidance."),
    ("observed_error", "error_memory", "Only stored observed errors support an error-memory claim."),
    ("verification_procedure", "verification", "Verification sources explain how to validate."),
    ("external_pattern", "external_examples", "External examples support patterns/upstream claims only."),
]:
    supporting = paths(role_name)
    claims.append({"claim_type": claim, "supported_by": supporting, "allowed": bool(supporting), "reason": reason})

symbol_rows = load_symbols(ROOT)
by_id = {x.get("symbol_id"): x for x in symbol_rows}
exact_names = data.get("exact_api_matches", [])
exact_ok = []
exact_blocked = []
for name in exact_names:
    row = by_id.get(name)
    if row and exact_signature_allowed(row):
        exact_ok.append(f"knowledge/api/symbols.jsonl#{name}")
    else:
        exact_blocked.append(name)
claims.append({
    "claim_type": "exact_api_signature",
    "supported_by": exact_ok,
    "allowed": bool(exact_names) and not exact_blocked,
    "reason": "Exact signatures require symbol-level signature evidence; otherwise use TODO(API VERIFY).",
    "blocked_symbols": exact_blocked,
})

local = []
for source in sources:
    path = (source.get("path") or "").lower()
    validation = (source.get("validation") or "").lower()
    if validation in {"compiled", "verified", "multiplayer-verified"} and (
        path.startswith("verification/") or path.startswith("lab/results/") or path.startswith("examples/compiled/")
    ):
        local.append(source.get("path"))
claims.append({
    "claim_type": "locally_compiled",
    "supported_by": [x for x in local if x],
    "allowed": bool(local),
    "reason": "Local compile claims require actual local UEFN evidence.",
})

out = {
    "schema_version": 2,
    "query": data.get("query", ""),
    "claims": claims,
    "unsupported_claims": [x["claim_type"] for x in claims if not x["allowed"]],
}
dest = ROOT / args.output
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Claim ledger written: {dest}")
