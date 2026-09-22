#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
DUPS=ROOT/"curation/semantic_duplicates.json"
QUEUE=ROOT/"lab/compile_queue.json"

if not DUPS.exists():
    raise SystemExit("Run detect_semantic_duplicates.py first.")

d=json.loads(DUPS.read_text(encoding="utf-8"))
q=json.loads(QUEUE.read_text(encoding="utf-8"))
by_path={e["source_path"]:e for e in q["entries"]}

changed=0
for group in d.get("groups",[]):
    paths=[]
    for full in group["files"]:
        marker="/examples/"
        if marker in full:
            paths.append("examples/"+full.split(marker,1)[1])
    candidates=[by_path[p] for p in paths if p in by_path]
    candidates.sort(key=lambda e:(-e.get("curation_score",0),e["source_path"]))
    if len(candidates)>1:
        keep=candidates[0]
        for e in candidates[1:]:
            if e["queue_status"]=="pending":
                e["queue_status"]="skipped"
                e["notes"]=f"Semantic duplicate of {keep['candidate_id']} ({keep['source_path']}); compile representative first."
                changed+=1

QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False),encoding="utf-8")
print(f"Duplicate candidates skipped: {changed}")
