from __future__ import annotations

from pathlib import Path
from typing import Any

from .api_index import lookup
from .policy import repo_root

EXACT_FIELDS = {"signature", "parameters", "return_type", "effects", "event_payloads"}
PRESENCE_FIELDS = {"presence", "module", "kind", "event_names", "member_names"}


def _evidence_for(row: dict[str, Any], field: str) -> list[str]:
    field_evidence = row.get("field_evidence") or {}
    values = field_evidence.get(field) or []
    return [str(x) for x in values if x]


def resolve_claim(
    symbol: str,
    field: str = "presence",
    *,
    root: Path | None = None,
) -> dict[str, Any]:
    root = root or repo_root()
    row, suggestions = lookup(symbol, root)
    if not row:
        return {
            "symbol": symbol,
            "field": field,
            "decision": "TODO(API VERIFY)",
            "supported": False,
            "reason": "Unknown structured API symbol.",
            "evidence_ids": [],
            "suggestions": suggestions,
        }

    revalidation = (row.get("revalidation") or {}).get("status", "unknown")
    if revalidation not in {"current", "not-applicable"}:
        return {
            "symbol": row.get("symbol_id"),
            "field": field,
            "decision": "TODO(API VERIFY)",
            "supported": False,
            "reason": f"Stored evidence requires revalidation: {revalidation}.",
            "evidence_ids": _evidence_for(row, field),
            "suggestions": [],
        }

    coverage = row.get("coverage") or {}
    evidence_ids = _evidence_for(row, field)

    if field == "presence":
        ok = bool(coverage.get("presence"))
    elif field == "signature":
        ok = bool(row.get("exact_signature_claim_allowed") and row.get("signature") and evidence_ids)
    elif field == "parameters":
        ok = bool(coverage.get("parameters") and evidence_ids)
    elif field == "return_type":
        ok = bool(coverage.get("return_type") and evidence_ids)
    elif field == "effects":
        ok = bool(coverage.get("effects") and evidence_ids)
    elif field == "event_names":
        ok = bool(coverage.get("event_names") and evidence_ids)
    elif field == "event_payloads":
        ok = bool(coverage.get("event_payloads") and evidence_ids)
    elif field == "member_names":
        ok = bool(row.get("member_names") and evidence_ids)
    elif field == "module":
        ok = bool(row.get("module") and evidence_ids)
    elif field == "kind":
        ok = bool(row.get("kind") and evidence_ids)
    else:
        return {
            "symbol": row.get("symbol_id"),
            "field": field,
            "decision": "TODO(API VERIFY)",
            "supported": False,
            "reason": "Unknown claim field.",
            "evidence_ids": [],
            "suggestions": [],
        }

    return {
        "symbol": row.get("symbol_id"),
        "field": field,
        "decision": "ALLOW" if ok else "TODO(API VERIFY)",
        "supported": bool(ok),
        "reason": "Field-level evidence is available." if ok else "Field-level evidence is insufficient.",
        "evidence_ids": evidence_ids,
        "source_url": row.get("source_url"),
        "api_version": row.get("api_version"),
        "claim_scope": row.get("claim_scope"),
        "suggestions": [],
    }
