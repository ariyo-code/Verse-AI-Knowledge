#!/usr/bin/env python3
"""Fetch one official Epic API page into an UNVERIFIED candidate file.

V24 security:
- only HTTPS dev.epicgames.com/documentation/ URLs;
- credentials rejected;
- redirect destination revalidated;
- response size/content type bounded;
- fetched content is treated as data, never instructions.

This tool never edits verified symbol knowledge and never auto-promotes signatures.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.epic_http import fetch_epic, validate_epic_url  # noqa: E402


def rows():
    return [
        json.loads(x)
        for x in (ROOT / "knowledge/api/symbols.jsonl").read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]


def clean_html(s):
    s = re.sub(r"<script\b[^>]*>.*?</script>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<style\b[^>]*>.*?</style>", " ", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", unescape(s)).strip()


def code_blocks(html):
    out = []
    for m in re.finditer(r"<(?:code|pre)\b[^>]*>(.*?)</(?:code|pre)>", html, re.I | re.S):
        t = clean_html(m.group(1))
        if t and len(t) < 3000:
            out.append(t)
    return list(dict.fromkeys(out))


def signature_candidates(symbol, blocks):
    needles = [symbol, symbol.split(".")[-1]]
    out = []
    for block in blocks:
        if any(n in block for n in needles) and ("(" in block or ":=" in block) and ":" in block:
            out.append(block)
    return out[:20]


ap = argparse.ArgumentParser()
ap.add_argument("--symbol", required=True)
ap.add_argument("--url")
ap.add_argument("--timeout", type=int, default=20)
ap.add_argument("--max-bytes", type=int, default=2_000_000)
args = ap.parse_args()

row = next(
    (x for x in rows() if x["symbol_id"].casefold() == args.symbol.casefold() or x["name"].casefold() == args.symbol.casefold()),
    None,
)
if not row:
    raise SystemExit("Unknown local symbol; discovery must happen before signature harvesting.")

url = validate_epic_url(args.url or row.get("source_url") or "")
raw, final_url, content_type = fetch_epic(url, timeout=args.timeout, max_bytes=args.max_bytes)
html = raw.decode("utf-8", "replace")
blocks = code_blocks(html)
sigs = signature_candidates(row["symbol_id"], blocks)

out = {
    "schema_version": 2,
    "candidate_only": True,
    "symbol_id": row["symbol_id"],
    "api_version": row.get("api_version"),
    "requested_url": url,
    "source_url": final_url,
    "content_type": content_type,
    "source_sha256": hashlib.sha256(raw).hexdigest(),
    "signature_candidates": sigs,
    "code_block_count": len(blocks),
    "warning": "UNVERIFIED HARVEST OUTPUT. Review exact official page before promotion.",
}
dest = ROOT / "knowledge/api/candidates" / f"{row['symbol_id'].replace('/', '_')}.json"
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(dest.relative_to(ROOT))
print(f"candidate signatures: {len(sigs)}")
print("Status: CANDIDATE ONLY — NOT VERIFIED")
