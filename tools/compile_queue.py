#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"

def load():
    if not QUEUE.exists():
        raise SystemExit("Compile queue missing. Run tools/build_compile_queue.py.")
    return json.loads(QUEUE.read_text(encoding="utf-8"))

def save(q):
    QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False),encoding="utf-8")

def main():
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest="cmd",required=True)

    sub.add_parser("list")
    sub.add_parser("next")

    show=sub.add_parser("show")
    show.add_argument("candidate_id")

    status=sub.add_parser("status")
    status.add_argument("candidate_id")
    status.add_argument("status",choices=[
        "pending","staged","compiling","compile-failed",
        "blocked-environment","compiled","runtime-pending",
        "verified","skipped"
    ])
    status.add_argument("--note")

    args=ap.parse_args()
    q=load()
    entries=q["entries"]

    if args.cmd=="list":
        for x in entries:
            print(f"{x['candidate_id']}  {x['queue_status']:20} score={x['curation_score']:5} {x['source_path']}")
        return

    if args.cmd=="next":
        x=next((x for x in entries if x["queue_status"]=="pending"),None)
        if not x:
            print("No pending candidate.")
            return
        print(json.dumps(x,indent=2,ensure_ascii=False))
        return

    x=next((x for x in entries if x["candidate_id"]==args.candidate_id),None)
    if not x:
        raise SystemExit("Candidate not found.")

    if args.cmd=="show":
        print(json.dumps(x,indent=2,ensure_ascii=False))
        return

    if args.cmd=="status":
        x["queue_status"]=args.status
        if args.note:
            x["notes"]=args.note
        save(q)
        print(f"{args.candidate_id} -> {args.status}")

if __name__=="__main__":
    main()
