#!/usr/bin/env python3
from pathlib import Path
import json,time,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src')); sys.path.insert(0,str(ROOT/'tools'))
from verse_ai_knowledge import KnowledgeBase
from rag_query import retrieve
kb=KnowledgeBase(ROOT)

def bench(fn,n=100):
    t=time.perf_counter()
    for _ in range(n): fn()
    return round((time.perf_counter()-t)*1000/n,4)
metrics={
 'environment_note':'Local package-build environment; metrics are comparative diagnostics, not service SLOs.',
 'api_lookup_ms_mean':bench(lambda:kb.lookup_api('GetFortCharacter')),
 'claim_resolution_ms_mean':bench(lambda:kb.resolve_claim('GetFortCharacter','signature')),
 'rag_query_ms_mean':bench(lambda:retrieve('GetFortCharacter decides transacts failure context',10),20),
 'rag_document_count':json.loads((ROOT/'rag/index.json').read_text(encoding='utf-8')).get('document_count'),
}
out=ROOT/'reports/PERFORMANCE_V25.json'; out.write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8'); print(json.dumps(metrics,indent=2))
