#!/usr/bin/env python3
from pathlib import Path
import json,sys

ROOT=Path(__file__).resolve().parents[1]
errors=[]

# Validate key JSON.
for rel in [
    "manifest.json","lab/compile_queue.json","external/corpus_manifest.json",
    "rag/evidence_policy.json","knowledge/api_catalog.json"
]:
    try:
        json.loads((ROOT/rel).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{rel}: {exc}")

# Evidence artifacts must exist, but this is not UEFN proof.
for rel in [
    "rag/evidence_graph.json",
    "tools/rag_context_compiler.py",
    "tools/build_claim_ledger.py"
]:
    if not (ROOT/rel).exists():
        errors.append("missing: "+rel)

if errors:
    print("Static self-test FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)

print("Static self-test PASS")
print("This does not claim an UEFN compile.")
