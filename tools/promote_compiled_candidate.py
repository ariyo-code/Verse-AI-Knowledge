#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"
REG=json.loads((ROOT/"external/sources.json").read_text(encoding="utf-8"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate_id")
    args=ap.parse_args()

    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    e=next((x for x in q["entries"] if x["candidate_id"]==args.candidate_id),None)
    if not e:
        raise SystemExit("Candidate not found.")

    if not e.get("local_verification",{}).get("compiled"):
        raise SystemExit("Promotion blocked: no local UEFN compile evidence.")

    if e.get("queue_status") not in {"compiled","runtime-pending","verified"}:
        raise SystemExit(f"Promotion blocked from queue status: {e.get('queue_status')}")

    srcmeta=next((x for x in REG["approved_sources"] if x["id"]==e["source_id"]),None)
    if not srcmeta or not srcmeta.get("license_verified"):
        raise SystemExit("Promotion blocked: source license not approved.")

    src=ROOT/"external/corpus"/e["source_id"]/e["source_revision"]/e["source_path"]
    if not src.exists():
        raise SystemExit(f"Source missing: {src}")

    destdir=ROOT/"examples/compiled/external"/e["source_id"]/e["candidate_id"]
    destdir.mkdir(parents=True,exist_ok=True)
    dest=destdir/src.name
    shutil.copy2(src,dest)

    metadata={
        "title":src.name,
        "status":"compiled",
        "source_id":e["source_id"],
        "source_repository":srcmeta["repository"],
        "source_revision":e["source_revision"],
        "source_path":e["source_path"],
        "license":srcmeta["license"],
        "local_verification":e["local_verification"],
        "compile_attempts":e.get("compile_attempts",[]),
        "warning":"Compiled means UEFN compilation succeeded. Runtime behavior may still be unverified."
    }
    (destdir/"metadata.json").write_text(
        json.dumps(metadata,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )

    # Preserve upstream license file if synchronized.
    base=ROOT/"external/corpus"/e["source_id"]/e["source_revision"]
    lic=base/"LICENSE"
    if lic.exists():
        shutil.copy2(lic,destdir/"LICENSE")

    print(destdir)

if __name__=="__main__":
    main()
