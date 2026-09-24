#!/usr/bin/env python3
from pathlib import Path
import json,math,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
from rag_query import retrieve
cases=json.loads((ROOT/'evals/retrieval/v25_cases.json').read_text(encoding='utf-8'))['cases']; rows=[]
for case in cases:
 res=retrieve(case['query'],10); paths=[doc['path'] for _,doc,_ in res]; ranks=[i+1 for i,p in enumerate(paths) if p in case['must_include_any']]; rank=min(ranks) if ranks else None; rows.append(rank)
def rec(k): return sum(1 for r in rows if r and r<=k)/len(rows)
mrr=sum((1/r if r else 0) for r in rows)/len(rows); ndcg=sum((1/math.log2(r+1) if r else 0) for r in rows)/len(rows)
out={'cases':len(rows),'Recall@1':round(rec(1),4),'Recall@5':round(rec(5),4),'Recall@10':round(rec(10),4),'MRR':round(mrr,4),'nDCG@10':round(ndcg,4)}
print(json.dumps(out,indent=2)); (ROOT/'reports/benchmarks').mkdir(parents=True,exist_ok=True); (ROOT/'reports/benchmarks/retrieval-v25.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
raise SystemExit(0)
