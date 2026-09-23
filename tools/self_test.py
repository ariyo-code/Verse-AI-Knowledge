#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
errors=[]
for rel in [
 'manifest.json','knowledge/api_catalog.json','knowledge/module_catalog.json','knowledge/api/modules.json',
 'knowledge/api/versions.json','rag/config.json','rag/evidence_policy.json','portable/generated_code_marker.json',
 'evals/hallucination/cases.json','evals/retrieval/evidence_composition.json'
]:
    p=ROOT/rel
    if not p.exists(): errors.append(f'missing {rel}'); continue
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc: errors.append(f'{rel}: {exc}')
jsonl=ROOT/'knowledge/api/symbols.jsonl'
if not jsonl.exists(): errors.append('missing knowledge/api/symbols.jsonl')
else:
    for n,line in enumerate(jsonl.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        try: json.loads(line)
        except Exception as exc: errors.append(f'symbols.jsonl:{n}: {exc}')
if errors:
    print('Static self-test FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('Static self-test OK')
print('This test did not compile Verse in UEFN.')
