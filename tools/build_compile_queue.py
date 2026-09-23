#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def now(): return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--limit',type=int,default=50); ap.add_argument('--replace',action='store_true'); a=ap.parse_args()
    src=ROOT/'curation/curated_examples.json'
    if not src.exists(): raise SystemExit('Run tools/curate_external_examples.py first.')
    data=json.loads(src.read_text(encoding='utf-8')); dest=ROOT/'lab/compile_queue.json'; existing={}
    if dest.exists() and not a.replace:
        old=json.loads(dest.read_text(encoding='utf-8')); existing={x['candidate_id']:x for x in old.get('entries',[])}
    entries=[]
    for row in data.get('examples',[])[:a.limit]:
        cid=row['id']
        if cid in existing:
            e=existing[cid]; e['upstream_source_trust']=row.get('source_trust',row.get('status','unknown')); e.setdefault('validation','draft'); entries.append(e); continue
        entries.append({'candidate_id':cid,'source_id':row['source_id'],'source_revision':data['source_revision'],'source_path':row['path'],'curation_score':row['score'],'category':row['category'],'devices':row['devices'],'api_symbols':row['api_symbols'],'features':row['features'],'project_relevance':row.get('project_relevance',[]),'upstream_source_trust':row.get('source_trust','unknown'),'queue_status':'pending','validation':'draft','failure_classification':None,'local_verification':{'compiled':False,'runtime_tested':False,'multiplayer_tested':False},'compile_attempts':[],'notes':None})
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps({'schema_version':2,'generated_at':now(),'source_id':data['source_id'],'source_revision':data['source_revision'],'entries':entries},indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(f'Compile queue: {len(entries)} candidate(s)')
if __name__=='__main__': main()
