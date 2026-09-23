#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import datetime
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.api_index import load_symbols  # noqa: E402

API_RE = re.compile(r"\b(?:Get[A-Z][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*_device|fort_[A-Za-z0-9_]+|player_ui)\b")
FALSE_COMPILE_RE = re.compile(
    r"(?:status\s*:\s*`?(?:compiled|verified|multiplayer-verified)|UEFN\s+compile\s*:\s*`?(?:PASSED|SUCCESS))",
    re.I,
)

ap = argparse.ArgumentParser()
ap.add_argument("--responses")
ap.add_argument("--output")
args = ap.parse_args()

if not args.responses:
    print("SKIPPED — no LLM provider or saved responses configured")
    raise SystemExit(0)

payload = json.loads(Path(args.responses).read_text(encoding="utf-8"))
responses = payload.get("responses") or {}
cases = json.loads((ROOT / "evals/llm/cases.json").read_text(encoding="utf-8"))["cases"]
symbols = load_symbols(ROOT)
known = {r["name"] for r in symbols} | {r["symbol_id"] for r in symbols}

rows = []
for case in cases:
    output = str(responses.get(case["id"], ""))
    if not output:
        rows.append({"id": case["id"], "status": "MISSING_RESPONSE"})
        continue
    api_like = sorted(set(API_RE.findall(output)))
    unknown = [x for x in api_like if x not in known]
    todo = output.count("TODO(API VERIFY)")
    expected = case.get("expected_behaviour") or {}
    checks = {}
    if expected.get("must_not_invent_api"):
        # Conservative: unknown API-looking tokens require explicit uncertainty.
        checks["unknown_api_guarded"] = (not unknown) or todo > 0
    if expected.get("must_use_todo_api_verify_when_uncertain"):
        checks["todo_present"] = todo > 0
    if expected.get("must_not_claim_compiled"):
        checks["no_false_compile_claim"] = not bool(FALSE_COMPILE_RE.search(output))
    rows.append({
        "id": case["id"],
        "status": "PASS" if checks and all(checks.values()) else "REVIEW",
        "checks": checks,
        "unknown_api_like_tokens": unknown,
        "todo_api_verify_count": todo,
        "output_sha256": hashlib.sha256(output.encode()).hexdigest(),
    })

completed = [r for r in rows if r["status"] != "MISSING_RESPONSE"]
result = {
    "schema_version": 1,
    "suite": "v24-llm-end-to-end-saved-responses",
    "provider": payload.get("provider"),
    "model": payload.get("model"),
    "created_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    "case_count": len(cases),
    "responses_count": len(completed),
    "pass_count": sum(r["status"] == "PASS" for r in completed),
    "review_count": sum(r["status"] == "REVIEW" for r in completed),
    "tasks": rows,
    "uefn_compile_status": "NOT TESTED",
    "warning": "Static response review is not a UEFN compile and does not prove zero hallucinations.",
}
out = Path(args.output) if args.output else ROOT / "evals/llm/results/latest.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(out)
print(f"Saved-response LLM eval: PASS={result['pass_count']} REVIEW={result['review_count']} RESPONSES={result['responses_count']}/{result['case_count']}")
