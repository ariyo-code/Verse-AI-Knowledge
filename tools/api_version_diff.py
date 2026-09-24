#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ap=argparse.ArgumentParser(); ap.add_argument('old'); ap.add_argument('new'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
def load(path):
 p=Path(path); data=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(data,dict) and 'symbols' in data: return data['symbols']
 if isinstance(data,list): return data
 raise SystemExit('Expected JSON list or {symbols:[...]}')
def byid(rows): return {str(r.get('symbol_id') or r.get('qualified_name') or r.get('name')):r for r in rows}
o,n=byid(load(a.old)),byid(load(a.new)); changes={'added':sorted(set(n)-set(o)),'removed':sorted(set(o)-set(n)),'changed':[]}
for sid in sorted(set(o)&set(n)):
 d={}
 for f in ['module','signature','parameters','return_type','effects','event_payloads','deprecated_in']:
  if o[sid].get(f)!=n[sid].get(f): d[f]={'old':o[sid].get(f),'new':n[sid].get(f)}
 if d: changes['changed'].append({'symbol_id':sid,'fields':d})
if a.json: print(json.dumps(changes,indent=2,ensure_ascii=False))
else:
 print(f"added: {len(changes['added'])}\nremoved: {len(changes['removed'])}\nchanged: {len(changes['changed'])}")
 for x in changes['changed'][:50]: print('-',x['symbol_id'],', '.join(x['fields']))
