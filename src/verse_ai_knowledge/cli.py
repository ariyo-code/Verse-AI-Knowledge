from __future__ import annotations
import argparse,json,subprocess,sys
from pathlib import Path
from .api_index import lookup
from .claims import resolve_claim
from .knowledge_base import KnowledgeBase
from .policy import repo_root

def run_script(root:Path,rel:str,args:list[str])->int:
    return subprocess.run([sys.executable,str(root/rel),*args],cwd=root).returncode

def emit(data,as_json=False):
    if as_json: print(json.dumps(data,indent=2,ensure_ascii=False))
    elif isinstance(data,dict):
        for k,v in data.items(): print(f'{k}: {v}')
    else: print(data)

def cmd_api(root:Path,symbol:str,as_json=False)->int:
    row,suggestions=lookup(symbol,root)
    if row:
        if as_json: print(json.dumps(row,indent=2,ensure_ascii=False))
        else:
            print(json.dumps(row,indent=2,ensure_ascii=False))
            if row.get('signature') and not row.get('exact_signature_claim_allowed'): print('\nTODO(API VERIFY): exact signature evidence is insufficient.')
        return 0
    data={'symbol':symbol,'decision':'TODO(API VERIFY)','closest_known_symbols':suggestions}
    emit(data,as_json); return 2

def cmd_claim(root,symbol,field,as_json=False)->int:
    r=resolve_claim(symbol,field,root=root)
    if as_json: print(json.dumps(r,indent=2,ensure_ascii=False))
    else:
        print(f"{r['symbol']} :: {r['field']} -> {r['decision']}"); print(r['reason'])
        if r.get('evidence_ids'): print('Evidence:',', '.join(r['evidence_ids']))
        if r.get('suggestions'): print('Closest known symbols:',', '.join(r['suggestions']))
    return 0 if r['supported'] else 2

def git_revision(root):
    try: return subprocess.check_output(['git','rev-parse','--short','HEAD'],cwd=root,text=True,stderr=subprocess.DEVNULL).strip()
    except Exception: return 'unknown'

def version_data(root):
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
    idx=root/'knowledge/api/evidence_graph.json'; rev=hashlib_file(idx)[:12] if idx.exists() else 'unknown'
    return {'knowledge_release':m.get('release',{}).get('version'),'schema':m.get('schema_version'),'verse_api_snapshot':m.get('verse_api_version'),'git_revision':git_revision(root),'generated_data_revision':rev}

def hashlib_file(path):
    import hashlib; return hashlib.sha256(path.read_bytes()).hexdigest()

def cmd_doctor(root,as_json=False):
    m=json.loads((root/'manifest.json').read_text(encoding='utf-8')); marker=json.loads((root/'portable/generated_code_marker.json').read_text(encoding='utf-8'))
    checks={'schema_25':m.get('schema_version')==25,'release_25':m.get('release',{}).get('version')=='25.0.0','bootstrap':(root/'AI_BOOTSTRAP.md').exists(),'prompt_sources':(root/'prompt_sources/core.yaml').exists(),'portable_current':(root/'portable/current/VERSE_AI_MASTER_PROMPT.txt').exists(),'symbol_index':(root/'knowledge/api/symbols.jsonl').exists(),'evidence_graph':(root/'knowledge/api/evidence_graph.json').exists(),'provenance_v25':marker.get('marker_version')=='v25','sdk':(root/'src/verse_ai_knowledge/knowledge_base.py').exists(),'mcp':(root/'mcp/server.py').exists(),'ci':(root/'.github/workflows/ci.yml').exists()}
    data={'release':m.get('release',{}).get('version'),'checks':checks,'uefn_compile':'NOT TESTED by doctor'}
    if as_json: print(json.dumps(data,indent=2,ensure_ascii=False))
    else:
        print('Verse AI Knowledge doctor'); print('Repository:',root); print('Release:',data['release']); [print(f"[{'PASS' if ok else 'FAIL'}] {name}") for name,ok in checks.items()]; print('UEFN compile status: NOT TESTED by doctor')
    return 0 if all(checks.values()) else 1

def explain(root,symbol,as_json=False):
    kb=KnowledgeBase(root); row=kb.lookup_api(symbol)
    if not row:
        data={'symbol':symbol,'presence':'UNKNOWN','decision':'TODO(API VERIFY)'}; emit(data,as_json); return 2
    fields=['presence','module','signature','parameters','return_type','effects','event_names','event_payloads','member_names']
    claims={f:kb.resolve_claim(symbol,f)['decision'] for f in fields}
    data={'symbol':row.get('symbol_id'),'claims':claims,'source_trust':row.get('source_trust'),'local_validation':row.get('validation'),'runtime_behavior':'NOT TESTED unless matching evidence exists','source_url':row.get('source_url')}
    emit(data,as_json); return 0

def parser():
    p=argparse.ArgumentParser(prog='verse-ai',description='Verse AI Knowledge V25 CLI'); sub=p.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('search'); q.add_argument('query'); q.add_argument('--limit',type=int,default=12); q.add_argument('--json',action='store_true')
    c=sub.add_parser('context'); c.add_argument('query'); c.add_argument('--budget',type=int,default=18000); c.add_argument('--output',default='rag/generated/CONTEXT.md')
    a=sub.add_parser('api'); a.add_argument('symbol'); a.add_argument('--api-version'); a.add_argument('--json',action='store_true')
    cl=sub.add_parser('claim'); cl.add_argument('symbol'); cl.add_argument('--field',default='presence',choices=['presence','module','kind','signature','parameters','return_type','effects','event_names','event_payloads','member_names']); cl.add_argument('--json',action='store_true')
    ex=sub.add_parser('explain'); ex.add_argument('symbol'); ex.add_argument('--json',action='store_true')
    ev=sub.add_parser('evidence'); ev.add_argument('symbol'); ev.add_argument('--json',action='store_true')
    cov=sub.add_parser('coverage'); cov.add_argument('--json',action='store_true')
    aq=sub.add_parser('api-queue'); aq.add_argument('--limit',type=int,default=30); aq.add_argument('--json',action='store_true')
    lint=sub.add_parser('lint'); lint.add_argument('file'); lint.add_argument('--json',action='store_true'); lint.add_argument('--strict',action='store_true')
    err=sub.add_parser('errors'); err.add_argument('query'); err.add_argument('--limit',type=int,default=10); err.add_argument('--json',action='store_true')
    ver=sub.add_parser('version'); ver.add_argument('--json',action='store_true')
    st=sub.add_parser('status'); st.add_argument('--json',action='store_true')
    snap=sub.add_parser('snapshot'); snap.add_argument('--output'); snap.add_argument('--json',action='store_true')
    diff=sub.add_parser('api-diff'); diff.add_argument('old'); diff.add_argument('new'); diff.add_argument('--json',action='store_true')
    project=sub.add_parser('project'); ps=project.add_subparsers(dest='project_cmd',required=True); sc=ps.add_parser('scan'); sc.add_argument('project_root'); sc.add_argument('--output',default='project_scan.json')
    v=sub.add_parser('verify'); v.add_argument('path')
    lab=sub.add_parser('lab'); ls=lab.add_subparsers(dest='lab_cmd',required=True); ls.add_parser('next'); ls.add_parser('status')
    maint=sub.add_parser('maintenance'); ms=maint.add_subparsers(dest='maintenance_cmd',required=True); ms.add_parser('check')
    prov=sub.add_parser('provenance'); prs=prov.add_subparsers(dest='provenance_cmd',required=True); s=prs.add_parser('stamp'); s.add_argument('file'); s.add_argument('--status',default='draft'); r=prs.add_parser('read'); r.add_argument('file'); ck=prs.add_parser('check'); ck.add_argument('file')
    llm=sub.add_parser('llm-eval'); llm.add_argument('--responses'); llm.add_argument('--output')
    d=sub.add_parser('doctor'); d.add_argument('--json',action='store_true'); sub.add_parser('validate')
    return p
build_parser=parser

def main(argv=None):
    args=parser().parse_args(argv); root=repo_root(); kb=KnowledgeBase(root)
    if args.cmd=='search':
        x=[args.query,'--limit',str(args.limit)]+(['--json'] if args.json else []); return run_script(root,'tools/rag_query.py',x)
    if args.cmd=='context': return run_script(root,'tools/rag_context_pack.py',[args.query,'--budget',str(args.budget),'--output',args.output])
    if args.cmd=='api': return cmd_api(root,args.symbol,args.json)
    if args.cmd=='claim': return cmd_claim(root,args.symbol,args.field,args.json)
    if args.cmd=='explain': return explain(root,args.symbol,args.json)
    if args.cmd=='evidence':
        data=kb.get_evidence(args.symbol)
        if data is None: emit({'symbol':args.symbol,'decision':'TODO(API VERIFY)'},args.json); return 2
        emit(data,args.json); return 0
    if args.cmd=='coverage':
        data=kb.get_coverage(); emit(data,args.json); return 0
    if args.cmd=='api-queue':
        p=root/'knowledge/api/verification_queue.json'; data=json.loads(p.read_text(encoding='utf-8')); entries=(data.get('entries') or data.get('queue') or [])[:args.limit]; emit({'entries':entries,'count':len(entries)},args.json); return 0
    if args.cmd=='lint': return run_script(root,'tools/lint_verse_claims.py',[args.file]+(['--json'] if args.json else [])+(['--strict'] if args.strict else []))
    if args.cmd=='errors': return run_script(root,'tools/search_errors.py',[args.query,'--limit',str(args.limit)]+(['--json'] if args.json else []))
    if args.cmd=='version': emit(version_data(root),args.json); return 0
    if args.cmd=='status': emit({'version':version_data(root),'coverage':kb.get_coverage(),'uefn_compile':'NOT TESTED','runtime':'NOT TESTED','multiplayer':'NOT TESTED','llm_benchmark':'SKIPPED unless configured'},args.json); return 0
    if args.cmd=='snapshot': return run_script(root,'tools/api_coverage_snapshot.py',(['--output',args.output] if args.output else []))
    if args.cmd=='api-diff': return run_script(root,'tools/api_version_diff.py',[args.old,args.new]+(['--json'] if args.json else []))
    if args.cmd=='project' and args.project_cmd=='scan': return run_script(root,'tools/scan_verse_project.py',[args.project_root,'--output',args.output])
    if args.cmd=='verify': return run_script(root,'tools/check_api_references.py',[args.path])
    if args.cmd=='lab' and args.lab_cmd=='next': return run_script(root,'tools/compile_queue.py',['next'])
    if args.cmd=='lab' and args.lab_cmd=='status': return run_script(root,'tools/verselab_status.py',[])
    if args.cmd=='maintenance' and args.maintenance_cmd=='check': return run_script(root,'tools/revalidation_report.py',[])
    if args.cmd=='provenance' and args.provenance_cmd=='stamp': return run_script(root,'tools/stamp_generated_code.py',[args.file,'--status',args.status])
    if args.cmd=='provenance' and args.provenance_cmd=='read': return run_script(root,'tools/read_generated_marker.py',[args.file])
    if args.cmd=='provenance' and args.provenance_cmd=='check': return run_script(root,'tools/check_generated_marker.py',[args.file])
    if args.cmd=='llm-eval':
        x=[]
        if args.responses:x+=['--responses',args.responses]
        if args.output:x+=['--output',args.output]
        return run_script(root,'evals/llm/runner.py',x)
    if args.cmd=='doctor': return cmd_doctor(root,args.json)
    if args.cmd=='validate': return run_script(root,'tools/validate_all.py',[])
    return 2
if __name__=='__main__': raise SystemExit(main())
