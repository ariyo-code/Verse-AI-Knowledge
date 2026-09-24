#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter
from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from migrate_api_catalog_v24 import build_generated as build_v24, build_queue, build_evidence_graph, build_revalidation_state, render

def build_generated(root:Path=ROOT):
    rows,modules,versions=build_v24(root)
    modules=dict(modules); modules['schema_version']=4
    versions=dict(versions); versions['schema_version']=4
    versions['note']='V25 preserves V24 field-level evidence and adds professionalized tooling/multi-version diff infrastructure.'
    return rows,modules,versions

def build_coverage(rows,api_version):
    total=len(rows)
    def metric(fn):
        n=sum(1 for r in rows if fn(r)); return {'count':n,'percent':round(100*n/max(total,1),2)}
    modules=sorted({r.get('module') for r in rows if r.get('module')})
    cov={
      'presence':metric(lambda r:(r.get('coverage') or {}).get('presence')),
      'signature_verified':metric(lambda r:(r.get('coverage') or {}).get('signature')),
      'parameters_structured':metric(lambda r:(r.get('coverage') or {}).get('parameters')),
      'return_type_structured':metric(lambda r:(r.get('coverage') or {}).get('return_type')),
      'effects_structured':metric(lambda r:(r.get('coverage') or {}).get('effects')),
      'event_names_known':metric(lambda r:(r.get('coverage') or {}).get('event_names')),
      'event_payloads_verified':metric(lambda r:(r.get('coverage') or {}).get('event_payloads')),
      'members_known':metric(lambda r:bool(r.get('member_names'))),
      'member_evidence_verified':metric(lambda r:bool((r.get('field_evidence') or {}).get('member_names'))),
      'enum_values_known':metric(lambda r:bool(r.get('enum_values'))),
      'inheritance_known':metric(lambda r:bool(r.get('inheritance'))),
      'exact_signature_claim_allowed':metric(lambda r:r.get('exact_signature_claim_allowed')),
      'field_evidence_present':metric(lambda r:any((r.get('field_evidence') or {}).values())),
    }
    stale=sum(1 for r in rows if (r.get('revalidation') or {}).get('status') not in {'current','not-applicable'})
    return {'schema_version':3,'generated_by':'tools/migrate_api_catalog_v25.py','api_version':api_version,'symbol_count':total,'module_count':len(modules),'modules':modules,'coverage':cov,
      'source_trust_breakdown':dict(sorted(Counter(r.get('source_trust','unknown') for r in rows).items())),
      'validation_breakdown':dict(sorted(Counter(r.get('validation','draft') for r in rows).items())),
      'claim_state_breakdown':dict(sorted(Counter(r.get('claim_state','presence-only') for r in rows).items())),
      'revalidation':{'current':total-stale,'needs_attention':stale},
      'note':'Coverage describes evidence for symbols currently known to this repository. It is not the percentage of Epic\'s total Verse API surface.'}

def write_all(root:Path=ROOT):
    rows,modules,versions=build_generated(root)
    outputs={
      root/'knowledge/api/symbols.jsonl':render(rows),
      root/'knowledge/api/modules.json':json.dumps(modules,indent=2,ensure_ascii=False)+'\n',
      root/'knowledge/api/versions.json':json.dumps(versions,indent=2,ensure_ascii=False)+'\n',
      root/'knowledge/api/coverage.json':json.dumps(build_coverage(rows,versions['current']),indent=2,ensure_ascii=False)+'\n',
      root/'knowledge/api/verification_queue.json':json.dumps(build_queue(rows),indent=2,ensure_ascii=False)+'\n',
      root/'knowledge/api/evidence_graph.json':json.dumps(build_evidence_graph(rows,root),indent=2,ensure_ascii=False)+'\n',
      root/'knowledge/api/revalidation_state.json':json.dumps(build_revalidation_state(rows,root),indent=2,ensure_ascii=False)+'\n',
    }
    for p,c in outputs.items(): p.write_text(c,encoding='utf-8')
    return outputs
if __name__=='__main__':
    for p in write_all(): print(p.relative_to(ROOT))
