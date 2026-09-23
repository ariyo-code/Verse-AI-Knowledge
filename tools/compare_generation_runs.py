#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser(); ap.add_argument('baseline'); ap.add_argument('candidate'); a=ap.parse_args(); b=json.loads(Path(a.baseline).read_text()); c=json.loads(Path(a.candidate).read_text()); bm=b.get('metrics') or {}; cm=c.get('metrics') or {}
keys=['unknown_api_like_claims','unsupported_exact_signature_claims','todo_api_verify','first_pass_compile_rate','average_compile_corrections']
print(f"Baseline: {b.get('knowledge_version')}  Candidate: {c.get('knowledge_version')}")
for k in keys:
 bv=bm.get(k); cv=cm.get(k); delta=None if bv is None or cv is None else round(cv-bv,3); print(f"{k}: {bv} -> {cv}  delta={delta}")
print('No winner is inferred when metrics are missing; compile metrics require real UEFN evidence.')
