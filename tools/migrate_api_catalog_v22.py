#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from verse_ai_knowledge.policy import canonical_source_trust  # noqa: E402


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def evidence_basis(entry: dict[str, Any]) -> str | None:
    return entry.get("verification") or entry.get("evidence_basis")


def source_trust_for(entry: dict[str, Any]) -> str:
    old_verification = str(entry.get("verification") or "").lower()
    old_status = str(entry.get("status") or "").lower()
    if old_verification == "signature-verified":
        return "signature-verified"
    if old_verification == "api-page-verified":
        return "api-page-verified"
    if old_status in {
        "official-current", "official-stale", "community-verified", "community-unverified",
        "external-compiler-claimed", "reference-only", "deprecated", "unknown"
    }:
        return old_status
    if old_status == "external-community":
        return "community-unverified"
    source = str(entry.get("source") or entry.get("source_url") or "")
    if source.startswith("https://dev.epicgames.com/"):
        return "official-current"
    return canonical_source_trust(old_verification or old_status)


def symbol_record(name: str, entry: dict[str, Any], api_version: str, catalog_verified: str | None) -> dict[str, Any]:
    trust = source_trust_for(entry)
    basis = evidence_basis(entry)
    signature = entry.get("signature")
    signature_verified = bool(signature and basis in {"signature-verified", "api-page-verified"})
    effects = list(dict.fromkeys(entry.get("effects") or []))
    if signature and "<decides>" in signature and "decides" not in effects:
        effects.append("decides")
    if signature and "<transacts>" in signature and "transacts" not in effects:
        effects.append("transacts")
    failure_required = "decides" in effects or bool(signature and "<decides>" in signature)

    claim_scope = "exact-signature" if signature_verified else "presence-only"
    if signature and not signature_verified:
        claim_scope = "legacy-signature-unverified"

    return {
        "symbol_id": name,
        "name": name.split(".")[-1] if "." in name else name,
        "qualified_name": name,
        "kind": entry.get("kind") or "unknown",
        "module": entry.get("module") or "unknown",
        "signature": signature if signature is not None else None,
        "effects": sorted(set(str(x) for x in effects)),
        "failure_context_required": failure_required,
        "api_version": api_version,
        "introduced_in": entry.get("introduced_in"),
        "deprecated_in": entry.get("deprecated_in"),
        "replacement": entry.get("replacement"),
        "source_trust": trust,
        "validation": "static-checked",
        "source_url": entry.get("source") or entry.get("source_url"),
        "verified_at": entry.get("last_verified") or catalog_verified,
        "evidence_basis": basis,
        "claim_scope": claim_scope,
        "signature_verified": signature_verified,
        "exact_signature_claim_allowed": signature_verified,
        "summary": entry.get("summary"),
        "cautions": list(entry.get("cautions") or []),
        "member_names": sorted(set(entry.get("key_members") or [])),
        "event_names": sorted(set(entry.get("key_events") or [])),
    }


def build_generated(root: Path = ROOT) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    catalog = read_json(root / "knowledge/api_catalog.json")
    module_catalog = read_json(root / "knowledge/module_catalog.json")
    api_version = str(catalog.get("verse_api_version") or module_catalog.get("snapshot") or "unknown")
    last_verified = catalog.get("last_verified") or module_catalog.get("last_verified")

    symbols = [
        symbol_record(name, entry, api_version, last_verified)
        for name, entry in sorted(catalog.get("entries", {}).items(), key=lambda x: x[0].casefold())
    ]

    modules = {
        "schema_version": 1,
        "api_version": api_version,
        "source_url": module_catalog.get("source"),
        "verified_at": module_catalog.get("last_verified"),
        "source_trust": "official-current" if str(module_catalog.get("source", "")).startswith("https://dev.epicgames.com/") else "unknown",
        "validation": "static-checked",
        "top_level": module_catalog.get("top_level", {}),
    }
    versions = {
        "schema_version": 1,
        "current": api_version,
        "known": [
            {
                "version": api_version,
                "verified_at": last_verified,
                "source_url": module_catalog.get("source"),
                "source_trust": modules["source_trust"],
            }
        ],
        "note": "V22 does not infer historical introduction/deprecation versions that are not present in verified source data.",
    }
    return symbols, modules, versions


def render_symbols_jsonl(symbols: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in symbols)


def write_generated(root: Path = ROOT) -> None:
    symbols, modules, versions = build_generated(root)
    api_dir = root / "knowledge/api"
    api_dir.mkdir(parents=True, exist_ok=True)
    (api_dir / "symbols.jsonl").write_text(render_symbols_jsonl(symbols), encoding="utf-8")
    write_json(api_dir / "modules.json", modules)
    write_json(api_dir / "versions.json", versions)
    print(f"Generated {len(symbols)} structured API symbol record(s).")


if __name__ == "__main__":
    write_generated()
