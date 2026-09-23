#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verse_ai_knowledge.policy import (  # noqa: E402
    SOURCE_TRUST,
    VALIDATION,
    canonical_source_trust,
    validation_from_checks,
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_manifest() -> None:
    path = ROOT / "manifest.json"
    m = read_json(path)
    m["schema_version"] = 22
    m["release"] = {"version": "22.0.0", "name": "Knowledge Integrity & Agent Reliability"}
    m["entrypoint"] = "AI_BOOTSTRAP.md"
    api_version = str(m.get("last_verified_verse_api_version") or "42.20")
    m["verse_api_version"] = api_version
    m["trust_model"] = {
        "source_trust": list(SOURCE_TRUST),
        "validation": list(VALIDATION),
        "source_trust_schema": "schemas/trust.schema.json",
        "validation_schema": "schemas/validation_status.schema.json",
        "rule": "Source trust and local validation are independent axes."
    }
    # Compatibility mirror for older tools. V22 validators require equality with canonical validation.
    m["verification_statuses"] = list(VALIDATION)
    m["ci_validation"] = ".github/workflows/ci.yml"
    m["api_knowledge_v22"] = {
        "legacy_catalog": "knowledge/api_catalog.json",
        "symbols": "knowledge/api/symbols.jsonl",
        "modules": "knowledge/api/modules.json",
        "versions": "knowledge/api/versions.json",
        "symbol_schema": "schemas/api_symbol.schema.json",
        "migration_tool": "tools/migrate_api_catalog_v22.py"
    }
    m["evals"] = {
        "root": "evals/",
        "hallucination_cases": "evals/hallucination/cases.json",
        "retrieval_evidence": "evals/retrieval/evidence_composition.json",
        "runner": "tools/run_hallucination_evals.py"
    }
    m["unified_cli"] = {
        "package": "src/verse_ai_knowledge/",
        "entrypoint": "verse-ai",
        "pyproject": "pyproject.toml"
    }
    m["v22"] = {
        "bootstrap": "AI_BOOTSTRAP.md",
        "integrity_validator": "tools/validate_v22_integrity.py",
        "generated_drift": "tools/check_generated_drift.py",
        "migration_docs": "docs/MIGRATION_V21_TO_V22.md"
    }
    # Existing sections are retained; point legacy benchmark to the stable singular/manual suite.
    if isinstance(m.get("benchmark"), dict):
        m["benchmark"]["note"] = "Legacy/manual scoring suite; automated policy/retrieval evals live under evals/."
    write_json(path, m)


def update_marker() -> None:
    path = ROOT / "portable/generated_code_marker.json"
    d = read_json(path)
    d["schema_version"] = 2
    d["marker_version"] = "v22"
    d["default_marker"] = "<!-- verse-ai-generated:v22 -->"
    d["metadata_template"] = "<!-- verse-ai-generated:v22;lang=verse;status={status} -->"
    d["allowed_statuses"] = list(VALIDATION)
    d["default_status"] = "draft"
    d.setdefault("rules", {})["claim_compiled_without_evidence"] = False
    write_json(path, d)


def update_rag_config() -> None:
    path = ROOT / "rag/config.json"
    old = read_json(path)
    weights = dict(old.get("weights", {}))
    legacy_trust_weight = weights.pop("trust", 4.0)
    legacy_validation_weight = weights.pop("verified_status", 2.5)
    weights["source_trust"] = legacy_trust_weight
    weights["validation"] = legacy_validation_weight
    weights.setdefault("semantic_similarity", 0.5)
    config = {
        "schema_version": 2,
        "default_context_budget_chars": old.get("default_context_budget_chars", 18000),
        "default_max_results": old.get("default_max_results", 12),
        "weights": weights,
        "source_trust_scores": {
            "signature-verified": 1.0,
            "api-page-verified": 0.98,
            "official-current": 0.95,
            "community-verified": 0.78,
            "external-compiler-claimed": 0.70,
            "official-stale": 0.60,
            "community-unverified": 0.45,
            "reference-only": 0.25,
            "deprecated": 0.10,
            "unknown": 0.35
        },
        "validation_scores": {
            "multiplayer-verified": 1.0,
            "verified": 0.90,
            "compiled": 0.78,
            "static-checked": 0.55,
            "draft": 0.25
        },
        "legacy_source_trust_aliases": {
            "module-index-verified": "official-current",
            "official-guide-presence-verified": "official-current",
            "external-community": "community-unverified",
            "unspecified": "unknown"
        },
        "semantic": {
            "enabled": False,
            "provider": "none",
            "rule": "Semantic similarity is optional and must never outrank exact verified API evidence."
        },
        "preferred_paths": old.get("preferred_paths", []),
        "excluded_paths": old.get("excluded_paths", [".git/", "__pycache__/"])
    }
    write_json(path, config)


def update_api_catalog() -> None:
    path = ROOT / "knowledge/api_catalog.json"
    d = read_json(path)
    for _, entry in d.get("entries", {}).items():
        old_verification = entry.get("verification")
        old_status = entry.get("status")
        if old_verification == "signature-verified":
            trust = "signature-verified"
        elif old_verification == "api-page-verified":
            trust = "api-page-verified"
        elif str(entry.get("source") or "").startswith("https://dev.epicgames.com/"):
            trust = "official-current"
        else:
            trust = canonical_source_trust(old_status or old_verification)
        entry["source_trust"] = trust
        entry["validation"] = "static-checked"
        if old_verification:
            entry["evidence_basis"] = old_verification
        sig = entry.get("signature")
        entry["signature_verified"] = bool(sig and old_verification in {"signature-verified", "api-page-verified"})
        entry["exact_signature_claim_allowed"] = bool(entry["signature_verified"])
    write_json(path, d)


def update_external_sources() -> None:
    path = ROOT / "external/sources.json"
    if not path.exists():
        return
    d = read_json(path)
    for src in d.get("approved_sources", []):
        src["trust"] = canonical_source_trust(src.get("trust"))
    for src in d.get("reference_only", []):
        src.setdefault("trust", "reference-only")
    write_json(path, d)


def update_curated_examples() -> None:
    path = ROOT / "curation/curated_examples.json"
    if not path.exists():
        return
    d = read_json(path)
    if d.get("upstream_trust"):
        d["upstream_trust"] = canonical_source_trust(d.get("upstream_trust"))
    for row in d.get("examples", []):
        legacy = row.get("source_trust") or row.get("status")
        row["source_trust"] = canonical_source_trust(legacy)
        row["validation"] = "draft"
        if row.get("status") and row.get("status") != row["source_trust"]:
            row["legacy_status"] = row.get("status")
    write_json(path, d)


def update_compile_queue() -> None:
    path = ROOT / "lab/compile_queue.json"
    if not path.exists():
        return
    d = read_json(path)
    for row in d.get("entries", []):
        trust = row.get("upstream_source_trust") or row.get("upstream_status")
        row["upstream_source_trust"] = canonical_source_trust(trust)
        row["validation"] = validation_from_checks(row.get("local_verification"), row.get("queue_status"))
    write_json(path, d)


def migrate_memory_file(path: Path) -> None:
    d = read_json(path)
    legacy = str(d.get("status") or "planned")
    checks = d.get("verification") if isinstance(d.get("verification"), dict) else {}
    d["validation"] = validation_from_checks(checks, legacy)
    if legacy in {"template", "planned", "discovered", "deprecated"}:
        d["lifecycle_status"] = legacy
    else:
        d["lifecycle_status"] = "active"
    d.setdefault("source_trust", "unknown")
    write_json(path, d)


def update_project_memory() -> None:
    for pattern in ("projects/**/project.json", "projects/**/system.json"):
        for path in ROOT.glob(pattern):
            migrate_memory_file(path)
    for path in ROOT.glob("examples/**/metadata.json"):
        try:
            d = read_json(path)
        except Exception:
            continue
        legacy = str(d.get("status") or "draft")
        checks = {
            "compiled": bool(d.get("tested_in_uefn")),
            "runtime_tested": legacy in {"verified", "multiplayer-verified"},
            "multiplayer_tested": bool(d.get("multiplayer_tested")),
        }
        d["validation"] = validation_from_checks(checks, legacy)
        d["lifecycle_status"] = "deprecated" if legacy == "deprecated" else "active"
        d.setdefault("source_trust", "unknown")
        write_json(path, d)


def prepend_once(path: Path, marker: str, block: str) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    # Keep the original title first if present, then insert V22 block.
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        new = lines[0] + "\n\n" + block.rstrip() + "\n\n" + "\n".join(lines[1:]).lstrip("\n")
    else:
        new = block.rstrip() + "\n\n" + text
    path.write_text(new.rstrip() + "\n", encoding="utf-8")


def update_entry_docs() -> None:
    prepend_once(
        ROOT / "AGENTS.md",
        "V22_CANONICAL_CONFIDENCE_MODEL",
        "<!-- V22_CANONICAL_CONFIDENCE_MODEL -->\n"
        "## V22 canonical confidence model\n\n"
        "Before substantial work, read `AI_BOOTSTRAP.md`. Keep `source_trust` and `validation` independent. "
        "The only canonical local validation values are `draft`, `static-checked`, `compiled`, `verified`, and "
        "`multiplayer-verified`. Deprecation, planning, discovery, and source authority are not local validation statuses. "
        "If an exact Verse API/signature is unsupported, use `TODO(API VERIFY)`.\n"
    )
    prepend_once(
        ROOT / "knowledge/ROUTING.md",
        "V22_ROUTING_ENTRY",
        "<!-- V22_ROUTING_ENTRY -->\n"
        "## V22 entry route\n\n"
        "For a new agent session: `AI_BOOTSTRAP.md` → this routing table → targeted retrieval → Evidence Pack → Claim Ledger → implementation → real UEFN validation when available. "
        "Use `verse-ai` as the preferred CLI; legacy `tools/*.py` entry points remain supported.\n"
    )


def main() -> None:
    update_manifest()
    update_marker()
    update_rag_config()
    update_api_catalog()
    update_external_sources()
    update_curated_examples()
    update_compile_queue()
    update_project_memory()
    update_entry_docs()

    subprocess.run([sys.executable, str(ROOT / "tools/migrate_api_catalog_v22.py")], check=True)
    print("V22 metadata migration complete.")


if __name__ == "__main__":
    main()
