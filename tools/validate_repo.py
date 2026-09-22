#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]
req=["AGENTS.md","manifest.json","external/corpus_manifest.json","tools/corpus_coverage.py",
     "tools/ensure_full_corpus.py","tools/analyze_verse_dependencies.py","rag/evidence_policy.json",
     "tools/rag_build_evidence_graph.py","tools/rag_context_compiler.py","benchmarks/evidence_composition.json",
     "prompts/EVIDENCE_FIRST_CODEX_AGENT.md","lab/compile_queue.json"]
err=[x for x in req if not (ROOT/x).exists()]
m=json.loads((ROOT/"manifest.json").read_text())
if m.get("schema_version",0)<19: err.append("schema_version < 19")
q=json.loads((ROOT/"lab/compile_queue.json").read_text())
if len(q.get("entries",[]))!=50: err.append("compile queue != 50")
if err:
    print("Repository validation FAILED")
    for x in err: print("-",x)
    sys.exit(1)
print("Repository validation OK")
