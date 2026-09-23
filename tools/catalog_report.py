#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
legacy=json.loads((ROOT/'knowledge/api_catalog.json').read_text(encoding='utf-8'))
rows=[json.loads(x) for x in (ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
coverage=json.loads((ROOT/'knowledge/api/coverage.json').read_text(encoding='utf-8'))
print(f"Verse API snapshot: {coverage.get('api_version')}")
print(f"Legacy catalog last verified: {legacy.get('last_verified')}")
print(f"Structured symbols: {len(rows)}")
print(f"Exact signatures verified: {coverage['coverage']['signature_verified']['count']}/{len(rows)} ({coverage['coverage']['signature_verified']['percent']}%)")
print(f"Event names known: {coverage['coverage']['event_names_known']['count']}/{len(rows)} ({coverage['coverage']['event_names_known']['percent']}%)")
print(f"Event payloads verified: {coverage['coverage']['event_payloads_verified']['count']}/{len(rows)} ({coverage['coverage']['event_payloads_verified']['percent']}%)")
print('Signature states:')
for k,v in sorted(Counter(r.get('signature_state','missing') for r in rows).items()): print(f'- {k}: {v}')
print('Source trust:')
for k,v in sorted(Counter(r.get('source_trust','unknown') for r in rows).items()): print(f'- {k}: {v}')
print('Local validation:')
for k,v in sorted(Counter(r.get('validation','draft') for r in rows).items()): print(f'- {k}: {v}')
