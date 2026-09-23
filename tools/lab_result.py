#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone
from lab_state import ROOT,load_queue,save_queue,get_entry,transition,current,clear_current
RESULTS=ROOT/'lab/results'
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True); success=sub.add_parser('success'); success.add_argument('--evidence',required=True); success.add_argument('--uefn-version',default='42.20'); fail=sub.add_parser('fail'); fail.add_argument('--classification',required=True,choices=['syntax-or-language','api-or-version','unknown']); fail.add_argument('--error',action='append',required=True); fail.add_argument('--uefn-version',default='42.20'); fail.add_argument('--note'); blocked=sub.add_parser('blocked'); blocked.add_argument('--classification',required=True,choices=['missing-dependency','project-environment']); blocked.add_argument('--error',action='append',required=True); blocked.add_argument('--uefn-version',default='42.20'); blocked.add_argument('--note'); a=ap.parse_args()
    cur=current()
    if not cur: raise SystemExit('No active VerseLab candidate.')
    q=load_queue(); e=get_entry(q,cur['candidate_id']); local=e.setdefault('local_verification',{'compiled':False,'runtime_tested':False,'multiplayer_tested':False})
    if e['queue_status']=='staged': transition(e,'compiling')
    attempt={'attempt':len(e.get('compile_attempts',[]))+1,'timestamp':now(),'uefn_version':a.uefn_version,'original_untouched':bool(cur.get('original_untouched')),'success':a.cmd=='success','blocked_environment':a.cmd=='blocked'}
    if a.cmd=='success': attempt['evidence']=a.evidence; attempt['exact_errors']=[]; attempt['classification']=None; transition(e,'compiled'); local['compiled']=True; e['validation']='compiled'; e['failure_classification']=None
    else:
        attempt['exact_errors']=a.error; attempt['classification']=a.classification; attempt['note']=getattr(a,'note',None); e['failure_classification']=a.classification; transition(e,'blocked-environment' if a.cmd=='blocked' else 'compile-failed'); e.setdefault('validation','draft')
    e.setdefault('compile_attempts',[]).append(attempt); save_queue(q); RESULTS.mkdir(parents=True,exist_ok=True); (RESULTS/f"{e['candidate_id']}.json").write_text(json.dumps({'candidate_id':e['candidate_id'],'source_path':e['source_path'],'status':e['queue_status'],'validation':e.get('validation','draft'),'source_trust':e.get('upstream_source_trust','unknown'),'verification':local,'attempts':e['compile_attempts']},indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); clear_current(); print(f"{e['candidate_id']} -> {e['queue_status']}")
if __name__=='__main__': main()
