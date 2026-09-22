#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/"external/corpus_manifest.json").read_text())
def count():
    p=ROOT/"external/corpus"/M["source_id"]/M["source_revision"]/"examples"
    return len(list(p.rglob("*.verse"))) if p.exists() else 0
n=count(); expected=M["expected_examples"]
if n>=expected:
    print(f"Corpus complete: {n}/{expected}"); raise SystemExit(0)
print(f"Corpus incomplete: {n}/{expected}")
cmd=[sys.executable,str(ROOT/"tools/sync_external_sources.py"),
     "--source",M["source_id"],"--examples-only"]
r=subprocess.run(cmd)
if r.returncode: raise SystemExit(r.returncode)
n=count(); print(f"Corpus after sync: {n}/{expected}")
if n<expected: raise SystemExit("Full corpus not confirmed.")
