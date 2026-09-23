#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
errors = []

for rel in [
    "manifest.json",
    "knowledge/api_catalog.json",
    "knowledge/module_catalog.json",
    "knowledge/api/modules.json",
    "knowledge/api/versions.json",
    "knowledge/api/coverage.json",
    "knowledge/api/verification_queue.json",
    "knowledge/api/evidence_graph.json",
    "knowledge/api/revalidation_state.json",
    "rag/config.json",
    "rag/evidence_policy.json",
    "portable/generated_code_marker.json",
    "evals/hallucination/cases.json",
    "evals/retrieval/evidence_composition.json",
    "evals/generation/tasks.json",
    "evals/llm/cases.json",
    "evals/llm/schema.json",
]:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{rel}: {exc}")

for rel in ["knowledge/api/symbols.jsonl", "knowledge/api/verification_records.jsonl"]:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing {rel}")
        continue
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            json.loads(line)
        except Exception as exc:
            errors.append(f"{rel}:{n}: {exc}")

if errors:
    print("Static self-test FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Static self-test OK")
print("This test did not compile Verse in UEFN.")
