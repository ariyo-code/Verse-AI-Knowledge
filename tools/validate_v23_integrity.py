#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
def check(ok,msg):
 if not ok: errors.append(msg)
def load(rel):
 p=ROOT/rel
 if not p.exists(): errors.append(f'missing: {rel}'); return {}
 try: return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e: errors.append(f'{rel}: invalid JSON: {e}'); return {}
m=load('manifest.json'); check(m.get('schema_version')==23,'manifest schema_version must be 23'); check(m.get('release',{}).get('version')=='23.0.0','release version must be 23.0.0')
marker=load('portable/generated_code_marker.json'); check(marker.get('marker_version')=='v23','marker must be v23'); check(marker.get('safety',{}).get('invisible_unicode') is False,'invisible Unicode must be forbidden')
required=['AI_BOOTSTRAP.md','docs/architecture/V23_API_COVERAGE.md','schemas/api_evidence.schema.json','schemas/generated_artifact.schema.json','knowledge/api/coverage.json','knowledge/api/verification_queue.json','knowledge/api/verification_records.jsonl','evals/generation/tasks.json','tools/migrate_api_catalog_v23.py','tools/api_coverage_report.py','tools/stamp_generated_code.py']
for rel in required: check((ROOT/rel).exists(),f'missing: {rel}')
rows=[]
for n,line in enumerate((ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines(),1):
 if not line.strip(): continue
 try: r=json.loads(line); rows.append(r)
 except Exception as e: errors.append(f'symbols.jsonl:{n}: {e}'); continue
 for key in ['signature_state','parameters','return_type','coverage','evidence_ids']: check(key in r,f'symbols.jsonl:{n}: missing V23 field {key}')
 if r.get('signature_state')=='verified': check(r.get('exact_signature_claim_allowed') is True,f"{r.get('symbol_id')}: verified signature state without exact claim permission")
 if r.get('exact_signature_claim_allowed'): check(bool(r.get('signature')),f"{r.get('symbol_id')}: exact signature allowed without signature")
cov=load('knowledge/api/coverage.json'); check(cov.get('symbol_count')==len(rows),'coverage symbol_count mismatch')
q=load('knowledge/api/verification_queue.json'); check(q.get('pending_count')==sum(not r.get('exact_signature_claim_allowed') for r in rows),'verification queue count mismatch')
if errors:
 print('V23 integrity FAILED'); [print('-',e) for e in sorted(set(errors))]; raise SystemExit(1)
print('V23 integrity OK'); print('UEFN compile status: NOT TESTED by this validator')
