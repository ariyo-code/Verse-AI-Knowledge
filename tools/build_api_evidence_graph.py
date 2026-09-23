#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from migrate_api_catalog_v24 import build_generated, build_evidence_graph  # noqa: E402

rows, _, _ = build_generated(ROOT)
graph = build_evidence_graph(rows, ROOT)
dest = ROOT / "knowledge/api/evidence_graph.json"
dest.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(dest.relative_to(ROOT))
print(f"symbols={graph['symbol_count']} evidence_nodes={graph['evidence_node_count']}")
