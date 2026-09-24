#!/usr/bin/env python3
"""Record one manually reviewed official Epic API evidence record.

V25 never treats a field as verified unless the reviewer explicitly supplies the
corresponding value (including an explicit empty list for zero parameters/effects).
"""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.epic_http import validate_epic_url

ap=argparse.ArgumentParser()
ap.add_argument('symbol')
ap.add_argument('--source-url',required=True)
ap.add_argument('--reviewed-by',default='manual-review')
ap.add_argument('--api-version',default='42.20')
ap.add_argument('--notes')
ap.add_argument('--fields',default='signature',help='Comma-separated fields actually reviewed.')
ap.add_argument('--signature')
ap.add_argument('--parameters-json',help='JSON array. Use [] when reviewed and there are no parameters.')
ap.add_argument('--return-type')
ap.add_argument('--effects-json',help='JSON array. Use [] when reviewed and there are no effects.')
ap.add_argument('--events-json',help='JSON array for reviewed event names/payloads.')
ap.add_argument('--member-names-json',help='JSON array for reviewed member names.')
a=ap.parse_args()
source_url=validate_epic_url(a.source_url)
known={json.loads(x)['symbol_id'] for x in (ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()}
if a.symbol not in known: raise SystemExit('Unknown local symbol. Discover it as an unverified candidate first; do not create it from memory.')
allowed={'presence','module','kind','signature','parameters','return_type','effects','event_names','event_payloads','member_names'}
fields=[x.strip() for x in a.fields.split(',') if x.strip()]
bad=[x for x in fields if x not in allowed]
if bad: raise SystemExit('Unknown reviewed field(s): '+', '.join(bad))

def parse_list(raw,label):
    if raw is None: return None
    try: value=json.loads(raw)
    except Exception as e: raise SystemExit(f'{label} must be valid JSON: {e}')
    if not isinstance(value,list): raise SystemExit(f'{label} must be a JSON array')
    return value
params=parse_list(a.parameters_json,'--parameters-json')
effects=parse_list(a.effects_json,'--effects-json')
events=parse_list(a.events_json,'--events-json')
members=parse_list(a.member_names_json,'--member-names-json')
requirements={
 'signature':a.signature,
 'parameters':params,
 'return_type':a.return_type,
 'effects':effects,
 'event_names':events,
 'event_payloads':events,
 'member_names':members,
}
for field in fields:
    if field in requirements and requirements[field] is None:
        raise SystemExit(f'{field} was declared reviewed but its explicit value was not supplied')
now=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
canonical_payload=json.dumps({'symbol':a.symbol,'api_version':a.api_version,'source_url':source_url,'fields':sorted(fields),'signature':a.signature,'parameters':params,'return_type':a.return_type,'effects':effects,'events':events,'members':members},sort_keys=True,ensure_ascii=False)
eid='api-'+hashlib.sha1(canonical_payload.encode()).hexdigest()[:16]
record={'evidence_id':eid,'symbol_id':a.symbol,'api_version':a.api_version,'source_url':source_url,'reviewed_at':now,'reviewed_by':a.reviewed_by,'review_status':'verified','fields_verified':fields,'signature':a.signature,'parameters':params,'return_type':a.return_type,'effects':effects,'events':events,'member_names':members,'notes':a.notes,'source_sha256':None}
path=ROOT/'knowledge/api/verification_records.jsonl'; rows=[]
if path.exists():
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.strip():
            row=json.loads(line)
            if row.get('symbol_id')!=a.symbol: rows.append(row)
rows.append(record); rows.sort(key=lambda x:x['symbol_id'].casefold())
path.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in rows),encoding='utf-8')
print('Recorded reviewed evidence:',eid)
raise SystemExit(subprocess.run([sys.executable,str(ROOT/'tools/migrate_api_catalog_v25.py')],cwd=ROOT).returncode)
