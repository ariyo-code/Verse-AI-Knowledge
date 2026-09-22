#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil,re

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"
REG=json.loads((ROOT/"external/sources.json").read_text(encoding="utf-8"))

def source_base(source_id,revision):
    return ROOT/"external/corpus"/source_id/revision

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate_id")
    ap.add_argument("--uefn-verse-dir",required=True)
    args=ap.parse_args()

    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    entry=next((x for x in q["entries"] if x["candidate_id"]==args.candidate_id),None)
    if not entry:
        raise SystemExit("Candidate not found.")

    src=source_base(entry["source_id"],entry["source_revision"])/entry["source_path"]
    if not src.exists():
        raise SystemExit(f"Source file missing: {src}")

    destdir=Path(args.uefn_verse_dir)
    destdir.mkdir(parents=True,exist_ok=True)

    safe=re.sub(r"[^A-Za-z0-9_.-]+","_",Path(entry["source_path"]).name)
    dest=destdir/f"VAI_{entry['candidate_id']}_{safe}"

    shutil.copy2(src,dest)

    # Stage only one candidate at a time to keep compile evidence attributable.
    entry["queue_status"]="staged"
    entry["staged_path"]=str(dest)
    QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False),encoding="utf-8")

    staged={
        "candidate_id":entry["candidate_id"],
        "source_id":entry["source_id"],
        "source_revision":entry["source_revision"],
        "source_path":entry["source_path"],
        "staged_path":str(dest),
        "warning":"Staging is not compile proof. Compile this candidate in UEFN."
    }
    out=ROOT/"lab/staged_current.json"
    out.write_text(json.dumps(staged,indent=2,ensure_ascii=False),encoding="utf-8")

    print(dest)
    print(out)

if __name__=="__main__":
    main()
