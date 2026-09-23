#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--output'); a=ap.parse_args(); run=json.loads(Path(a.run).read_text(encoding='utf-8'))
rows=[json.loads(x) for x in (ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
known={r['name'] for r in rows}|{r['symbol_id'] for r in rows}; exact={r['name'] for r in rows if r.get('exact_signature_claim_allowed')}|{r['symbol_id'] for r in rows if r.get('exact_signature_claim_allowed')}
# Conservative API-looking tokens. Unknown tokens are candidates, not automatic hallucinations.
API_RE=re.compile(r'\b(?:Get[A-Z][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*_device|fort_[A-Za-z0-9_]+|player_ui)\b')
SIG_RE=re.compile(r'\b([A-Za-z_][A-Za-z0-9_.]*)\s*(?:<[^>]+>)*\s*\([^\n)]*\)\s*(?:<[^>]+>)*\s*:[A-Za-z_\[\]?][^\n`]*')
results=[]; agg={'tasks':0,'unknown_api_like_claims':0,'unsupported_exact_signature_claims':0,'todo_api_verify':0,'compile_passed':0,'compile_known':0,'compile_corrections_total':0,'compile_corrections_known':0}
for t in run.get('tasks',[]):
 out=t.get('output',''); tokens=sorted(set(API_RE.findall(out))); unknown=[x for x in tokens if x not in known]
 sig_names=[]
 for m in SIG_RE.finditer(out): sig_names.append(m.group(1).split('.')[-1])
 unsupported=[x for x in sig_names if x not in exact]
 todo=out.count('TODO(API VERIFY)'); cp=t.get('compile_passed'); cc=t.get('compile_corrections')
 r={'task_id':t.get('task_id'),'api_like_tokens':tokens,'unknown_api_like_claims':unknown,'unsupported_exact_signature_claims':unsupported,'todo_api_verify':todo,'compile_passed':cp,'compile_corrections':cc}
 results.append(r); agg['tasks']+=1; agg['unknown_api_like_claims']+=len(unknown); agg['unsupported_exact_signature_claims']+=len(unsupported); agg['todo_api_verify']+=todo
 if cp is not None: agg['compile_known']+=1; agg['compile_passed']+=int(bool(cp))
 if cc is not None: agg['compile_corrections_known']+=1; agg['compile_corrections_total']+=cc
agg['first_pass_compile_rate']=round(100*agg['compile_passed']/agg['compile_known'],2) if agg['compile_known'] else None
agg['average_compile_corrections']=round(agg['compile_corrections_total']/agg['compile_corrections_known'],3) if agg['compile_corrections_known'] else None
res={'schema_version':1,'run_id':run.get('run_id'),'knowledge_version':run.get('knowledge_version'),'model_or_agent':run.get('model_or_agent'),'metrics':agg,'tasks':results,
     'warning':'Static token checks flag review candidates; only real UEFN fields prove compile/runtime behavior.'}
out=Path(a.output) if a.output else Path(a.run).with_suffix('.result.json'); out.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(out); print(json.dumps(agg,indent=2))
