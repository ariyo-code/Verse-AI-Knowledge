#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(); ap.add_argument('--github-ci',choices=['PASS','FAIL','UNKNOWN'],default='UNKNOWN'); ap.add_argument('--json-output',default='reports/PUBLIC_RELEASE_AUDIT_CURRENT.json'); ap.add_argument('--md-output',default='reports/PUBLIC_RELEASE_AUDIT_CURRENT.md'); a=ap.parse_args()
m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')); cov=json.loads((ROOT/'knowledge/api/coverage.json').read_text(encoding='utf-8'))
checks={}
for name,cmd in {'repository_integrity':['tools/validate_v25_integrity.py'],'prompt_consistency':['tests/prompts/test_prompt_consistency.py'],'secret_scan':['tools/scan_secrets.py'],'internal_paths':['tools/check_internal_paths.py'],'generated_drift':['tools/check_generated_drift.py']}.items():
 rc=subprocess.run([sys.executable,str(ROOT/cmd[0])],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode; checks[name]='PASS' if rc==0 else 'FAIL'
checks['github_ci']=a.github_ci
blocking=any(v=='FAIL' for v in checks.values()); readiness='BLOCKED' if blocking else ('READY' if a.github_ci=='PASS' else 'UNKNOWN')
data={'release':m['release']['version'],'schema':m['schema_version'],'api_snapshot':m['verse_api_version'],'checks':checks,'api_coverage':cov,'validation_boundaries':{'uefn_compile':'NOT TESTED','runtime':'NOT TESTED','multiplayer':'NOT TESTED','llm_benchmark':'SKIPPED unless configured'},'publication_readiness':readiness}
(ROOT/a.json_output).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
lines=['# Public Release Audit — Current','',f"- Release: **{data['release']}**",f"- Schema: **{data['schema']}**",f"- API snapshot: **{data['api_snapshot']}**",'', '## Checks','']+[f'- {k}: **{v}**' for k,v in checks.items()]+['','## Validation boundaries','','- UEFN compile: **NOT TESTED**','- Runtime: **NOT TESTED**','- Multiplayer: **NOT TESTED**','- LLM benchmark: **SKIPPED unless configured**','','## Publication',f"**PUBLICATION READINESS: {readiness}**",'']
(ROOT/a.md_output).write_text('\n'.join(lines),encoding='utf-8'); print(a.md_output); print(f'PUBLICATION READINESS: {readiness}')
