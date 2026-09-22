#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone
from lab_state import (
    ROOT,load_queue,save_queue,get_entry,transition,
    current,set_current,clear_current
)

RESULTS=ROOT/"lab/results"

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)

    success=sub.add_parser("success")
    success.add_argument("--evidence",required=True)
    success.add_argument("--uefn-version",default="42.20")

    fail=sub.add_parser("fail")
    fail.add_argument("--classification",required=True,choices=[
        "syntax-or-language","api-or-version","unknown"
    ])
    fail.add_argument("--error",action="append",required=True)
    fail.add_argument("--uefn-version",default="42.20")
    fail.add_argument("--note")

    blocked=sub.add_parser("blocked")
    blocked.add_argument("--classification",required=True,choices=[
        "missing-dependency","project-environment"
    ])
    blocked.add_argument("--error",action="append",required=True)
    blocked.add_argument("--uefn-version",default="42.20")
    blocked.add_argument("--note")

    args=ap.parse_args()

    cur=current()
    if not cur:
        raise SystemExit("No active VerseLab candidate.")

    q=load_queue()
    e=get_entry(q,cur["candidate_id"])

    if e["queue_status"]=="staged":
        transition(e,"compiling")

    attempt={
        "attempt":len(e.get("compile_attempts",[]))+1,
        "timestamp":now(),
        "uefn_version":args.uefn_version,
        "original_untouched":bool(cur.get("original_untouched")),
        "success":args.cmd=="success",
        "blocked_environment":args.cmd=="blocked"
    }

    if args.cmd=="success":
        attempt["evidence"]=args.evidence
        attempt["exact_errors"]=[]
        attempt["classification"]=None
        transition(e,"compiled")
        e["local_verification"]["compiled"]=True
        e["failure_classification"]=None
    else:
        attempt["exact_errors"]=args.error
        attempt["classification"]=args.classification
        attempt["note"]=getattr(args,"note",None)
        e["failure_classification"]=args.classification
        if args.cmd=="blocked":
            transition(e,"blocked-environment")
        else:
            transition(e,"compile-failed")

    e.setdefault("compile_attempts",[]).append(attempt)
    save_queue(q)

    RESULTS.mkdir(parents=True,exist_ok=True)
    (RESULTS/f"{e['candidate_id']}.json").write_text(
        json.dumps({
            "candidate_id":e["candidate_id"],
            "source_path":e["source_path"],
            "status":e["queue_status"],
            "verification":e["local_verification"],
            "attempts":e["compile_attempts"]
        },indent=2,ensure_ascii=False),
        encoding="utf-8"
    )

    clear_current()
    print(f"{e['candidate_id']} -> {e['queue_status']}")
    print("Current candidate cleared.")
    print("You can stage the next candidate.")

if __name__=="__main__":
    main()
