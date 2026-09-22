#!/usr/bin/env python3
from pathlib import Path
import argparse, re
from error_memory_lib import read_entries, normalize_message

def tokens(text):
    return set(re.findall(r"[a-zA-Z0-9_./<>-]+", text.lower()))

def score(query, entry):
    q=tokens(query)
    corpus=" ".join([
        entry.get("exact_message",""),
        entry.get("normalized_message","") or "",
        entry.get("cause","") or "",
        entry.get("correction","") or "",
        " ".join(entry.get("tags",[])),
        " ".join(entry.get("related_api",[])),
        " ".join(entry.get("related_files",[])),
    ]).lower()
    s=0
    for t in q:
        if t in corpus:
            s += 4
        if t in (entry.get("normalized_message","") or ""):
            s += 5
    if entry.get("status")=="verified":
        s += 3
    elif entry.get("status")=="fixed":
        s += 2
    elif entry.get("status")=="diagnosed":
        s += 1
    return s

def main():
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit",type=int,default=10)
    args=p.parse_args()

    rows=[]
    for e in read_entries():
        s=score(args.query,e)
        if s:
            rows.append((s,e))
    rows.sort(key=lambda x:(-x[0],x[1].get("id","")))

    if not rows:
        print("No matching stored error. Use exact UEFN/compiler feedback; do not invent a diagnosis.")
        return

    for s,e in rows[:args.limit]:
        print(f"[{s}] {e.get('id')}  status={e.get('status')}  category={e.get('category')}")
        print(" message:", e.get("exact_message","")[:220].replace("\n"," "))
        if e.get("cause"):
            print(" cause:", e["cause"][:220].replace("\n"," "))
        if e.get("correction"):
            print(" fix:", e["correction"][:220].replace("\n"," "))
        print()

if __name__=="__main__":
    main()
