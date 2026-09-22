#!/usr/bin/env python3
import argparse, json
from error_memory_lib import read_entries, write_entries, utc_now

def main():
    p=argparse.ArgumentParser(description="Update diagnosis/fix/verification for an existing real error.")
    p.add_argument("id")
    p.add_argument("--status", choices=["observed","diagnosed","fixed","verified","deprecated"])
    p.add_argument("--cause")
    p.add_argument("--correction")
    p.add_argument("--corrected-code")
    p.add_argument("--compiled", action="store_true")
    p.add_argument("--runtime-tested", action="store_true")
    p.add_argument("--multiplayer-tested", action="store_true")
    p.add_argument("--evidence")
    p.add_argument("--notes")
    args=p.parse_args()

    entries=read_entries()
    found=None
    for e in entries:
        if e.get("id")==args.id:
            found=e
            break
    if found is None:
        raise SystemExit(f"Unknown error id: {args.id}")

    if args.status: found["status"]=args.status
    if args.cause is not None: found["cause"]=args.cause
    if args.correction is not None: found["correction"]=args.correction
    if args.corrected_code is not None: found["corrected_code"]=args.corrected_code
    if args.notes is not None: found["notes"]=args.notes

    ver=found.setdefault("verification",{})
    if args.compiled: ver["compiled"]=True
    if args.runtime_tested: ver["runtime_tested"]=True
    if args.multiplayer_tested: ver["multiplayer_tested"]=True
    if args.evidence is not None: ver["evidence"]=args.evidence

    # Guard against false verified status.
    if found.get("status")=="verified":
        if not ver.get("compiled"):
            raise SystemExit("Cannot mark verified without compiled=true.")
        if not ver.get("runtime_tested"):
            raise SystemExit("Cannot mark verified without runtime_tested=true.")

    if found.get("status")=="fixed" and not ver.get("compiled"):
        raise SystemExit("Cannot mark fixed without compiled=true.")

    found["updated_at"]=utc_now()
    write_entries(entries)
    print(json.dumps(found,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
