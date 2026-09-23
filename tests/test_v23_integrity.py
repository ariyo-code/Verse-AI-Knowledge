#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.api_index import load_symbols
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')); assert m['schema_version']==23; assert m['release']['version']=='23.0.0'
rows=load_symbols(ROOT); assert rows
for r in rows:
 assert r['signature_state'] in {'missing','candidate','verified'}; assert isinstance(r['parameters'],list); assert isinstance(r['coverage'],dict); assert isinstance(r['evidence_ids'],list)
 if r['exact_signature_claim_allowed']:
  assert r['signature_state']=='verified' and r['signature']
marker=json.loads((ROOT/'portable/generated_code_marker.json').read_text(encoding='utf-8')); assert marker['marker_version']=='v23'; assert marker['safety']['invisible_unicode'] is False
print('V23 integrity unit tests OK')
