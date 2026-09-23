#!/usr/bin/env python3
from pathlib import Path
import json,argparse
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--limit',type=int,default=30); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
d=json.loads((ROOT/'knowledge/api/verification_queue.json').read_text(encoding='utf-8')); items=d.get('items',[])[:a.limit]
if a.json: print(json.dumps({'pending_count':d.get('pending_count'), 'items':items},indent=2,ensure_ascii=False))
else:
 print(f"Pending exact API verification: {d.get('pending_count',0)}")
 for i,x in enumerate(items,1): print(f"{i:>3}. [{x['priority_score']}] {x['symbol_id']} ({x['kind']}) -> {x.get('source_url') or 'NO SOURCE'}")
