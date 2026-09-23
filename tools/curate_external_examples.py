#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, sys
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.policy import canonical_source_trust
REG=json.loads((ROOT/'external/sources.json').read_text(encoding='utf-8'))
POLICY=json.loads((ROOT/'curation/policy.json').read_text(encoding='utf-8'))
CATALOG=json.loads((ROOT/'knowledge/api_catalog.json').read_text(encoding='utf-8')).get('entries',{})
DEVICE_RE=re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*_device)\b'); USING_RE=re.compile(r'^\s*using\s*\{\s*([^}]+)\s*\}',re.M)
CREATIVE_RE=re.compile(r'\bclass\s*\(\s*creative_device\s*\)'); EDITABLE_RE=re.compile(r'@editable\b')
FEATURES={'ui':['player_ui','canvas','GetPlayerUI'],'player-lifecycle':['GetPlayers','PlayerAddedEvent','PlayerRemovedEvent'],'character':['GetFortCharacter','fort_character'],'vehicles':['vehicle_spawner_','fort_vehicle'],'persistence':['weak_map','persist'],'async':['spawn{','race:','<suspends>'],'events':['Subscribe(','.Await()'],'teams':['GetTeamCollection','fort_team_collection'],'teleport':['teleporter_device','Teleport(']}
def source_root(source_id):
    parent=ROOT/'external/corpus'/source_id
    if not parent.exists(): raise SystemExit(f'External source not synchronized: {parent}')
    src=next((x for x in REG['approved_sources'] if x['id']==source_id),None)
    if src and (parent/src['reviewed_tree_sha']).exists(): return parent/src['reviewed_tree_sha']
    dirs=sorted(p for p in parent.iterdir() if p.is_dir())
    if not dirs: raise SystemExit(f'No synchronized revision under {parent}')
    return dirs[-1]
def category_for(path):
    parts=path.parts
    try: i=parts.index('examples'); return parts[i+1] if len(parts)>i+1 else 'examples'
    except ValueError: return 'unknown'
def analyse(path,base,source_id,trust):
    text=path.read_text(encoding='utf-8',errors='ignore'); rel=str(path.relative_to(base)).replace('\\','/'); lines=text.splitlines()
    devices=sorted(set(DEVICE_RE.findall(text))); imports=sorted(set(x.strip() for x in USING_RE.findall(text)))
    api_symbols=sorted(name for name in CATALOG if name in text); features=[label for label,needles in FEATURES.items() if any(n in text for n in needles)]
    score=18 if trust=='external-compiler-claimed' else 8 if trust=='community-unverified' else 4
    score+=10 if CREATIVE_RE.search(text) else 0; score+=4 if EDITABLE_RE.search(text) else 0
    n=len(lines); score+=10 if 20<=n<=500 else 3 if n<20 else -12 if n>900 else -4 if n>500 else 0
    score+=min(len(api_symbols)*1.8,18)+min(len(devices)*1.2,12)+min(len(features)*1.5,9)
    cat=category_for(path); preferred=POLICY.get('preferred_categories',[]); score+=max(0,10-preferred.index(cat)) if cat in preferred else 0
    if 'aimbot' in path.name.lower() or 'aim-bot' in path.name.lower(): score-=20
    h=hashlib.sha256(re.sub(r'\s+','',text).encode()).hexdigest(); cid=hashlib.sha1(f'{source_id}|{rel}'.encode()).hexdigest()[:14]
    return {'id':f'ext-{cid}','source_id':source_id,'path':rel,'category':cat,'score':round(score,2),'line_count':n,'devices':devices,'api_symbols':api_symbols,'imports':imports,'features':features,'project_relevance':[],'source_trust':trust,'validation':'draft','content_hash':h}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',default=POLICY.get('target_source','uefncentral-examples')); ap.add_argument('--limit',type=int,default=POLICY.get('default_max_candidates',100)); a=ap.parse_args()
    src=next((x for x in REG['approved_sources'] if x['id']==a.source),None)
    if not src: raise SystemExit(f'Source is not approved for import: {a.source}')
    trust=canonical_source_trust(src.get('trust')); base=source_root(a.source); root=base/'examples'
    rows=[analyse(p,base,a.source,trust) for p in sorted(root.rglob('*.verse'))]
    best={}
    for r in sorted(rows,key=lambda x:(-x['score'],x['path'])): best.setdefault(r['content_hash'],r)
    unique=list(best.values()); selected={}; per_device=defaultdict(int); per_cat=defaultdict(int)
    for r in sorted(unique,key=lambda x:(-x['score'],x['path'])):
        take=per_cat[r['category']]<POLICY.get('top_per_category',10) or any(per_device[d]<POLICY.get('top_per_device',5) for d in r['devices'])
        if take or len(selected)<min(20,a.limit):
            selected[r['id']]=r; per_cat[r['category']]+=1
            for d in r['devices']: per_device[d]+=1
        if len(selected)>=a.limit: break
    chosen=sorted(selected.values(),key=lambda x:(-x['score'],x['path']))
    out={'schema_version':2,'source_id':a.source,'source_revision':src['reviewed_tree_sha'],'upstream_trust':trust,'analysed_examples':len(rows),'unique_examples':len(unique),'selected_examples':len(chosen),'selection_note':'Static ranking only. UEFN recompilation is required for local compiled status.','examples':chosen}
    (ROOT/'curation/curated_examples.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(f'Selected {len(chosen)} candidate(s).')
if __name__=='__main__': main()
