#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "AI_BOOTSTRAP.md", "manifest.json", "pyproject.toml",
    "knowledge/api/symbols.jsonl", "knowledge/api/modules.json", "knowledge/api/versions.json",
    "knowledge/api/coverage.json", "knowledge/api/verification_queue.json",
    "knowledge/api/evidence_graph.json", "knowledge/api/revalidation_state.json",
    "schemas/trust.schema.json", "schemas/validation_status.schema.json",
    "schemas/api_symbol.schema.json", "schemas/api_evidence.schema.json",
    "schemas/api_claim.schema.json", "schemas/generated_artifact.schema.json",
    "external/corpus_manifest.json", "tools/corpus_coverage.py", "tools/ensure_full_corpus.py",
    "tools/analyze_verse_dependencies.py", "rag/evidence_policy.json",
    "tools/rag_build_evidence_graph.py", "tools/rag_context_compiler.py",
    "evals/retrieval/evidence_composition.json", "evals/llm/cases.json",
    "prompts/EVIDENCE_FIRST_CODEX_AGENT.md", "lab/compile_queue.json",
    ".github/workflows/ci.yml",
]
errors = [rel for rel in required if not (ROOT / rel).exists()]

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
if manifest.get("schema_version") != 25:
    errors.append("schema_version != 25")
if manifest.get("release", {}).get("version") != "25.0.0":
    errors.append("release != 25.0.0")

queue = json.loads((ROOT / "lab/compile_queue.json").read_text(encoding="utf-8"))
if len(queue.get("entries", [])) != 50:
    errors.append("compile queue != 50")

if errors:
    print("Repository validation FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Repository validation OK")
