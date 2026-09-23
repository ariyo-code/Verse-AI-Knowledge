#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from migrate_api_catalog_v22 import build_generated, render_symbols_jsonl  # noqa: E402

errors=[]
symbols,modules,versions=build_generated(ROOT)
expected={
    ROOT/'knowledge/api/symbols.jsonl': render_symbols_jsonl(symbols),
    ROOT/'knowledge/api/modules.json': json.dumps(modules,indent=2,ensure_ascii=False)+'\n',
    ROOT/'knowledge/api/versions.json': json.dumps(versions,indent=2,ensure_ascii=False)+'\n',
}
for path,content in expected.items():
    if not path.exists(): errors.append(f'missing generated file: {path.relative_to(ROOT)}'); continue
    if path.read_text(encoding='utf-8') != content: errors.append(f'generated drift: {path.relative_to(ROOT)}')
manifest=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
version=(ROOT/'VERSION.md').read_text(encoding='utf-8') if (ROOT/'VERSION.md').exists() else ''
if manifest.get('release',{}).get('version') not in version: errors.append('VERSION.md release metadata drift')
if str(manifest.get('verse_api_version')) not in version: errors.append('VERSION.md Verse API metadata drift')
if errors:
    print('Generated-file drift FAILED')
    for e in errors: print('-',e)
    raise SystemExit(1)
print('Generated-file drift OK')
