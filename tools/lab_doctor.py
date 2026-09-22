#!/usr/bin/env python3
from pathlib import Path
import argparse,json,sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]

def check(label,ok,detail=""):
    icon="OK" if ok else "MISSING"
    print(f"[{icon}] {label}" + (f": {detail}" if detail else ""))
    return ok

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--verse-dir")
    args=ap.parse_args()

    good=True

    good &= check("Python",True,sys.version.split()[0])
    good &= check("manifest", (ROOT/"manifest.json").exists())
    good &= check("compile queue",(ROOT/"lab/compile_queue.json").exists())

    source=ROOT/"external/corpus/uefncentral-examples"
    synced=source.exists() and any(source.iterdir())
    good &= check("UEFN Central corpus",synced,str(source))

    if args.verse_dir:
        vd=Path(args.verse_dir)
        good &= check("VerseLab Verse directory",vd.exists(),str(vd))

    if (ROOT/"lab/compile_queue.json").exists():
        q=json.loads((ROOT/"lab/compile_queue.json").read_text(encoding="utf-8"))
        c=Counter(x.get("queue_status") for x in q.get("entries",[]))
        print("[INFO] queue:",dict(c))

    current=ROOT/"lab/current_candidate.json"
    if current.exists():
        c=json.loads(current.read_text(encoding="utf-8"))
        print("[INFO] active candidate:",c.get("candidate_id"))
    else:
        print("[INFO] active candidate: none")

    if not good:
        raise SystemExit(1)

if __name__=="__main__":
    main()
