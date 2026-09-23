#!/usr/bin/env python3
from pathlib import Path
import argparse,json,shutil
ROOT=Path(__file__).resolve().parents[1]; QUEUE=ROOT/'lab/compile_queue.json'; REG=json.loads((ROOT/'external/sources.json').read_text(encoding='utf-8'))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('candidate_id'); a=ap.parse_args(); q=json.loads(QUEUE.read_text(encoding='utf-8')); e=next((x for x in q['entries'] if x['candidate_id']==a.candidate_id),None)
    if not e: raise SystemExit('Candidate not found.')
    if not e.get('local_verification',{}).get('compiled'): raise SystemExit('Promotion blocked: no local UEFN compile evidence.')
    if e.get('validation') not in {'compiled','verified','multiplayer-verified'}: raise SystemExit(f"Promotion blocked from validation: {e.get('validation')}")
    srcmeta=next((x for x in REG['approved_sources'] if x['id']==e['source_id']),None)
    if not srcmeta or not srcmeta.get('license_verified'): raise SystemExit('Promotion blocked: source license not approved.')
    src=ROOT/'external/corpus'/e['source_id']/e['source_revision']/e['source_path']
    if not src.exists(): raise SystemExit(f'Source missing: {src}')
    destdir=ROOT/'examples/compiled/external'/e['source_id']/e['candidate_id']; destdir.mkdir(parents=True,exist_ok=True); shutil.copy2(src,destdir/src.name)
    metadata={'title':src.name,'lifecycle_status':'active','validation':e['validation'],'source_trust':e.get('upstream_source_trust','unknown'),'status':e['validation'],'source_id':e['source_id'],'source_repository':srcmeta['repository'],'source_revision':e['source_revision'],'source_path':e['source_path'],'license':srcmeta['license'],'local_verification':e['local_verification'],'compile_attempts':e.get('compile_attempts',[]),'warning':'Compilation evidence does not imply runtime or multiplayer verification.'}
    (destdir/'metadata.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); lic=ROOT/'external/corpus'/e['source_id']/e['source_revision']/'LICENSE'; shutil.copy2(lic,destdir/'LICENSE') if lic.exists() else None; print(destdir)
if __name__=='__main__': main()
