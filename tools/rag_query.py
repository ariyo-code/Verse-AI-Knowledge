#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import argparse
import json
import math
import re
import sys

from rag_route_query import route

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.policy import canonical_source_trust, canonical_validation  # noqa: E402

CONFIG = json.loads((ROOT / "rag/config.json").read_text(encoding="utf-8"))
INDEX = json.loads((ROOT / "rag/index.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "knowledge/api_catalog.json").read_text(encoding="utf-8")).get("entries", {})
CURRENT_API = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8")).get("verse_api_version", "42.20")


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_./<>:-]+", text.lower())


def bm25(query_tokens: list[str], doc: dict, k1: float = 1.5, b: float = 0.75) -> float:
    n_docs = INDEX["document_count"]
    avgdl = INDEX["avg_document_length"] or 1
    dl = doc.get("token_count", 1)
    tf = doc.get("term_freq", {})
    df = INDEX.get("document_frequency", {})
    score = 0.0
    for token in query_tokens:
        freq = tf.get(token, 0)
        if not freq:
            continue
        seen = df.get(token, 0)
        idf = math.log(1 + (n_docs - seen + 0.5) / (seen + 0.5))
        score += idf * ((freq * (k1 + 1)) / (freq + k1 * (1 - b + b * dl / avgdl)))
    return score


def source_trust_score(doc: dict) -> float:
    value = canonical_source_trust(doc.get("source_trust"))
    return CONFIG["source_trust_scores"].get(value, CONFIG["source_trust_scores"].get("unknown", 0.35))


def validation_score(doc: dict) -> float:
    value = canonical_validation(doc.get("validation"))
    return CONFIG["validation_scores"].get(value, 0.25)


def path_route_bonus(path: str, routes: list[str]) -> int:
    p = path.lower()
    checks = {
        "api": ("docs/api/" in p or "api_catalog" in p or "knowledge/api/" in p),
        "project": "projects/" in p,
        "error": "errors/" in p,
        "mcp": "mcp/" in p,
        "ui": ("/ui/" in p or "ui" in p),
        "vehicle": "vehicle" in p,
        "persistence": "persist" in p,
        "maintenance": "maintenance/" in p,
    }
    return sum(1 for name in routes if checks.get(name, False))


def exact_api_matches(query: str) -> list[str]:
    q = query.lower()
    return sorted([name for name in CATALOG if name.lower() in q])


def semantic_similarity(_query: str, _doc: dict) -> float:
    # V22 keeps semantics optional. No provider is enabled by default.
    return 0.0


def score_doc(query: str, doc: dict) -> tuple[float, dict]:
    weights = CONFIG["weights"]
    tokens = tokenize(query)
    routes = route(query)
    exact_apis = exact_api_matches(query)
    score = bm25(tokens, doc) * weights["bm25"]
    path = doc["path"].lower()
    title = doc["title"].lower()

    for token in tokens:
        if token in path:
            score += weights["path_exact"] * 0.35
        if token in title:
            score += weights["title_exact"] * 0.35

    for api in exact_apis:
        if api in doc.get("api_symbols", []):
            score += weights["api_symbol_exact"]
        elif api.lower() in path:
            score += weights["api_symbol_exact"] * 0.8

    score += path_route_bonus(doc["path"], routes) * weights["routing_match"]
    if "projects/" in path and "project" in routes:
        score += weights["project_match"]
    if "errors/" in path and "error" in routes:
        score += weights["error_match"]

    trust = source_trust_score(doc)
    validation = validation_score(doc)
    score += trust * weights["source_trust"]
    score += validation * weights["validation"]

    if doc.get("verse_api") == CURRENT_API:
        score += weights["freshness"]

    semantic = 0.0
    if CONFIG.get("semantic", {}).get("enabled"):
        semantic = semantic_similarity(query, doc)
        score += semantic * weights.get("semantic_similarity", 0.0)

    return score, {
        "routes": routes,
        "exact_api_matches": exact_apis,
        "source_trust": canonical_source_trust(doc.get("source_trust")),
        "source_trust_score": trust,
        "validation": canonical_validation(doc.get("validation")),
        "validation_score": validation,
        "semantic_similarity": semantic,
    }


def excerpt(path: str, query: str, max_chars: int = 2200) -> str:
    p = ROOT / path
    text = p.read_text(encoding="utf-8", errors="ignore")
    qtokens = tokenize(query)
    lines = text.splitlines()
    best = 0
    best_score = -1
    for i, line in enumerate(lines):
        low = line.lower()
        s = sum(1 for token in qtokens if token in low)
        if s > best_score:
            best_score = s
            best = i
    start = max(0, best - 5)
    chunk = "\n".join(lines[start : start + 35]).strip()
    return chunk if len(chunk) <= max_chars else chunk[:max_chars] + "\n…"


def retrieve(query: str, limit: int = 12):
    rows = []
    for doc in INDEX["documents"]:
        score, meta = score_doc(query, doc)
        if score > 0:
            rows.append((score, doc, meta))
    rows.sort(key=lambda x: (-x[0], x[1]["path"]))
    return rows[:limit]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit", type=int, default=12)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    rows = retrieve(args.query, args.limit)
    if args.json:
        out = [
            {
                "score": round(score, 3),
                "path": doc["path"],
                "title": doc["title"],
                "source_trust": meta["source_trust"],
                "validation": meta["validation"],
                "source_trust_score": round(meta["source_trust_score"], 2),
                "validation_score": round(meta["validation_score"], 2),
            }
            for score, doc, meta in rows
        ]
        print(json.dumps({"query": args.query, "routes": route(args.query), "results": out}, indent=2, ensure_ascii=False))
    else:
        print("Routes:", ", ".join(route(args.query)) or "generic")
        for score, doc, meta in rows:
            print(f"[{score:.2f}] trust={meta['source_trust']} validation={meta['validation']} {doc['path']}")
            print(" ", doc["title"])


if __name__ == "__main__":
    main()
