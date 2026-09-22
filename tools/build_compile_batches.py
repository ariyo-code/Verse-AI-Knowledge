#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--size",type=int,default=10)
    args=ap.parse_args()

    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    entries=q.get("entries",[])

    outdir=ROOT/"lab/batches"
    outdir.mkdir(parents=True,exist_ok=True)

    # Clear generated markdown only.
    for p in outdir.glob("BATCH_*.md"):
        p.unlink()

    index=[]
    for start in range(0,len(entries),args.size):
        batch=entries[start:start+args.size]
        n=start//args.size+1
        bid=f"{n:03d}"
        path=outdir/f"BATCH_{bid}.md"

        lines=[
            f"# VerseLab Batch {bid}",
            "",
            f"Candidates {start+1}–{start+len(batch)} of {len(entries)}",
            ""
        ]
        for i,e in enumerate(batch,start+1):
            lines += [
                f"## {i}. `{e['candidate_id']}`",
                "",
                f"- Source: `{e['source_path']}`",
                f"- Score: `{e.get('curation_score')}`",
                f"- Status: `{e.get('queue_status')}`",
                f"- Features: {', '.join(e.get('features',[])) or 'none'}",
                f"- API signals: {', '.join(e.get('api_symbols',[])) or 'none'}",
                ""
            ]

        path.write_text("\n".join(lines),encoding="utf-8")
        index.append({
            "batch":bid,
            "path":str(path.relative_to(ROOT)).replace("\\","/"),
            "candidate_ids":[x["candidate_id"] for x in batch]
        })

    (outdir/"index.json").write_text(
        json.dumps({"batch_size":args.size,"batches":index},indent=2),
        encoding="utf-8"
    )
    print(f"{len(index)} batch(es) generated.")

if __name__=="__main__":
    main()
