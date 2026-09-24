#!/usr/bin/env python3
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.policy import SOURCE_TRUST,VALIDATION
errors=[]
def load(rel):
 p=ROOT/rel
 if not p.exists(): errors.append(f'missing: {rel}'); return {}
 try:return json.loads(p.read_text(encoding='utf-8'))
 except Exception as e: errors.append(f'{rel}: invalid JSON: {e}'); return {}
m=load('manifest.json'); marker=load('portable/generated_code_marker.json'); schema=load('schemas/generated_artifact.schema.json')
if m.get('schema_version')!=25: errors.append('manifest schema_version != 25')
if m.get('release',{}).get('version')!='25.0.0': errors.append('manifest release != 25.0.0')
if marker.get('marker_version')!='v25': errors.append('marker_version != v25')
if tuple(marker.get('allowed_statuses',[]))!=tuple(VALIDATION): errors.append('marker validation statuses diverge')
if schema.get('properties',{}).get('version',{}).get('const')!='v25': errors.append('generated artifact schema not v25')
for rel in ['ROADMAP.md','prompt_sources/core.yaml','tools/build_prompts.py','portable/current/VERSE_AI_MASTER_PROMPT.txt','portable/archive/v24/VERSE_AI_MASTER_PROMPT_WITH_UI.txt','src/verse_ai_knowledge/knowledge_base.py','mcp/server.py','mkdocs.yml','.github/CODEOWNERS','.github/dependabot.yml','.github/workflows/codeql.yml','.github/workflows/release.yml','THIRD_PARTY_MANIFEST.json','schemas/api_candidate.schema.json','reports/BASELINE_BEFORE_UPGRADE.json']:
 if not (ROOT/rel).exists(): errors.append(f'missing: {rel}')
# Prompt source files are JSON-as-YAML and deterministic
for p in sorted((ROOT/'prompt_sources').glob('*.yaml')):
 try: json.loads(p.read_text(encoding='utf-8'))
 except Exception as e: errors.append(f'{p.relative_to(ROOT)} invalid canonical prompt source: {e}')
# API index invariants
seen=set()
for n,line in enumerate((ROOT/'knowledge/api/symbols.jsonl').read_text(encoding='utf-8').splitlines(),1):
 if not line.strip(): continue
 row=json.loads(line); sid=row.get('symbol_id')
 if sid in seen: errors.append(f'duplicate symbol {sid}')
 seen.add(sid)
 if row.get('source_trust') not in SOURCE_TRUST: errors.append(f'{sid}: bad source_trust')
 if row.get('validation') not in VALIDATION: errors.append(f'{sid}: bad validation')
 if row.get('exact_signature_claim_allowed') and not (row.get('signature') and (row.get('field_evidence') or {}).get('signature')): errors.append(f'{sid}: exact signature without evidence')
# current docs should not use old marker as current provenance
for rel in ['README.md','AI_BOOTSTRAP.md','docs/GENERATED_CODE_MARKER.md','PROMPT_AI_CHAT_FR_EN.md']:
 text=(ROOT/rel).read_text(encoding='utf-8',errors='ignore')
 if 'verse-ai-generated:v24' in text or 'verse-ai-generated:v23' in text: errors.append(f'{rel}: legacy marker in current doc')
if errors:
 print('V25 integrity FAILED'); [print('-',e) for e in sorted(set(errors))]; raise SystemExit(1)
print('V25 integrity OK'); print(f'Structured symbols: {len(seen)}'); print('UEFN compile status: NOT TESTED by this validator')
