#!/usr/bin/env python3
"""Simple offline retrieval helper for Verse-AI-Knowledge."""

from pathlib import Path
import re
import sys
import math

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", "__pycache__"}
ALLOWED = {".md", ".json", ".verse"}

def tokenize(text: str):
    return re.findall(r"[a-zA-Z0-9_./<>-]+", text.lower())

def score(query_tokens, path, text):
    p = str(path).lower()
    lower = text.lower()
    s = 0.0
    for token in query_tokens:
        if token in p:
            s += 12
        n = lower.count(token)
        if n:
            s += 1 + min(n, 8)
    if "/api/" in p:
        s += 1
    if "/errors/" in p:
        s += 0.5
    return s

def main():
    if len(sys.argv) < 2:
        print('Usage: python tools/search_knowledge.py "query"')
        raise SystemExit(2)

    query = " ".join(sys.argv[1:])
    tokens = tokenize(query)
    results = []

    for p in ROOT.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in ALLOWED:
            continue
        if any(part in SKIP for part in p.parts):
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        s = score(tokens, p.relative_to(ROOT), text)
        if s > 0:
            lines = text.splitlines()
            hit = 0
            for i, line in enumerate(lines):
                if any(t in line.lower() for t in tokens):
                    hit = i
                    break
            excerpt = " ".join(lines[max(0,hit-1):hit+3]).strip()
            results.append((s, str(p.relative_to(ROOT)), excerpt[:300]))

    results.sort(key=lambda x: (-x[0], x[1]))
    for s, path, excerpt in results[:12]:
        print(f"[{s:.1f}] {path}")
        if excerpt:
            print(f"  {excerpt}")
    if not results:
        print("No local result. Verify the current official Epic documentation.")

if __name__ == "__main__":
    main()
