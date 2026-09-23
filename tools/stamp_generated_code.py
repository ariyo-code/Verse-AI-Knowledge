#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
CONF = json.loads((ROOT / "portable/generated_code_marker.json").read_text(encoding="utf-8"))

ap = argparse.ArgumentParser()
ap.add_argument("file")
ap.add_argument("--status", default="draft", choices=CONF["allowed_statuses"])
ap.add_argument("--api", default="42.20")
ap.add_argument("--artifact-id")
ap.add_argument("--compiled", action="store_true")
ap.add_argument("--runtime", action="store_true")
ap.add_argument("--multiplayer", action="store_true")
args = ap.parse_args()

path = Path(args.file)
code = path.read_text(encoding="utf-8")
uncertain = len(re.findall(r"TODO\(API VERIFY\)", code))
artifact_id = args.artifact_id or ("VAI-" + hashlib.sha1(code.encode()).hexdigest()[:12].upper())

compiled = args.compiled or args.status in {"compiled", "verified", "multiplayer-verified"}
runtime = args.runtime or args.status in {"verified", "multiplayer-verified"}
multiplayer = args.multiplayer or args.status == "multiplayer-verified"

if runtime and not compiled:
    raise SystemExit("runtime evidence requires compiled evidence.")
if multiplayer and not runtime:
    raise SystemExit("multiplayer evidence requires runtime evidence.")
if args.status in {"compiled", "verified", "multiplayer-verified"} and not compiled:
    raise SystemExit("Cannot stamp compiled status without evidence.")
if args.status in {"verified", "multiplayer-verified"} and not runtime:
    raise SystemExit("Cannot stamp verified status without runtime evidence.")
if args.status == "multiplayer-verified" and not multiplayer:
    raise SystemExit("Cannot stamp multiplayer-verified without multiplayer evidence.")

compile_label = "EVIDENCE RECORDED" if compiled else "NOT TESTED"
runtime_label = "EVIDENCE RECORDED" if runtime else "NOT TESTED"
multiplayer_label = "EVIDENCE RECORDED" if multiplayer else "NOT TESTED"

visible = (
    f"> **Verse AI Knowledge · V24**  \n"
    f"> Status: `{args.status}` · API snapshot: `{args.api}` · "
    f"UEFN compile: `{compile_label}` · Runtime: `{runtime_label}` · Multiplayer: `{multiplayer_label}`"
)
if uncertain:
    visible += f"  \n> ⚠ API verification required: `{uncertain}` unresolved exact API claim(s)."

hidden = (
    f"<!-- verse-ai-generated:v24;lang=verse;artifact={artifact_id};status={args.status};api={args.api};"
    f"compiled={str(compiled).lower()};runtime={str(runtime).lower()};multiplayer={str(multiplayer).lower()};"
    f"api_verify_required={str(bool(uncertain)).lower()};uncertain_api_count={uncertain};claim_resolution=field-level -->"
)

print(visible)
print()
print("```verse")
print(code.rstrip())
print("```")
print()
print(hidden)
