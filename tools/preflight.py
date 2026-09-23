#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, ok, detail):
    checks.append({"name": name, "passed": bool(ok), "detail": detail})

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
check("schema", manifest.get("schema_version") == 24, f"schema={manifest.get('schema_version')}")
check("release", manifest.get("release", {}).get("version") == "24.0.0", f"release={manifest.get('release', {}).get('version')}")
check("AI bootstrap", (ROOT / "AI_BOOTSTRAP.md").exists(), "AI_BOOTSTRAP.md")

queue = json.loads((ROOT / "lab/compile_queue.json").read_text(encoding="utf-8"))
check("compile queue", len(queue.get("entries", [])) == 50, f"entries={len(queue.get('entries', []))}")

corpus = json.loads((ROOT / "external/corpus_manifest.json").read_text(encoding="utf-8"))
base = ROOT / "external/corpus" / corpus["source_id"] / corpus["source_revision"] / "examples"
local = len(list(base.rglob("*.verse"))) if base.exists() else 0
check("starter corpus", local > 0, f"local examples={local}/{corpus['expected_examples']}")

for name, rel in [
    ("structured API", "knowledge/api/symbols.jsonl"),
    ("API coverage", "knowledge/api/coverage.json"),
    ("API queue", "knowledge/api/verification_queue.json"),
    ("API evidence graph", "knowledge/api/evidence_graph.json"),
    ("API revalidation", "knowledge/api/revalidation_state.json"),
    ("generated provenance", "portable/generated_code_marker.json"),
    ("claim resolver", "tools/resolve_api_claim.py"),
    ("LLM eval harness", "evals/llm/runner.py"),
    ("evidence compiler", "tools/rag_context_compiler.py"),
    ("claim ledger", "tools/build_claim_ledger.py"),
    ("policy evals", "evals/hallucination/cases.json"),
    ("unified CI", ".github/workflows/ci.yml"),
]:
    check(name, (ROOT / rel).exists(), rel)

ok = all(x["passed"] for x in checks)
dest = ROOT / "reports/PREFLIGHT.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps({
    "passed": ok,
    "checks": checks,
    "uefn_compile_status": "NOT TESTED",
    "llm_end_to_end_status": "SKIPPED unless configured",
}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

print("Preflight:", "PASS" if ok else "FAIL")
for item in checks:
    print(f"[{'PASS' if item['passed'] else 'FAIL'}] {item['name']} - {item['detail']}")
print("UEFN compile status: NOT TESTED")
if not ok:
    raise SystemExit(1)
