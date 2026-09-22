#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil,re
from lab_state import ROOT,load_queue,save_queue,transition,set_current,current

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--uefn-verse-dir",required=True)
    args=ap.parse_args()

    existing=current()
    if existing:
        raise SystemExit(
            f"A candidate is already active: {existing.get('candidate_id')}. "
            "Record its result before staging another."
        )

    q=load_queue()
    e=next((x for x in q["entries"] if x.get("queue_status")=="pending"),None)
    if not e:
        raise SystemExit("No pending candidate.")

    src=ROOT/"external/corpus"/e["source_id"]/e["source_revision"]/e["source_path"]
    if not src.exists():
        raise SystemExit(
            f"Candidate source is not synchronized:\n{src}\n"
            f"Run tools/sync_external_sources.py --source {e['source_id']} --verse-only"
        )

    verse_dir=Path(args.uefn_verse_dir)
    verse_dir.mkdir(parents=True,exist_ok=True)

    stage_root=verse_dir/"VAI_LAB"
    stage_root.mkdir(parents=True,exist_ok=True)

    # Safety: only remove files created by this runner.
    for p in stage_root.glob("VAI_*.verse"):
        p.unlink()

    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",src.name)
    dest=stage_root/f"VAI_{e['candidate_id']}_{safe}"
    shutil.copy2(src,dest)

    transition(e,"staged")
    save_queue(q)

    obj={
        "candidate_id":e["candidate_id"],
        "source_id":e["source_id"],
        "source_revision":e["source_revision"],
        "source_path":e["source_path"],
        "staged_path":str(dest),
        "original_untouched":True,
        "first_compile_recorded":False
    }
    set_current(obj)

    print("Candidate:",e["candidate_id"])
    print("Source:",e["source_path"])
    print("Staged:",dest)
    print("Status: staged")
    print()
    print("Compile this exact file in UEFN before editing it.")

if __name__=="__main__":
    main()
