#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.api_index import load_symbols  # noqa: E402

API_RE = re.compile(r"\b(?:Get[A-Z][A-Za-z0-9_]*|[A-Za-z_][A-Za-z0-9_]*_device|fort_[A-Za-z0-9_]+|player_ui)\b")
SIG_RE = re.compile(r"\b([A-Za-z_][A-Za-z0-9_.]*)\s*(?:<[^>]+>)*\s*\([^\n)]*\)\s*(?:<[^>]+>)*\s*:[A-Za-z_\[\]?][^\n`]*")

ap = argparse.ArgumentParser(description="Conservative static review of Verse API-looking claims.")
ap.add_argument("file")
ap.add_argument("--json", action="store_true")
ap.add_argument("--strict", action="store_true", help="Exit non-zero when review candidates exist.")
args = ap.parse_args()

path = Path(args.file)
text = path.read_text(encoding="utf-8", errors="ignore")
rows = load_symbols(ROOT)
known = {r["name"]: r for r in rows}
known.update({r["symbol_id"]: r for r in rows})

tokens = sorted(set(API_RE.findall(text)))
unknown = [t for t in tokens if t not in known]
exact_names = []
for m in SIG_RE.finditer(text):
    exact_names.append(m.group(1).split(".")[-1])
unsupported_exact = []
for name in sorted(set(exact_names)):
    row = known.get(name)
    if not row or not row.get("exact_signature_claim_allowed"):
        unsupported_exact.append(name)

todo_count = text.count("TODO(API VERIFY)")
result = {
    "file": str(path),
    "scan_type": "static-review-candidates",
    "warning": "Unknown API-looking identifiers are review candidates, not proof of hallucination.",
    "api_like_tokens": tokens,
    "unknown_api_like_tokens": unknown,
    "unsupported_exact_signature_claims": unsupported_exact,
    "todo_api_verify_count": todo_count,
    "review_required": bool(unknown or unsupported_exact),
}

if args.json:
    print(json.dumps(result, indent=2, ensure_ascii=False))
else:
    print("Verse API claim lint")
    print("File:", path)
    print("Unknown API-like review candidates:", len(unknown))
    for item in unknown:
        print("-", item)
    print("Unsupported exact signatures:", len(unsupported_exact))
    for item in unsupported_exact:
        print("-", item)
    print("TODO(API VERIFY):", todo_count)
    if result["review_required"]:
        print("Result: REVIEW REQUIRED")
    else:
        print("Result: no unsupported API-looking claim detected by this heuristic")

raise SystemExit(1 if args.strict and result["review_required"] else 0)
