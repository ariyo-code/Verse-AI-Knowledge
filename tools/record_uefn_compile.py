#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"
RESULTS=ROOT/"lab/results"

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate_id")
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--success",action="store_true")
    group.add_argument("--failure",action="store_true")
    group.add_argument("--blocked",action="store_true")
    ap.add_argument("--uefn-version",default="42.20")
    ap.add_argument("--error",action="append",default=[])
    ap.add_argument("--classification",choices=[
        "syntax-or-language","api-or-version","missing-dependency",
        "project-environment","unknown"
    ])
    ap.add_argument("--evidence")
    ap.add_argument("--note")
    args=ap.parse_args()

    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    e=next((x for x in q["entries"] if x["candidate_id"]==args.candidate_id),None)
    if not e:
        raise SystemExit("Candidate not found.")

    attempt={
        "attempt":len(e.get("compile_attempts",[]))+1,
        "timestamp":now(),
        "uefn_version":args.uefn_version,
        "success":bool(args.success),
        "blocked_environment":bool(args.blocked),
        "classification":args.classification,
        "exact_errors":args.error,
        "evidence":args.evidence,
        "note":args.note
    }
    e.setdefault("compile_attempts",[]).append(attempt)

    if args.success:
        e["queue_status"]="compiled"
        e["failure_classification"]=None
        e["local_verification"]["compiled"]=True
    elif args.blocked:
        e["queue_status"]="blocked-environment"
        e["failure_classification"]=args.classification or "project-environment"
    else:
        e["queue_status"]="compile-failed"
        e["failure_classification"]=args.classification or "unknown"

    QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False),encoding="utf-8")

    RESULTS.mkdir(parents=True,exist_ok=True)
    result_path=RESULTS/f"{args.candidate_id}.json"
    result_path.write_text(json.dumps({
        "candidate_id":args.candidate_id,
        "source_id":e["source_id"],
        "source_path":e["source_path"],
        "queue_status":e["queue_status"],
        "local_verification":e["local_verification"],
        "attempts":e["compile_attempts"]
    },indent=2,ensure_ascii=False),encoding="utf-8")

    print(f"{args.candidate_id} -> {e['queue_status']}")
    print(result_path)

if __name__=="__main__":
    main()
