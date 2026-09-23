#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
from datetime import datetime, timezone


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    p = argparse.ArgumentParser(description="Create an evidence-guarded V22 promotion record.")
    p.add_argument("artifact")
    p.add_argument("--from-status", required=True, choices=["draft", "static-checked", "compiled", "verified"])
    p.add_argument("--to-status", required=True, choices=["static-checked", "compiled", "verified", "multiplayer-verified"])
    p.add_argument("--verse-api", default="42.20")
    p.add_argument("--static-checked", action="store_true")
    p.add_argument("--compiled", action="store_true")
    p.add_argument("--runtime-tested", action="store_true")
    p.add_argument("--multiplayer-tested", action="store_true")
    p.add_argument("--evidence", action="append", default=[])
    p.add_argument("--output-dir", default="verification/promotions")
    args = p.parse_args()

    if args.to_status in {"static-checked", "compiled", "verified", "multiplayer-verified"} and not args.static_checked:
        raise SystemExit("Promotion blocked: static check evidence required.")
    if args.to_status in {"compiled", "verified", "multiplayer-verified"} and not args.compiled:
        raise SystemExit("Promotion blocked: actual compile evidence required.")
    if args.to_status in {"verified", "multiplayer-verified"} and not args.runtime_tested:
        raise SystemExit("Promotion blocked: runtime evidence required.")
    if args.to_status == "multiplayer-verified" and not args.multiplayer_tested:
        raise SystemExit("Promotion blocked: multiplayer evidence required.")
    if args.to_status in {"compiled", "verified", "multiplayer-verified"} and not args.evidence:
        raise SystemExit("Promotion blocked: provide at least one evidence reference.")

    record = {
        "artifact": args.artifact,
        "from_status": args.from_status,
        "to_status": args.to_status,
        "verse_api": args.verse_api,
        "promoted_at": now(),
        "checks": {
            "static_checked": args.static_checked,
            "compiled": args.compiled,
            "runtime_tested": args.runtime_tested,
            "multiplayer_tested": args.multiplayer_tested,
        },
        "evidence": args.evidence,
        "notes": None,
    }
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    safe = args.artifact.replace("\\", "_").replace("/", "_").replace(" ", "_")
    path = outdir / f"{safe}-{args.to_status}.json"
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
