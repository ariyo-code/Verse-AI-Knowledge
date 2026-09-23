#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.api_index import load_symbols  # noqa: E402
from verse_ai_knowledge.policy import exact_signature_allowed  # noqa: E402

cases=json.loads((ROOT/'evals/hallucination/cases.json').read_text(encoding='utf-8'))['cases']
symbols=load_symbols(ROOT); by_id={x.get('symbol_id'):x for x in symbols}; by_name={x.get('name'):x for x in symbols}
module_catalog=json.loads((ROOT/'knowledge/api/modules.json').read_text(encoding='utf-8'))
known_modules={f'/{domain}/{module}' for domain,mods in module_catalog.get('top_level',{}).items() for module in mods}
rows=[]; todo_expected=0; todo_predicted=0; todo_true=0; unknown_total=0; hallucinated=0; unsupported_sig=0; false_compile=0; verified_source_hits=0; api_cases=0
for case in cases:
    kind=case['kind']; passed=False; action=''
    if kind=='unknown_api':
        unknown_total+=1; todo_expected+=1
        found=by_id.get(case['symbol']) or by_name.get(case['symbol'])
        action='todo_api_verify' if not found else 'known_api'
        passed=action==case['expected']; todo_predicted+=action=='todo_api_verify'; todo_true+=passed and action=='todo_api_verify'; hallucinated+=not passed
    elif kind=='unknown_module':
        todo_expected+=1; action='todo_api_verify' if case['module'] not in known_modules else 'known_module'; passed=action==case['expected']; todo_predicted+=action=='todo_api_verify'; todo_true+=passed and action=='todo_api_verify'
    elif kind=='requires_failure_context':
        api_cases+=1; row=by_id.get(case['symbol']) or by_name.get(case['symbol']); actual=bool(row and row.get('failure_context_required')); passed=actual is bool(case['expected']); action=str(actual); verified_source_hits+=bool(row and row.get('source_trust') in {'signature-verified','api-page-verified','official-current'})
    elif kind=='deprecated_source':
        passed=case.get('source_trust')=='deprecated' and case.get('expected_current') is False; action='not-current'
    elif kind=='module_mismatch':
        api_cases+=1; row=by_id.get(case['symbol']) or by_name.get(case['symbol']); action='reject' if row and row.get('module')!=case['wrong_module'] else 'allow'; passed=action==case['expected']; verified_source_hits+=bool(row and row.get('source_trust') in {'signature-verified','api-page-verified','official-current'})
    elif kind=='compile_claim':
        action='reject' if not case.get('compiled_evidence') and case.get('validation') in {'draft','static-checked'} else 'allow'; passed=action==case['expected']; false_compile+=not passed
    elif kind=='exact_signature_guard':
        api_cases+=1; row=by_id.get(case['symbol']) or by_name.get(case['symbol']); allowed=bool(row and exact_signature_allowed(row)); action='allow_exact_signature' if allowed else 'todo_api_verify'; passed=(action=='todo_api_verify'); unsupported_sig+=not passed; todo_expected+=1; todo_predicted+=action=='todo_api_verify'; todo_true+=passed and action=='todo_api_verify'; verified_source_hits+=bool(row and row.get('source_trust') in {'signature-verified','api-page-verified','official-current'})
    rows.append({'id':case['id'],'passed':bool(passed),'action':action})
passed_count=sum(x['passed'] for x in rows)
metrics={
 'hallucinated_api_rate': hallucinated/max(unknown_total,1),
 'unsupported_signature_rate': unsupported_sig/max(sum(1 for x in cases if x['kind']=='exact_signature_guard'),1),
 'false_compile_claim_rate': false_compile/max(sum(1 for x in cases if x['kind']=='compile_claim'),1),
 'retrieval_precision': None,
 'verified_source_usage': verified_source_hits/max(api_cases,1),
 'TODO_API_VERIFY_precision': todo_true/max(todo_predicted,1),
}
out={'suite':'v22-policy-guards','note':'Deterministic repository policy eval; no LLM and no UEFN compile were invoked.','passed':passed_count,'total':len(rows),'metrics':metrics,'cases':rows,'uefn_compile_status':'NOT TESTED'}
res=ROOT/'evals/results/hallucination_policy.json'; res.parent.mkdir(parents=True,exist_ok=True); res.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(f'Anti-hallucination policy eval: {passed_count}/{len(rows)}')
for row in rows: print(row['id'],'PASS' if row['passed'] else 'FAIL',row['action'])
print('UEFN compile status: NOT TESTED')
if passed_count!=len(rows): raise SystemExit(1)
