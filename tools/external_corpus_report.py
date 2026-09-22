#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
REG=json.loads((ROOT/"external/sources.json").read_text(encoding="utf-8"))

print("Approved sources:")
for src in REG["approved_sources"]:
    claim=src.get("claimed_verification",{})
    print(
        f"- {src['id']}: {src['repository']} | "
        f"license={src['license']} | trust={src['trust']} | "
        f"upstream_examples={claim.get('examples_count','?')}"
    )

print()
print("Reference only:")
for src in REG["reference_only"]:
    print(f"- {src['repository']}: {src['reason']}")

corpus=ROOT/"external/corpus"
if corpus.exists():
    verse=list(corpus.rglob("*.verse"))
    print()
    print(f"Local synchronized .verse files: {len(verse)}")
else:
    print()
    print("Local synchronized corpus: not downloaded yet.")
