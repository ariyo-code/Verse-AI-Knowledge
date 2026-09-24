#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from migrate_api_catalog_v25 import (  # noqa: E402
    build_generated, build_coverage, build_queue, build_evidence_graph,
    build_revalidation_state, render,
)

errors = []
rows, modules, versions = build_generated(ROOT)
expected = {
    ROOT / "knowledge/api/symbols.jsonl": render(rows),
    ROOT / "knowledge/api/modules.json": json.dumps(modules, indent=2, ensure_ascii=False) + "\n",
    ROOT / "knowledge/api/versions.json": json.dumps(versions, indent=2, ensure_ascii=False) + "\n",
    ROOT / "knowledge/api/coverage.json": json.dumps(build_coverage(rows, versions["current"]), indent=2, ensure_ascii=False) + "\n",
    ROOT / "knowledge/api/verification_queue.json": json.dumps(build_queue(rows), indent=2, ensure_ascii=False) + "\n",
    ROOT / "knowledge/api/evidence_graph.json": json.dumps(build_evidence_graph(rows, ROOT), indent=2, ensure_ascii=False) + "\n",
    ROOT / "knowledge/api/revalidation_state.json": json.dumps(build_revalidation_state(rows, ROOT), indent=2, ensure_ascii=False) + "\n",
}
for path, content in expected.items():
    if not path.exists():
        errors.append(f"missing generated file: {path.relative_to(ROOT)}")
    elif path.read_text(encoding="utf-8") != content:
        errors.append(f"generated drift: {path.relative_to(ROOT)}")

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
version = (ROOT / "VERSION.md").read_text(encoding="utf-8")
if manifest.get("release", {}).get("version") not in version:
    errors.append("VERSION.md release metadata drift")
if str(manifest.get("verse_api_version")) not in version:
    errors.append("VERSION.md Verse API metadata drift")

if errors:
    print("Generated-file drift FAILED")
    for error in errors:
        print("-", error)
    raise SystemExit(1)

print("Generated-file drift OK")

# V25 prompt compiler drift
import importlib.util
spec=importlib.util.spec_from_file_location('build_prompts',ROOT/'tools/build_prompts.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
expected_public=mod.render_public(); expected_master=mod.body('en',False); expected_ui=mod.body('en',True)
for path,content in {ROOT/'PROMPT_AI_CHAT_FR_EN.md':expected_public,ROOT/'portable/current/VERSE_AI_MASTER_PROMPT.txt':expected_master,ROOT/'portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt':expected_ui}.items():
    if path.read_text(encoding='utf-8')!=content:
        print('Generated-file drift FAILED'); print('-',path.relative_to(ROOT),'prompt drift'); raise SystemExit(1)
print('V25 prompt drift OK')

# V25 prompt compiler drift
import importlib.util
spec=importlib.util.spec_from_file_location('build_prompts',ROOT/'tools/build_prompts.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
expected_public=mod.render_public(); expected_master=mod.body('en',False); expected_ui=mod.body('en',True)
for path,content in {ROOT/'PROMPT_AI_CHAT_FR_EN.md':expected_public,ROOT/'portable/current/VERSE_AI_MASTER_PROMPT.txt':expected_master,ROOT/'portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt':expected_ui}.items():
    if path.read_text(encoding='utf-8')!=content:
        print('Generated-file drift FAILED'); print('-',path.relative_to(ROOT),'prompt drift'); raise SystemExit(1)
print('V25 prompt drift OK')
