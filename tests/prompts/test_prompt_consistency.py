from pathlib import Path
import json,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
def test_current_version_and_entrypoint():
 m=json.loads((ROOT/'manifest.json').read_text(encoding='utf-8')); assert m['schema_version']==25; assert m['release']['version']=='25.0.0'; assert m['entrypoint']=='AI_BOOTSTRAP.md'
def test_generated_prompts_no_drift(tmp_path):
 before={p:(ROOT/p).read_text(encoding='utf-8') for p in ['PROMPT_AI_CHAT_FR_EN.md','portable/current/VERSE_AI_MASTER_PROMPT.txt','portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt','portable/current/TASK_TEMPLATE.txt']}
 assert subprocess.run([sys.executable,str(ROOT/'tools/build_prompts.py')],cwd=ROOT).returncode==0
 after={p:(ROOT/p).read_text(encoding='utf-8') for p in before}; assert before==after
def test_no_legacy_status_in_current_prompt():
 text=(ROOT/'PROMPT_AI_CHAT_FR_EN.md').read_text(encoding='utf-8'); assert 'upstream-verified' not in text; assert 'AI_BOOTSTRAP.md' in text
def test_legacy_is_archived():
 assert (ROOT/'portable/CURRENT').read_text().strip()=='v25'; assert (ROOT/'portable/archive/v24/VERSE_AI_MASTER_PROMPT_WITH_UI.txt').exists()
