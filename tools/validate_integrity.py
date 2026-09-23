#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; errors=[]
q=json.loads((ROOT/'lab/compile_queue.json').read_text(encoding='utf-8'))
for e in q.get('entries',[]):
    validation=e.get('validation','draft'); v=e.get('local_verification',{})
    if validation in {'compiled','verified','multiplayer-verified'} and not v.get('compiled'): errors.append(f"{e.get('candidate_id')}: {validation} but compiled=false")
    if validation in {'verified','multiplayer-verified'} and not v.get('runtime_tested'): errors.append(f"{e.get('candidate_id')}: {validation} but runtime_tested=false")
    if validation=='multiplayer-verified' and not v.get('multiplayer_tested'): errors.append(f"{e.get('candidate_id')}: multiplayer-verified but multiplayer_tested=false")
compiled=ROOT/'examples/compiled'
if compiled.exists():
    for p in compiled.rglob('metadata.json'):
        m=json.loads(p.read_text(encoding='utf-8')); validation=m.get('validation') or m.get('status'); checks=m.get('local_verification',{})
        if validation in {'compiled','verified','multiplayer-verified'} and not checks.get('compiled',m.get('tested_in_uefn',False)): errors.append(f"{p.relative_to(ROOT)}: {validation} without compile evidence")
if errors:
    print('Integrity validation FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('Integrity validation OK')
