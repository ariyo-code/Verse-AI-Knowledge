#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import json,re,sys
from collections import Counter
from typing import Any

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.policy import canonical_source_trust

EFFECT_RE=re.compile(r'<([A-Za-z_][A-Za-z0-9_]*)>')
NON_EFFECT_SPECIFIERS={'public','private','protected','internal','native','native_callable','epic_internal'}

def load(path): return json.loads(path.read_text(encoding='utf-8'))
def dump(path,obj): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def evidence_basis(e): return e.get('verification') or e.get('evidence_basis')

def trust_for(e):
    oldv=str(e.get('verification') or '').lower(); olds=str(e.get('status') or '').lower()
    if oldv in {'signature-verified','api-page-verified'}: return oldv
    if olds in {'official-current','official-stale','community-verified','community-unverified','external-compiler-claimed','reference-only','deprecated','unknown'}: return olds
    if olds=='external-community': return 'community-unverified'
    src=str(e.get('source') or e.get('source_url') or '')
    if src.startswith('https://dev.epicgames.com/'): return 'official-current'
    return canonical_source_trust(oldv or olds)

def split_top_level(text,sep=','):
    out=[]; buf=[]; depth=0
    pairs={'(':')','[':']','{':'}','<':'>'}
    opens=set(pairs); closes=set(pairs.values())
    for ch in text:
        if ch in opens: depth+=1
        elif ch in closes: depth=max(0,depth-1)
        if ch==sep and depth==0:
            out.append(''.join(buf).strip()); buf=[]
        else: buf.append(ch)
    if buf: out.append(''.join(buf).strip())
    return [x for x in out if x]

def parse_signature(sig):
    if not sig: return [],None,[]
    effects=sorted(set(x for x in EFFECT_RE.findall(sig) if x not in NON_EFFECT_SPECIFIERS))
    # Collect parameter-bearing parenthesized groups. This preserves extension receivers
    # such as (InAgent:agent) as structured parameters while ignoring empty call groups.
    matches=list(re.finditer(r'\(([^()]*)\)',sig))
    params=[]
    for match in matches:
        raw=match.group(1).strip()
        if not raw or ':' not in raw:
            continue
        for token in split_top_level(raw):
            if ':' not in token: continue
            name,typ=token.split(':',1); default=None
            if ':=' in typ:
                typ,default=typ.split(':=',1)
            params.append({'name':name.strip(),'type':typ.strip(),'default':default.strip() if default else None,'optional':False})
    ret=None
    tail=sig[matches[-1].end():] if matches else sig
    # remove effects/specifiers before final :ReturnType
    if ':' in tail:
        candidate=tail.rsplit(':',1)[1].strip()
        if candidate: ret=candidate
    return params,ret,effects

def reviewed_records(root):
    path=root/'knowledge/api/verification_records.jsonl'; out={}
    if not path.exists(): return out
    for n,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
        if not line.strip(): continue
        row=json.loads(line)
        if row.get('review_status')=='verified': out[row['symbol_id']]=row
    return out

def base_symbol(name,e,api_version,last_verified):
    trust=trust_for(e); basis=evidence_basis(e); sig=e.get('signature')
    sig_verified=bool(sig and basis in {'signature-verified','api-page-verified'})
    state='verified' if sig_verified else ('candidate' if sig else 'missing')
    effects=list(dict.fromkeys(e.get('effects') or []))
    if sig_verified:
        _,_,parsed=parse_signature(sig); effects=sorted(set(effects+parsed))
    params,ret,_=parse_signature(sig) if sig_verified else ([],None,[])
    return {
      'symbol_id':name,'name':name.split('.')[-1] if '.' in name else name,'qualified_name':name,
      'kind':e.get('kind') or 'unknown','module':e.get('module') or 'unknown','signature':sig if sig is not None else None,
      'signature_state':state,'parameters':params,'return_type':ret,'effects':sorted(set(map(str,effects))),
      'failure_context_required':'decides' in effects,'api_version':api_version,
      'introduced_in':e.get('introduced_in'),'deprecated_in':e.get('deprecated_in'),'replacement':e.get('replacement'),
      'source_trust':trust,'validation':'static-checked','source_url':e.get('source') or e.get('source_url'),
      'verified_at':e.get('last_verified') or last_verified,'evidence_basis':basis,
      'claim_scope':'exact-signature' if sig_verified else ('legacy-signature-unverified' if sig else 'presence-only'),
      'signature_verified':sig_verified,'exact_signature_claim_allowed':sig_verified,'summary':e.get('summary'),
      'cautions':list(e.get('cautions') or []),'member_names':sorted(set(e.get('key_members') or [])),
      'event_names':sorted(set(e.get('key_events') or [])),'event_details':[],'evidence_ids':[],
      'coverage':{'presence':True,'signature':sig_verified,'parameters':sig_verified,'return_type':sig_verified and ret is not None,
                  'effects':sig_verified,'event_names':bool(e.get('key_events') or []),'event_payloads':False}
    }

def apply_review(row,ev):
    sig=ev.get('signature'); params=ev.get('parameters') or []; ret=ev.get('return_type'); effects=ev.get('effects') or []
    if sig and not params and ret is None:
        params,ret,parsed=parse_signature(sig); effects=sorted(set(effects+parsed))
    row.update({
      'signature':sig,'signature_state':'verified' if sig else row.get('signature_state','missing'),
      'parameters':params,'return_type':ret,'effects':sorted(set(effects)),
      'failure_context_required':'decides' in effects,'source_trust':'signature-verified' if sig else 'api-page-verified',
      'source_url':ev.get('source_url'),'verified_at':ev.get('reviewed_at'),'evidence_basis':'reviewed-official-evidence',
      'claim_scope':'exact-signature' if sig else 'presence-only','signature_verified':bool(sig),
      'exact_signature_claim_allowed':bool(sig),'event_details':ev.get('events') or [],
      'evidence_ids':sorted(set(row.get('evidence_ids',[])+[ev['evidence_id']]))
    })
    row['coverage']={'presence':True,'signature':bool(sig),'parameters':bool(sig),'return_type':bool(sig) and ret is not None,
                     'effects':bool(sig),'event_names':bool(row.get('event_names') or []),'event_payloads':bool(row.get('event_details'))}
    return row

def build_generated(root=ROOT):
    catalog=load(root/'knowledge/api_catalog.json'); modules_legacy=load(root/'knowledge/module_catalog.json')
    api=str(catalog.get('verse_api_version') or modules_legacy.get('snapshot') or 'unknown'); last=catalog.get('last_verified') or modules_legacy.get('last_verified')
    reviews=reviewed_records(root); rows=[]
    for name,e in sorted(catalog.get('entries',{}).items(),key=lambda x:x[0].casefold()):
        row=base_symbol(name,e,api,last)
        if name in reviews: row=apply_review(row,reviews[name])
        rows.append(row)
    modules={'schema_version':2,'api_version':api,'source_url':modules_legacy.get('source'),'verified_at':modules_legacy.get('last_verified'),
             'source_trust':'official-current' if str(modules_legacy.get('source','')).startswith('https://dev.epicgames.com/') else 'unknown',
             'validation':'static-checked','top_level':modules_legacy.get('top_level',{})}
    versions={'schema_version':2,'current':api,'known':[{'version':api,'verified_at':last,'source_url':modules_legacy.get('source'),'source_trust':modules['source_trust']}],
              'note':'V23 records only version facts supported by stored evidence; unknown history remains null.'}
    return rows,modules,versions

def render(rows): return ''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows)
def coverage(rows,api):
    total=len(rows)
    def c(fn): return sum(1 for r in rows if fn(r))
    by_kind=Counter(r.get('kind','unknown') for r in rows)
    return {'schema_version':1,'generated_by':'tools/migrate_api_catalog_v23.py','api_version':api,'symbol_count':total,
      'coverage':{
        'presence':{'count':c(lambda r:r['coverage']['presence']),'percent':round(100*c(lambda r:r['coverage']['presence'])/max(total,1),2)},
        'signature_verified':{'count':c(lambda r:r['coverage']['signature']),'percent':round(100*c(lambda r:r['coverage']['signature'])/max(total,1),2)},
        'parameters_structured':{'count':c(lambda r:r['coverage']['parameters']),'percent':round(100*c(lambda r:r['coverage']['parameters'])/max(total,1),2)},
        'return_type_structured':{'count':c(lambda r:r['coverage']['return_type']),'percent':round(100*c(lambda r:r['coverage']['return_type'])/max(total,1),2)},
        'effects_structured':{'count':c(lambda r:r['coverage']['effects']),'percent':round(100*c(lambda r:r['coverage']['effects'])/max(total,1),2)},
        'event_names_known':{'count':c(lambda r:r['coverage']['event_names']),'percent':round(100*c(lambda r:r['coverage']['event_names'])/max(total,1),2)},
        'event_payloads_verified':{'count':c(lambda r:r['coverage']['event_payloads']),'percent':round(100*c(lambda r:r['coverage']['event_payloads'])/max(total,1),2)}},
      'signature_states':dict(Counter(r.get('signature_state','missing') for r in rows)),'by_kind':dict(sorted(by_kind.items()))}

def queue(rows):
    base_priority={'function':140,'extension':140,'class':120,'interface':115,'struct':100,'enum':90}
    pending=[]
    for r in rows:
      if r.get('exact_signature_claim_allowed'): continue
      score=base_priority.get(r.get('kind'),80)
      if r.get('source_trust')=='api-page-verified': score+=8
      if r.get('member_names'): score+=3
      if r.get('event_names'): score+=3
      pending.append({'symbol_id':r['symbol_id'],'kind':r['kind'],'module':r['module'],'source_url':r.get('source_url'),
                      'signature_state':r.get('signature_state'),'priority_score':score,'needs':(['signature','parameters','return_type','effects'] if r.get('kind') in {'function','extension'} else ['declaration','members','events']),
                      'reason':'Exact signature evidence is not yet verified.'})
    pending.sort(key=lambda x:(-x['priority_score'],x['symbol_id'].casefold()))
    return {'schema_version':1,'generated_by':'tools/migrate_api_catalog_v23.py','pending_count':len(pending),'items':pending}

def write_generated(root=ROOT):
    rows,mods,vers=build_generated(root); api=vers['current']; d=root/'knowledge/api'; d.mkdir(parents=True,exist_ok=True)
    (d/'symbols.jsonl').write_text(render(rows),encoding='utf-8'); dump(d/'modules.json',mods); dump(d/'versions.json',vers); dump(d/'coverage.json',coverage(rows,api)); dump(d/'verification_queue.json',queue(rows))
    print(f'Generated {len(rows)} V23 structured API symbol record(s).')
if __name__=='__main__': write_generated()
