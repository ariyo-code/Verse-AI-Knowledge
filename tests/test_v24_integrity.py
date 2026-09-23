#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.api_index import load_symbols  # noqa: E402

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
assert manifest["schema_version"] == 24
assert manifest["release"]["version"] == "24.0.0"

rows = load_symbols(ROOT)
assert rows
for row in rows:
    assert isinstance(row.get("field_evidence"), dict)
    assert isinstance(row.get("revalidation"), dict)
    assert row.get("claim_state") in {"presence-only", "exact-signature", "behavior-verified", "deprecated"}
    if row.get("exact_signature_claim_allowed"):
        assert row.get("signature")
        assert row["field_evidence"].get("signature")
        assert row["revalidation"]["status"] == "current"

graph = json.loads((ROOT / "knowledge/api/evidence_graph.json").read_text(encoding="utf-8"))
assert graph["symbol_count"] == len(rows)
assert set(graph["symbols"]) == {row["symbol_id"] for row in rows}

marker = json.loads((ROOT / "portable/generated_code_marker.json").read_text(encoding="utf-8"))
assert marker["marker_version"] == "v24"
assert marker["safety"]["invisible_unicode"] is False
assert marker["rules"]["field_level_claim_resolution"] is True

print("V24 integrity unit tests OK")
