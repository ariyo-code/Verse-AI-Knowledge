#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    p=argparse.ArgumentParser(description="Create a guarded promotion record.")
    p.add_argument("artifact")
    p.add_argument("--from-status",required=True,choices=["draft","compiled","verified"])
    p.add_argument("--to-status",required=True,choices=["compiled","verified","multiplayer-verified"])
    p.add_argument("--verse-api",default="42.20")
    p.add_argument("--compiled",action="store_true")
    p.add_argument("--runtime-tested",action="store_true")
    p.add_argument("--multiplayer-tested",action="store_true")
    p.add_argument("--evidence",action="append",default=[])
    p.add_argument("--output-dir",default="verification/promotions")
    args=p.parse_args()

    if args.to_status in {"compiled","verified","multiplayer-verified"} and not args.compiled:
        raise SystemExit("Promotion blocked: compiled evidence required.")
    if args.to_status in {"verified","multiplayer-verified"} and not args.runtime_tested:
        raise SystemExit("Promotion blocked: runtime test required.")
    if args.to_status=="multiplayer-verified" and not args.multiplayer_tested:
        raise SystemExit("Promotion blocked: multiplayer test required.")

    rec={
        "artifact":args.artifact,
        "from_status":args.from_status,
        "to_status":args.to_status,
        "verse_api":args.verse_api,
        "promoted_at":now(),
        "checks":{
            "compiled":args.compiled,
            "runtime_tested":args.runtime_tested,
            "multiplayer_tested":args.multiplayer_tested
        },
        "evidence":args.evidence,
        "notes":None
    }

    outdir=Path(args.output_dir)
    outdir.mkdir(parents=True,exist_ok=True)
    safe=args.artifact.replace("\\","_").replace("/","_").replace(" ","_")
    path=outdir/f"{safe}-{args.to_status}.json"
    path.write_text(json.dumps(rec,indent=2,ensure_ascii=False),encoding="utf-8")
    print(path)

if __name__=="__main__":
    main()
