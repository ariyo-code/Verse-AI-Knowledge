#!/usr/bin/env python3
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
cov=json.loads((ROOT/'knowledge/api/coverage.json').read_text(encoding='utf-8'))
retr_path=ROOT/'reports/benchmarks/retrieval-v25.json'; retr=json.loads(retr_path.read_text(encoding='utf-8')) if retr_path.exists() else None
lines=['# V25 Metrics Dashboard','',f"Verse API snapshot: **{cov.get('api_version')}**",f"Known structured symbols: **{cov.get('symbol_count')}**",f"Modules represented: **{cov.get('module_count')}**",'', '## API evidence coverage','', '| Field | Count | Percent |','|---|---:|---:|']
for k,v in cov.get('coverage',{}).items(): lines.append(f"| `{k}` | {v.get('count')} | {v.get('percent')}% |")
lines += ['','## Retrieval benchmark','']
if retr:
    for k,v in retr.items(): lines.append(f'- {k}: **{v}**')
else: lines.append('- NOT RUN')
lines += ['','## End-to-end validation','', '- LLM benchmark: **SKIPPED unless configured**','- UEFN compile: **NOT TESTED**','- Runtime: **NOT TESTED**','- Multiplayer: **NOT TESTED**','', '> Only measured repository data is shown. Missing evidence is not converted into a score.','']
(ROOT/'docs/dashboard.md').write_text('\n'.join(lines),encoding='utf-8'); print('docs/dashboard.md')
