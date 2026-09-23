#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"
CURRENT=ROOT/"lab/current_candidate.json"

ALLOWED={
    "pending":{"staged","skipped"},
    "staged":{"compiling","pending","blocked-environment","compile-failed"},
    "compiling":{"compiled","compile-failed","blocked-environment"},
    "compile-failed":{"pending","skipped"},
    "blocked-environment":{"pending","skipped"},
    "compiled":{"runtime-pending","verified"},
    "runtime-pending":{"verified"},
    "verified":{"multiplayer-verified"},
    "multiplayer-verified":set(),
    "skipped":{"pending"}
}

def load_queue():
    return json.loads(QUEUE.read_text(encoding="utf-8"))

def save_queue(q):
    QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False),encoding="utf-8")

def get_entry(q,cid):
    for x in q.get("entries",[]):
        if x.get("candidate_id")==cid:
            return x
    raise KeyError(cid)

def transition(entry,new_status):
    old=entry.get("queue_status")
    if new_status==old:
        return
    if new_status not in ALLOWED.get(old,set()):
        raise ValueError(f"Invalid VerseLab transition: {old} -> {new_status}")
    entry["queue_status"]=new_status

def current():
    if not CURRENT.exists():
        return None
    return json.loads(CURRENT.read_text(encoding="utf-8"))

def set_current(obj):
    CURRENT.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding="utf-8")

def clear_current():
    if CURRENT.exists():
        CURRENT.unlink()
