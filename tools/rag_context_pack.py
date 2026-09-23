#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
from rag_query import retrieve, excerpt, route, exact_api_matches, ROOT, CONFIG


def main() -> None:
    p = argparse.ArgumentParser(description="Build a compact V22 context pack.")
    p.add_argument("query")
    p.add_argument("--budget", type=int, default=None)
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--output", default="rag/context_pack.md")
    args = p.parse_args()

    budget = args.budget or CONFIG["default_context_budget_chars"]
    limit = args.limit or CONFIG["default_max_results"]
    rows = retrieve(args.query, limit * 3)
    selected = []
    used = 0
    seen = set()

    for score, doc, meta in rows:
        dedupe = (doc["title"].lower(), meta["source_trust"], meta["validation"])
        if dedupe in seen and "docs/api/" in doc["path"]:
            continue
        chunk = excerpt(doc["path"], args.query)
        block = (
            f"## {doc['title']}\n"
            f"Source file: `{doc['path']}`\n"
            f"Retrieval score: {score:.2f}\n"
            f"Source trust: `{meta['source_trust']}`\n"
            f"Local validation: `{meta['validation']}`\n\n"
            f"{chunk}\n\n"
        )
        if selected and used + len(block) > budget:
            continue
        if not selected and len(block) > budget:
            block = block[:budget]
        selected.append((doc, score, meta, block))
        used += len(block)
        seen.add(dedupe)
        if len(selected) >= limit or used >= budget:
            break

    lines = [
        "# Verse AI Context Pack — V22",
        "",
        f"Query: {args.query}",
        f"Routes: {', '.join(route(args.query)) or 'generic'}",
        f"Exact API matches: {', '.join(exact_api_matches(args.query)) or 'none'}",
        f"Budget: {budget} chars",
        f"Selected sources: {len(selected)}",
        "",
        "## Agent rules",
        "",
        "- `source_trust` and `validation` are independent.",
        "- Retrieval score is not proof of an API signature.",
        "- Prefer exact verified API evidence over semantic/lexical similarity.",
        "- Use `TODO(API VERIFY)` when an exact API claim cannot be verified.",
        "- Never claim a UEFN compile/runtime/multiplayer result without real evidence.",
        "",
        "## Retrieved context",
        "",
    ]
    body = "\n".join(lines) + "\n" + "".join(x[3] for x in selected)
    out = Path(args.output)
    if not out.is_absolute():
        out = ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")

    manifest = {
        "schema_version": 2,
        "query": args.query,
        "routes": route(args.query),
        "exact_api_matches": exact_api_matches(args.query),
        "budget_chars": budget,
        "used_chars": used,
        "sources": [
            {
                "path": doc["path"],
                "title": doc["title"],
                "score": round(score, 3),
                "source_trust": meta["source_trust"],
                "validation": meta["validation"],
            }
            for doc, score, meta, _ in selected
        ],
    }
    out.with_suffix(".json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out)
    print(out.with_suffix(".json"))
    print(f"Selected {len(selected)} source(s), ~{used} chars")


if __name__ == "__main__":
    main()
