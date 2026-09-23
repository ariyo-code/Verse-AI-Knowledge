#!/usr/bin/env python3
from pathlib import Path
import argparse,json
ROOT=Path(__file__).resolve().parents[1]; QUEUE=ROOT/'lab/compile_queue.json'
def load():
    if not QUEUE.exists(): raise SystemExit('Compile queue missing. Run tools/build_compile_queue.py.')
    return json.loads(QUEUE.read_text(encoding='utf-8'))
def save(q): QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); sub.add_parser('list'); sub.add_parser('next'); show=sub.add_parser('show'); show.add_argument('candidate_id'); status=sub.add_parser('status'); status.add_argument('candidate_id'); status.add_argument('status',choices=['pending','staged','compiling','compile-failed','blocked-environment','compiled','runtime-pending','verified','multiplayer-verified','skipped']); status.add_argument('--note'); a=ap.parse_args(); q=load(); entries=q['entries']
    if a.cmd=='list':
        for x in entries: print(f"{x['candidate_id']}  {x['queue_status']:20} validation={x.get('validation','draft'):20} score={x['curation_score']:5} {x['source_path']}")
        return
    if a.cmd=='next':
        x=next((x for x in entries if x['queue_status']=='pending'),None); print(json.dumps(x,indent=2,ensure_ascii=False) if x else 'No pending candidate.'); return
    x=next((x for x in entries if x['candidate_id']==a.candidate_id),None)
    if not x: raise SystemExit('Candidate not found.')
    if a.cmd=='show': print(json.dumps(x,indent=2,ensure_ascii=False)); return
    if a.cmd=='status':
        x['queue_status']=a.status
        checks=x.setdefault('local_verification',{'compiled':False,'runtime_tested':False,'multiplayer_tested':False})
        if a.status=='compiled': checks['compiled']=True; x['validation']='compiled'
        elif a.status=='verified': checks['compiled']=True; checks['runtime_tested']=True; x['validation']='verified'
        elif a.status=='multiplayer-verified': checks['compiled']=True; checks['runtime_tested']=True; checks['multiplayer_tested']=True; x['validation']='multiplayer-verified'
        if a.note: x['notes']=a.note
        save(q); print(f"{a.candidate_id} -> {a.status}")
if __name__=='__main__': main()
