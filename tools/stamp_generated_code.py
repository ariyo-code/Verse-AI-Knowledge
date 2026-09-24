#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, subprocess
ROOT=Path(__file__).resolve().parents[1]
CONF=json.loads((ROOT/'portable/generated_code_marker.json').read_text(encoding='utf-8'))
ap=argparse.ArgumentParser(); ap.add_argument('file'); ap.add_argument('--status',default='draft',choices=CONF['allowed_statuses']); ap.add_argument('--api',default='42.20'); ap.add_argument('--artifact-id'); ap.add_argument('--compiled',action='store_true'); ap.add_argument('--runtime',action='store_true'); ap.add_argument('--multiplayer',action='store_true'); ap.add_argument('--repo-revision'); args=ap.parse_args()
code=Path(args.file).read_text(encoding='utf-8'); uncertain=len(re.findall(r'TODO\(API VERIFY\)',code)); artifact=args.artifact_id or 'VAI-'+hashlib.sha1(code.encode()).hexdigest()[:12].upper()
compiled=args.compiled or args.status in {'compiled','verified','multiplayer-verified'}; runtime=args.runtime or args.status in {'verified','multiplayer-verified'}; multiplayer=args.multiplayer or args.status=='multiplayer-verified'
if runtime and not compiled: raise SystemExit('runtime evidence requires compiled evidence')
if multiplayer and not runtime: raise SystemExit('multiplayer evidence requires runtime evidence')
rev=args.repo_revision
if not rev:
    try: rev=subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception: rev='unknown'
lab=lambda x:'EVIDENCE RECORDED' if x else 'NOT TESTED'
print(f'> **Verse AI Knowledge · V25**  '); print(f'> Status: `{args.status}` · API snapshot: `{args.api}` · UEFN compile: `{lab(compiled)}` · Runtime: `{lab(runtime)}` · Multiplayer: `{lab(multiplayer)}`')
if uncertain: print(f'> ⚠ API verification required: `{uncertain}` unresolved exact API claim(s).')
print(); print('```verse'); print(code.rstrip()); print('```'); print()
print(f'<!-- verse-ai-provenance:v25;lang=verse;artifact={artifact};knowledge_release=25.0.0;repo_revision={rev};api={args.api};status={args.status};compiled={str(compiled).lower()};runtime={str(runtime).lower()};multiplayer={str(multiplayer).lower()};api_verify_required={str(bool(uncertain)).lower()};uncertain_api_count={uncertain};claim_resolution=field-level -->')
