#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.policy import SOURCE_TRUST,VALIDATION,exact_signature_allowed
from verse_ai_knowledge.api_index import load_symbols

m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
assert m['schema_version']==22
assert tuple(m['trust_model']['source_trust'])==SOURCE_TRUST
assert tuple(m['trust_model']['validation'])==VALIDATION
assert tuple(m['verification_statuses'])==VALIDATION
trust=json.loads((ROOT/'schemas/trust.schema.json').read_text(encoding='utf-8'))
validation=json.loads((ROOT/'schemas/validation_status.schema.json').read_text(encoding='utf-8'))
assert tuple(trust['enum'])==SOURCE_TRUST
assert tuple(validation['enum'])==VALIDATION
rows=load_symbols(ROOT)
assert rows
for row in rows:
    assert row['source_trust'] in SOURCE_TRUST
    assert row['validation'] in VALIDATION
    if row['exact_signature_claim_allowed']:
        assert exact_signature_allowed(row)
        assert row['signature']
# Critical regression: current V21 catalog stored GetFortCharacter signature without classified signature evidence.
by_id={x['symbol_id']:x for x in rows}
if 'GetFortCharacter' in by_id and by_id['GetFortCharacter'].get('evidence_basis') is None:
    assert by_id['GetFortCharacter']['exact_signature_claim_allowed'] is False
print('V22 integrity unit tests OK')
