#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.policy import SOURCE_TRUST, VALIDATION  # noqa: E402

errors: list[str] = []

def load(path: str):
    p = ROOT / path
    if not p.exists():
        errors.append(f"missing: {path}")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None

manifest = load("manifest.json") or {}
if manifest.get("schema_version") != 24:
    errors.append(f"manifest schema_version != 24: {manifest.get('schema_version')}")
if manifest.get("release", {}).get("version") != "24.0.0":
    errors.append(f"manifest release != 24.0.0: {manifest.get('release', {}).get('version')}")

marker = load("portable/generated_code_marker.json") or {}
if marker.get("marker_version") != "v24":
    errors.append("generated marker must be v24")
if tuple(marker.get("allowed_statuses", [])) != tuple(VALIDATION):
    errors.append("generated marker statuses diverge from canonical validation")
if marker.get("safety", {}).get("invisible_unicode") is not False:
    errors.append("invisible Unicode must remain disabled")

artifact_schema = load("schemas/generated_artifact.schema.json") or {}
if artifact_schema.get("properties", {}).get("version", {}).get("const") != "v24":
    errors.append("generated artifact schema must require v24")
if "claim_resolution" not in artifact_schema.get("required", []):
    errors.append("generated artifact schema must require claim_resolution")

for required in [
    "knowledge/api/symbols.jsonl",
    "knowledge/api/coverage.json",
    "knowledge/api/verification_queue.json",
    "knowledge/api/evidence_graph.json",
    "knowledge/api/revalidation_state.json",
    "schemas/api_claim.schema.json",
    "docs/architecture/V24_CLAIM_RESOLUTION.md",
    "evals/llm/cases.json",
    "evals/llm/runner.py",
]:
    if not (ROOT / required).exists():
        errors.append(f"missing: {required}")

symbols_path = ROOT / "knowledge/api/symbols.jsonl"
seen = set()
symbol_count = 0
if symbols_path.exists():
    for n, line in enumerate(symbols_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        symbol_count += 1
        try:
            row = json.loads(line)
        except Exception as exc:
            errors.append(f"symbols.jsonl:{n}: invalid JSON: {exc}")
            continue
        sid = row.get("symbol_id")
        if sid in seen:
            errors.append(f"symbols.jsonl:{n}: duplicate symbol_id {sid}")
        seen.add(sid)
        if row.get("source_trust") not in SOURCE_TRUST:
            errors.append(f"symbols.jsonl:{n}: invalid source_trust {row.get('source_trust')}")
        if row.get("validation") not in VALIDATION:
            errors.append(f"symbols.jsonl:{n}: invalid validation {row.get('validation')}")
        field_evidence = row.get("field_evidence")
        if not isinstance(field_evidence, dict):
            errors.append(f"symbols.jsonl:{n}: missing field_evidence")
            field_evidence = {}
        revalidation = row.get("revalidation")
        if not isinstance(revalidation, dict):
            errors.append(f"symbols.jsonl:{n}: missing revalidation")
            revalidation = {}
        if row.get("exact_signature_claim_allowed"):
            if not row.get("signature"):
                errors.append(f"symbols.jsonl:{n}: exact signature allowed without signature")
            if not field_evidence.get("signature"):
                errors.append(f"symbols.jsonl:{n}: exact signature allowed without signature field evidence")
            if revalidation.get("status") != "current":
                errors.append(f"symbols.jsonl:{n}: exact signature allowed with non-current evidence")
        if row.get("claim_state") == "exact-signature" and not row.get("exact_signature_claim_allowed"):
            errors.append(f"symbols.jsonl:{n}: exact-signature claim_state without exact signature permission")

coverage = load("knowledge/api/coverage.json") or {}
if coverage.get("symbol_count") not in (None, symbol_count):
    errors.append(f"coverage symbol_count {coverage.get('symbol_count')} != {symbol_count}")

graph = load("knowledge/api/evidence_graph.json") or {}
if graph.get("symbol_count") not in (None, symbol_count):
    errors.append(f"evidence graph symbol_count {graph.get('symbol_count')} != {symbol_count}")
graph_symbols = graph.get("symbols") or {}
if symbols_path.exists() and set(graph_symbols) != seen:
    errors.append("evidence graph symbols diverge from symbols.jsonl")

state = load("knowledge/api/revalidation_state.json") or {}
if str(state.get("api_version")) != str(manifest.get("verse_api_version")):
    errors.append("revalidation state API version diverges from manifest")

# Current authoritative docs must use V24 marker/version language.
for rel in [
    "README.md", "AI_BOOTSTRAP.md", "AI_GUIDE.md", "SECURITY.md",
    "docs/GENERATED_CODE_MARKER.md",
]:
    p = ROOT / rel
    if p.exists():
        text = p.read_text(encoding="utf-8", errors="ignore")
        if "verse-ai-generated:v21" in text or "verse-ai-generated:v22" in text or "verse-ai-generated:v23" in text:
            errors.append(f"{rel}: current documentation contains an old generated marker")

if errors:
    print("V24 integrity FAILED")
    for error in sorted(set(errors)):
        print("-", error)
    raise SystemExit(1)

print("V24 integrity OK")
print(f"Structured symbols: {symbol_count}")
print("UEFN compile status: NOT TESTED by this validator")
