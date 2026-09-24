#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--output'); a=ap.parse_args()
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')); version=str(m['verse_api_version'])
rows=[json.loads(x) for x in (ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
# Deterministic snapshot: no wall-clock timestamp.
payload={'schema_version':1,'api_version':version,'generated_by':'tools/api_snapshot.py','source_revision':hashlib.sha256((ROOT/'knowledge/api/evidence_graph.json').read_bytes()).hexdigest()[:16],'symbols':rows}
out=Path(a.output) if a.output else ROOT/'knowledge/api/snapshots'/version/'symbols.json'
if not out.is_absolute(): out=ROOT/out
out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(payload,indent=2,ensure_ascii=False,sort_keys=True)+'\n',encoding='utf-8'); print(out.relative_to(ROOT) if out.is_relative_to(ROOT) else out)
