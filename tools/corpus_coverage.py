#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]
M=json.loads((ROOT/"external/corpus_manifest.json").read_text())
base=ROOT/"external/corpus"/M["source_id"]/M["source_revision"]
ex=list((base/"examples").rglob("*.verse")) if (base/"examples").exists() else []
sn=list((base/"snippets").rglob("*.verse")) if (base/"snippets").exists() else []
out={"local_examples":len(ex),"expected_examples":M["expected_examples"],
     "coverage_percent":round(len(ex)/M["expected_examples"]*100,2),
     "examples_complete":len(ex)>=M["expected_examples"],
     "missing_examples_estimate":max(0,M["expected_examples"]-len(ex)),
     "local_snippets":len(sn)}
ap=argparse.ArgumentParser(); ap.add_argument("--json",action="store_true"); a=ap.parse_args()
if a.json: print(json.dumps(out,indent=2))
else:
    print(f"Examples: {out['local_examples']}/{out['expected_examples']} ({out['coverage_percent']}%)")
    print(f"Full examples corpus: {'yes' if out['examples_complete'] else 'no'}")
    print(f"Estimated missing examples: {out['missing_examples_estimate']}")
