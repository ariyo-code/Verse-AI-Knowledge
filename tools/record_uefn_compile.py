#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]; QUEUE=ROOT/'lab/compile_queue.json'; RESULTS=ROOT/'lab/results'
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('candidate_id'); g=ap.add_mutually_exclusive_group(required=True); g.add_argument('--success',action='store_true'); g.add_argument('--failure',action='store_true'); g.add_argument('--blocked',action='store_true'); ap.add_argument('--uefn-version',default='42.20'); ap.add_argument('--error',action='append',default=[]); ap.add_argument('--classification',choices=['syntax-or-language','api-or-version','missing-dependency','project-environment','unknown']); ap.add_argument('--evidence'); ap.add_argument('--note'); a=ap.parse_args()
    q=json.loads(QUEUE.read_text(encoding='utf-8')); e=next((x for x in q['entries'] if x['candidate_id']==a.candidate_id),None)
    if not e: raise SystemExit('Candidate not found.')
    if a.success and not a.evidence: raise SystemExit('Successful compile recording requires --evidence.')
    attempt={'attempt':len(e.get('compile_attempts',[]))+1,'timestamp':now(),'uefn_version':a.uefn_version,'success':bool(a.success),'blocked_environment':bool(a.blocked),'classification':a.classification,'exact_errors':a.error,'evidence':a.evidence,'note':a.note}
    e.setdefault('compile_attempts',[]).append(attempt); local=e.setdefault('local_verification',{'compiled':False,'runtime_tested':False,'multiplayer_tested':False})
    if a.success: e['queue_status']='compiled'; e['validation']='compiled'; e['failure_classification']=None; local['compiled']=True
    elif a.blocked: e['queue_status']='blocked-environment'; e['failure_classification']=a.classification or 'project-environment'; e.setdefault('validation','draft')
    else: e['queue_status']='compile-failed'; e['failure_classification']=a.classification or 'unknown'; e.setdefault('validation','draft')
    QUEUE.write_text(json.dumps(q,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); RESULTS.mkdir(parents=True,exist_ok=True); result=RESULTS/f"{a.candidate_id}.json"; result.write_text(json.dumps({'candidate_id':a.candidate_id,'source_id':e['source_id'],'source_path':e['source_path'],'queue_status':e['queue_status'],'validation':e.get('validation','draft'),'local_verification':local,'attempts':e['compile_attempts']},indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(f"{a.candidate_id} -> {e['queue_status']}"); print(result)
if __name__=='__main__': main()
