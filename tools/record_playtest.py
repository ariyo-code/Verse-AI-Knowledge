#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone
from lab_state import ROOT,load_queue,save_queue,get_entry,transition

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate_id")
    ap.add_argument("--runtime",action="store_true")
    ap.add_argument("--multiplayer",action="store_true")
    ap.add_argument("--evidence",required=True)
    args=ap.parse_args()

    if args.multiplayer:
        args.runtime=True

    q=load_queue()
    e=get_entry(q,args.candidate_id)

    if not e.get("local_verification",{}).get("compiled"):
        raise SystemExit("Playtest promotion blocked: candidate has not compiled locally.")

    tests=e.setdefault("playtests",[])
    tests.append({
        "timestamp":now(),
        "runtime":args.runtime,
        "multiplayer":args.multiplayer,
        "evidence":args.evidence
    })

    if args.runtime:
        e["local_verification"]["runtime_tested"]=True
    if args.multiplayer:
        e["local_verification"]["multiplayer_tested"]=True

    status=e["queue_status"]
    if args.multiplayer:
        if status=="compiled":
            transition(e,"verified")
            status="verified"
        elif status=="runtime-pending":
            transition(e,"verified")
            status="verified"
        if status=="verified":
            transition(e,"multiplayer-verified")
    elif args.runtime:
        if status=="compiled":
            transition(e,"verified")
        elif status=="runtime-pending":
            transition(e,"verified")

    save_queue(q)
    print(f"{e['candidate_id']} -> {e['queue_status']}")

if __name__=="__main__":
    main()
