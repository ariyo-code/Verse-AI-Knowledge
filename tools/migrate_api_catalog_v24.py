#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from migrate_api_catalog_v23 import build_generated as build_v23, queue as queue_v23  # noqa: E402


FIELDS = (
    "presence", "module", "kind", "signature", "parameters",
    "return_type", "effects", "event_names", "event_payloads", "member_names",
)


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render(rows: list[dict]) -> str:
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)


def source_evidence_id(url: str | None) -> str | None:
    if not url:
        return None
    return "src-" + hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def load_review_records(root: Path) -> dict[str, dict]:
    path = root / "knowledge/api/verification_records.jsonl"
    out: dict[str, dict] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("review_status") == "verified":
            out[row["evidence_id"]] = row
    return out


def enrich_row(row: dict, current_api: str) -> dict:
    row = dict(row)
    source_id = source_evidence_id(row.get("source_url"))
    exact_ids = list(row.get("evidence_ids") or [])
    if row.get("exact_signature_claim_allowed") and not exact_ids and source_id:
        exact_ids = [source_id]

    field_evidence = {field: [] for field in FIELDS}
    if source_id:
        for field in ("presence", "module", "kind"):
            field_evidence[field] = [source_id]
        if row.get("event_names"):
            field_evidence["event_names"] = [source_id]
        if row.get("member_names"):
            field_evidence["member_names"] = [source_id]

    if row.get("exact_signature_claim_allowed"):
        for field in ("signature", "parameters", "effects"):
            field_evidence[field] = list(exact_ids)
        if row.get("return_type") is not None:
            field_evidence["return_type"] = list(exact_ids)

    if row.get("event_details") and any(bool(x.get("verified")) for x in row.get("event_details", [])):
        field_evidence["event_payloads"] = list(exact_ids or ([source_id] if source_id else []))

    trust = row.get("source_trust")
    if trust == "deprecated":
        revalidation_status = "stale"
        reason = "Symbol/source is marked deprecated."
        claim_state = "deprecated"
    elif str(row.get("api_version")) != str(current_api):
        revalidation_status = "needs-review"
        reason = "Stored symbol evidence targets a different Verse API snapshot."
        claim_state = "exact-signature" if row.get("exact_signature_claim_allowed") else "presence-only"
    elif trust == "official-stale":
        revalidation_status = "needs-review"
        reason = "Source is marked official-stale."
        claim_state = "exact-signature" if row.get("exact_signature_claim_allowed") else "presence-only"
    else:
        revalidation_status = "current"
        reason = None
        claim_state = "exact-signature" if row.get("exact_signature_claim_allowed") else "presence-only"

    row["field_evidence"] = field_evidence
    row["revalidation"] = {
        "status": revalidation_status,
        "api_version": row.get("api_version"),
        "reason": reason,
    }
    row["claim_state"] = claim_state
    return row


def build_generated(root: Path = ROOT):
    rows, modules, versions = build_v23(root)
    current_api = str(versions.get("current"))
    rows = [enrich_row(r, current_api) for r in rows]
    modules = dict(modules)
    modules["schema_version"] = 3
    versions = dict(versions)
    versions["schema_version"] = 3
    versions["note"] = (
        "V24 keeps version facts evidence-bound. Field-level claims require field evidence; "
        "a version change triggers revalidation rather than silent promotion."
    )
    return rows, modules, versions


def build_coverage(rows: list[dict], api_version: str) -> dict:
    total = len(rows)

    def count(fn):
        return sum(1 for row in rows if fn(row))

    def metric(fn):
        n = count(fn)
        return {"count": n, "percent": round(100 * n / max(total, 1), 2)}

    modules = sorted({r.get("module") for r in rows if r.get("module")})
    source_breakdown = Counter(r.get("source_trust", "unknown") for r in rows)
    validation_breakdown = Counter(r.get("validation", "draft") for r in rows)
    claim_breakdown = Counter(r.get("claim_state", "presence-only") for r in rows)
    stale = count(lambda r: (r.get("revalidation") or {}).get("status") not in {"current", "not-applicable"})

    return {
        "schema_version": 2,
        "generated_by": "tools/migrate_api_catalog_v24.py",
        "api_version": api_version,
        "symbol_count": total,
        "module_count": len(modules),
        "modules": modules,
        "coverage": {
            "presence": metric(lambda r: (r.get("coverage") or {}).get("presence")),
            "signature_verified": metric(lambda r: (r.get("coverage") or {}).get("signature")),
            "parameters_structured": metric(lambda r: (r.get("coverage") or {}).get("parameters")),
            "return_type_structured": metric(lambda r: (r.get("coverage") or {}).get("return_type")),
            "effects_structured": metric(lambda r: (r.get("coverage") or {}).get("effects")),
            "event_names_known": metric(lambda r: (r.get("coverage") or {}).get("event_names")),
            "event_payloads_verified": metric(lambda r: (r.get("coverage") or {}).get("event_payloads")),
            "exact_signature_claim_allowed": metric(lambda r: r.get("exact_signature_claim_allowed")),
            "field_evidence_present": metric(lambda r: any((r.get("field_evidence") or {}).values())),
        },
        "source_trust_breakdown": dict(sorted(source_breakdown.items())),
        "validation_breakdown": dict(sorted(validation_breakdown.items())),
        "claim_state_breakdown": dict(sorted(claim_breakdown.items())),
        "revalidation": {
            "current": total - stale,
            "needs_attention": stale,
        },
        "note": (
            "Coverage describes symbols currently known to this repository. "
            "It is not a claim about the total number of APIs published by Epic."
        ),
    }


def build_queue(rows: list[dict]) -> dict:
    base = queue_v23(rows)
    items = []
    for item in base.get("items", []):
        row = next(x for x in rows if x["symbol_id"] == item["symbol_id"])
        missing = []
        fields = row.get("field_evidence") or {}
        if row.get("kind") in {"function", "extension"}:
            for field in ("signature", "parameters", "return_type", "effects"):
                if not fields.get(field):
                    missing.append(field)
        else:
            if not fields.get("member_names") and row.get("member_names"):
                missing.append("member_evidence")
            if not fields.get("event_names") and row.get("event_names"):
                missing.append("event_evidence")
            if not row.get("exact_signature_claim_allowed"):
                missing.append("declaration_or_signature")
        item = dict(item)
        item["missing_field_evidence"] = missing
        item["revalidation_status"] = (row.get("revalidation") or {}).get("status")
        items.append(item)
    return {
        "schema_version": 2,
        "generated_by": "tools/migrate_api_catalog_v24.py",
        "pending_count": len(items),
        "items": items,
    }


def build_evidence_graph(rows: list[dict], root: Path = ROOT) -> dict:
    verified = load_review_records(root)
    evidence: dict[str, dict] = {}

    for row in rows:
        source_id = source_evidence_id(row.get("source_url"))
        if source_id and source_id not in evidence:
            evidence[source_id] = {
                "kind": "source",
                "source_url": row.get("source_url"),
                "source_trust": row.get("source_trust"),
                "api_version": row.get("api_version"),
            }

    for evidence_id, record in verified.items():
        evidence[evidence_id] = {
            "kind": "reviewed-api-evidence",
            "source_url": record.get("source_url"),
            "api_version": record.get("api_version"),
            "review_status": record.get("review_status"),
            "reviewed_at": record.get("reviewed_at"),
            "fields_verified": record.get("fields_verified") or [
                "signature", "parameters", "return_type", "effects"
            ],
        }

    symbols = {
        row["symbol_id"]: {
            "claim_state": row.get("claim_state"),
            "revalidation": row.get("revalidation"),
            "fields": row.get("field_evidence") or {},
        }
        for row in rows
    }
    return {
        "schema_version": 1,
        "generated_by": "tools/migrate_api_catalog_v24.py",
        "api_version": rows[0].get("api_version") if rows else None,
        "symbol_count": len(rows),
        "evidence_node_count": len(evidence),
        "evidence": dict(sorted(evidence.items())),
        "symbols": dict(sorted(symbols.items(), key=lambda kv: kv[0].casefold())),
    }


def build_revalidation_state(rows: list[dict], root: Path = ROOT) -> dict:
    current = rows[0].get("api_version") if rows else None
    stale_symbols = [
        r["symbol_id"] for r in rows
        if (r.get("revalidation") or {}).get("status") not in {"current", "not-applicable"}
    ]
    records = load_review_records(root)
    stale_records = [
        eid for eid, rec in records.items()
        if str(rec.get("api_version")) != str(current)
    ]
    return {
        "schema_version": 1,
        "api_version": current,
        "stale_symbol_count": len(stale_symbols),
        "stale_symbols": stale_symbols,
        "stale_verified_evidence_count": len(stale_records),
        "stale_verified_evidence_ids": stale_records,
        "rule": "Version changes trigger revalidation; they never silently rewrite verified claims.",
    }


def write_generated(root: Path = ROOT) -> None:
    rows, modules, versions = build_generated(root)
    api = str(versions.get("current"))
    dest = root / "knowledge/api"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "symbols.jsonl").write_text(render(rows), encoding="utf-8")
    dump(dest / "modules.json", modules)
    dump(dest / "versions.json", versions)
    dump(dest / "coverage.json", build_coverage(rows, api))
    dump(dest / "verification_queue.json", build_queue(rows))
    dump(dest / "evidence_graph.json", build_evidence_graph(rows, root))
    dump(dest / "revalidation_state.json", build_revalidation_state(rows, root))
    print(f"Generated {len(rows)} V24 structured API symbol record(s).")


if __name__ == "__main__":
    write_generated()
