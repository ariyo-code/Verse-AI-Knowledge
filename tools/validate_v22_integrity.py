#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.policy import SOURCE_TRUST, VALIDATION  # noqa: E402

errors: list[str] = []
warnings: list[str] = []


def load(path: str):
    p = ROOT / path
    if not p.exists():
        errors.append(f"missing: {path}")
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return None


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


manifest = load("manifest.json") or {}
check(manifest.get("schema_version") == 22, "manifest schema_version must be 22")
check(manifest.get("release", {}).get("version") == "22.0.0", "manifest release version must be 22.0.0")
check(manifest.get("entrypoint") == "AI_BOOTSTRAP.md", "manifest entrypoint must be AI_BOOTSTRAP.md")
check(tuple(manifest.get("trust_model", {}).get("source_trust", [])) == SOURCE_TRUST, "manifest source_trust vocabulary diverges from canonical policy")
check(tuple(manifest.get("trust_model", {}).get("validation", [])) == VALIDATION, "manifest validation vocabulary diverges from canonical policy")
check(tuple(manifest.get("verification_statuses", [])) == VALIDATION, "legacy verification_statuses mirror must equal canonical validation list")

trust_schema = load("schemas/trust.schema.json") or {}
validation_schema = load("schemas/validation_status.schema.json") or {}
check(tuple(trust_schema.get("enum", [])) == SOURCE_TRUST, "schemas/trust.schema.json enum diverges")
check(tuple(validation_schema.get("enum", [])) == VALIDATION, "schemas/validation_status.schema.json enum diverges")

marker = load("portable/generated_code_marker.json") or {}
check(marker.get("marker_version") == "v22", "generated marker must be v22")
check(tuple(marker.get("allowed_statuses", [])) == VALIDATION, "generated marker statuses diverge from canonical validation")

catalog = load("knowledge/api_catalog.json") or {}
modules = load("knowledge/module_catalog.json") or {}
versions = load("knowledge/api/versions.json") or {}
api_version = manifest.get("verse_api_version")
check(catalog.get("verse_api_version") == api_version, "manifest/catalog Verse API version mismatch")
check(modules.get("snapshot") == api_version, "manifest/module catalog Verse API version mismatch")
check(versions.get("current") == api_version, "manifest/structured versions Verse API mismatch")

symbols_path = ROOT / "knowledge/api/symbols.jsonl"
if not symbols_path.exists():
    errors.append("missing: knowledge/api/symbols.jsonl")
else:
    symbol_count = 0
    for n, line in enumerate(symbols_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        symbol_count += 1
        try:
            row = json.loads(line)
        except Exception as exc:
            errors.append(f"symbols.jsonl:{n}: invalid JSON: {exc}")
            continue
        if row.get("source_trust") not in SOURCE_TRUST:
            errors.append(f"symbols.jsonl:{n}: invalid source_trust {row.get('source_trust')}")
        if row.get("validation") not in VALIDATION:
            errors.append(f"symbols.jsonl:{n}: invalid validation {row.get('validation')}")
        if row.get("exact_signature_claim_allowed") and not row.get("signature"):
            errors.append(f"symbols.jsonl:{n}: exact signature allowed without signature")
        if row.get("exact_signature_claim_allowed") and row.get("source_trust") not in {"signature-verified", "api-page-verified"}:
            errors.append(f"symbols.jsonl:{n}: exact signature allowed without signature-level trust")
    if catalog.get("entries") and symbol_count != len(catalog["entries"]):
        errors.append(f"structured symbol count {symbol_count} != legacy catalog count {len(catalog['entries'])}")

# Manifest path integrity: inspect path-like strings while ignoring URLs, commands and glob-like text.
PATH_EXT = re.compile(r"\.(?:md|json|jsonl|py|yml|yaml|txt|toml|ps1|bat)$", re.I)

def walk(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)
    elif isinstance(value, str):
        yield value

for value in walk(manifest):
    if "://" in value or value.startswith("verse-ai") or " " in value or "{" in value:
        continue
    if value.endswith("/") or PATH_EXT.search(value):
        target = ROOT / value
        if not target.exists():
            errors.append(f"manifest path does not exist: {value}")

# High validation statuses require evidence flags where verification records exist.
verification_root = ROOT / "verification"
if verification_root.exists():
    for path in verification_root.rglob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        status = data.get("validation") or data.get("status")
        checks = data.get("checks", {})
        if status in {"compiled", "verified", "multiplayer-verified"} and not checks.get("compiled"):
            errors.append(f"{path.relative_to(ROOT)}: {status} without compiled evidence")
        if status in {"verified", "multiplayer-verified"} and not checks.get("runtime_tested"):
            errors.append(f"{path.relative_to(ROOT)}: {status} without runtime evidence")
        if status == "multiplayer-verified" and not checks.get("multiplayer_tested"):
            errors.append(f"{path.relative_to(ROOT)}: multiplayer-verified without multiplayer evidence")

if errors:
    print("V22 integrity FAILED")
    for error in sorted(set(errors)):
        print("-", error)
    raise SystemExit(1)
print("V22 integrity OK")
print("UEFN compile status: NOT TESTED by this validator")
