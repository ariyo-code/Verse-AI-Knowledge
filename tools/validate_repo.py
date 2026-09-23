#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
required=[
 'AGENTS.md','AI_BOOTSTRAP.md','manifest.json','pyproject.toml','knowledge/api/symbols.jsonl',
 'knowledge/api/modules.json','knowledge/api/versions.json','schemas/trust.schema.json',
 'schemas/validation_status.schema.json','external/corpus_manifest.json','tools/corpus_coverage.py',
 'tools/ensure_full_corpus.py','tools/analyze_verse_dependencies.py','rag/evidence_policy.json',
 'tools/rag_build_evidence_graph.py','tools/rag_context_compiler.py','evals/retrieval/evidence_composition.json',
 'prompts/EVIDENCE_FIRST_CODEX_AGENT.md','lab/compile_queue.json','.github/workflows/ci.yml'
]
errors=[x for x in required if not (ROOT/x).exists()]
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
if m.get('schema_version')!=22: errors.append('schema_version != 22')
q=json.loads((ROOT/'lab/compile_queue.json').read_text(encoding='utf-8'))
if len(q.get('entries',[]))!=50: errors.append('compile queue != 50')
if errors:
    print('Repository validation FAILED')
    for x in errors: print('-',x)
    raise SystemExit(1)
print('Repository validation OK')
