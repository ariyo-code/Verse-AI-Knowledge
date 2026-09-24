#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
out = ROOT / "projects" / "public_project_graph.json"
data = {
    "schema_version": 2,
    "mode": "opaque-public",
    "nodes": [],
    "edges": [],
    "note": "Real project profiles are not stored in the public repository. Use tools/opaque_project_match.py."
}
out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
print("Public project graph contains no real project identities.")
