#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--limit",type=int,default=50)
    ap.add_argument("--replace",action="store_true")
    args=ap.parse_args()

    curated=ROOT/"curation/curated_examples.json"
    if not curated.exists():
        raise SystemExit("Run tools/curate_external_examples.py first.")

    data=json.loads(curated.read_text(encoding="utf-8"))
    dest=ROOT/"lab/compile_queue.json"

    existing={}
    if dest.exists() and not args.replace:
        old=json.loads(dest.read_text(encoding="utf-8"))
        existing={x["candidate_id"]:x for x in old.get("entries",[])}

    entries=[]
    for row in data.get("examples",[])[:args.limit]:
        cid=row["id"]
        if cid in existing:
            entries.append(existing[cid])
            continue

        entries.append({
            "candidate_id":cid,
            "source_id":row["source_id"],
            "source_revision":data["source_revision"],
            "source_path":row["path"],
            "curation_score":row["score"],
            "category":row["category"],
            "devices":row["devices"],
            "api_symbols":row["api_symbols"],
            "features":row["features"],
            "project_relevance":row["project_relevance"],
            "upstream_status":row["status"],
            "queue_status":"pending",
            "failure_classification":None,
            "local_verification":{
                "compiled":False,
                "runtime_tested":False,
                "multiplayer_tested":False
            },
            "compile_attempts":[],
            "notes":None
        })

    queue={
        "schema_version":1,
        "generated_at":now(),
        "source_id":data["source_id"],
        "source_revision":data["source_revision"],
        "entries":entries
    }
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(json.dumps(queue,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Compile queue: {len(entries)} candidate(s)")
    print(dest)

if __name__=="__main__":
    main()
