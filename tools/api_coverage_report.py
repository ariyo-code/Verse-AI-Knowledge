#!/usr/bin/env python3
from pathlib import Path
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser()
ap.add_argument("--json", action="store_true")
ap.add_argument("--write-md", action="store_true")
args = ap.parse_args()

data = json.loads((ROOT / "knowledge/api/coverage.json").read_text(encoding="utf-8"))
if args.json:
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"Verse API snapshot: {data['api_version']}")
    print(f"Known structured symbols: {data['symbol_count']}")
    print(f"Modules represented: {data.get('module_count', 0)}")
    for key, value in data["coverage"].items():
        print(f"- {key}: {value['count']}/{data['symbol_count']} ({value['percent']}%)")
    print("Revalidation:", data.get("revalidation", {}))
    print("Note:", data.get("note", ""))

if args.write_md:
    lines = [
        "# Verse API Coverage — V24", "",
        f"Snapshot: **{data['api_version']}**", "",
        f"Known structured symbols: **{data['symbol_count']}**", "",
        f"Modules represented: **{data.get('module_count', 0)}**", "",
        "| Field | Count | Coverage |", "|---|---:|---:|",
    ]
    for key, value in data["coverage"].items():
        lines.append(f"| `{key}` | {value['count']} | {value['percent']}% |")
    lines += [
        "",
        "These metrics describe evidence stored by this repository.",
        "They are not a claim about the total number of Verse APIs published by Epic.",
        "They are not UEFN compile results.",
        "",
    ]
    (ROOT / "reports/API_COVERAGE.md").write_text("\n".join(lines), encoding="utf-8")
