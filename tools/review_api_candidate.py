#!/usr/bin/env python3
"""Create/replace one REVIEWED official API evidence record.

The reviewer must supply exact claims only after checking the official Epic page.
V24 records which fields were actually reviewed.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.epic_http import validate_epic_url  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("symbol")
ap.add_argument("--signature")
ap.add_argument("--source-url", required=True)
ap.add_argument("--reviewed-by", default="manual-review")
ap.add_argument("--api-version", default="42.20")
ap.add_argument("--notes")
ap.add_argument("--fields", default="signature,parameters,return_type,effects",
                help="Comma-separated fields actually reviewed.")
args = ap.parse_args()

source_url = validate_epic_url(args.source_url)
known = {
    json.loads(x)["symbol_id"]
    for x in (ROOT / "knowledge/api/symbols.jsonl").read_text(encoding="utf-8").splitlines()
    if x.strip()
}
if args.symbol not in known:
    raise SystemExit("Unknown local symbol. Add/discover symbol first; do not create it from memory.")

allowed_fields = {
    "presence", "module", "kind", "signature", "parameters", "return_type",
    "effects", "event_names", "event_payloads", "member_names",
}
fields = [x.strip() for x in args.fields.split(",") if x.strip()]
bad = [x for x in fields if x not in allowed_fields]
if bad:
    raise SystemExit("Unknown reviewed field(s): " + ", ".join(bad))
if "signature" in fields and not args.signature:
    raise SystemExit("signature field was declared reviewed but --signature is missing.")

now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
eid = "api-" + hashlib.sha1(
    f"{args.symbol}|{args.api_version}|{source_url}|{args.signature}|{','.join(sorted(fields))}".encode()
).hexdigest()[:16]

record = {
    "evidence_id": eid,
    "symbol_id": args.symbol,
    "api_version": args.api_version,
    "source_url": source_url,
    "reviewed_at": now,
    "reviewed_by": args.reviewed_by,
    "review_status": "verified",
    "fields_verified": fields,
    "signature": args.signature,
    "parameters": [],
    "return_type": None,
    "effects": [],
    "events": [],
    "notes": args.notes,
    "source_sha256": None,
}

path = ROOT / "knowledge/api/verification_records.jsonl"
rows = []
if path.exists():
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if row.get("symbol_id") != args.symbol:
            rows.append(row)
rows.append(record)
rows.sort(key=lambda x: x["symbol_id"].casefold())
path.write_text("".join(json.dumps(x, ensure_ascii=False, sort_keys=True) + "\n" for x in rows), encoding="utf-8")

print("Recorded reviewed evidence:", eid)
rc = subprocess.run([sys.executable, str(ROOT / "tools/migrate_api_catalog_v24.py")], cwd=ROOT).returncode
raise SystemExit(rc)
