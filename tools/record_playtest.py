#!/usr/bin/env python3
import argparse
from datetime import datetime,timezone
from lab_state import load_queue,save_queue,get_entry,transition
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('candidate_id'); ap.add_argument('--runtime',action='store_true'); ap.add_argument('--multiplayer',action='store_true'); ap.add_argument('--evidence',required=True); a=ap.parse_args(); a.runtime = a.runtime or a.multiplayer
    q=load_queue(); e=get_entry(q,a.candidate_id); local=e.setdefault('local_verification',{'compiled':False,'runtime_tested':False,'multiplayer_tested':False})
    if not local.get('compiled'): raise SystemExit('Playtest promotion blocked: candidate has not compiled locally.')
    e.setdefault('playtests',[]).append({'timestamp':now(),'runtime':a.runtime,'multiplayer':a.multiplayer,'evidence':a.evidence})
    if a.runtime: local['runtime_tested']=True
    if a.multiplayer: local['multiplayer_tested']=True
    status=e['queue_status']
    if a.runtime and status in {'compiled','runtime-pending'}: transition(e,'verified'); status='verified'; e['validation']='verified'
    if a.multiplayer and status=='verified': transition(e,'multiplayer-verified'); e['validation']='multiplayer-verified'
    save_queue(q); print(f"{e['candidate_id']} -> {e['queue_status']} ({e.get('validation','draft')})")
if __name__=='__main__': main()
