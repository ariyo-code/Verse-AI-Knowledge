#!/usr/bin/env python3
import argparse
from maintenance_lib import load_json, save_json, now

def main():
    p=argparse.ArgumentParser()
    p.add_argument("index",type=int,help="1-based queue item index")
    p.add_argument("status",choices=["pending","reviewing","resolved","not-applicable"])
    p.add_argument("--note")
    args=p.parse_args()

    q=load_json("maintenance/revalidation_queue.json")
    items=q.get("items",[])
    i=args.index-1
    if i<0 or i>=len(items):
        raise SystemExit("Invalid queue index")

    items[i]["status"]=args.status
    items[i]["reviewed_at"]=now()
    if args.note:
        items[i]["review_note"]=args.note

    save_json("maintenance/revalidation_queue.json",q)
    print(f"Item {args.index} -> {args.status}")

if __name__=="__main__":
    main()
