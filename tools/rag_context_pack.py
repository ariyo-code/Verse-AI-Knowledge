#!/usr/bin/env python3
from pathlib import Path
import argparse,json
from rag_query import retrieve, excerpt, route, exact_api_matches, ROOT, CONFIG

def main():
    p=argparse.ArgumentParser(description="Build a compact context pack for Codex/AI.")
    p.add_argument("query")
    p.add_argument("--budget",type=int,default=None,help="Approximate character budget.")
    p.add_argument("--limit",type=int,default=None)
    p.add_argument("--output",default="rag/context_pack.md")
    args=p.parse_args()

    budget=args.budget or CONFIG["default_context_budget_chars"]
    limit=args.limit or CONFIG["default_max_results"]
    rows=retrieve(args.query,limit*3)

    selected=[]
    used=0
    seen_titles=set()

    for score,doc,meta in rows:
        # Avoid near-duplicate title cards consuming context.
        dedupe=(doc["title"].lower(),doc.get("verification"))
        if dedupe in seen_titles and "docs/api/" in doc["path"]:
            continue

        chunk=excerpt(doc["path"],args.query)
        block=(
            f"## {doc['title']}\n"
            f"Source file: `{doc['path']}`\n"
            f"Retrieval score: {score:.2f}\n"
            f"Trust: {meta['trust']:.2f}\n\n"
            f"{chunk}\n\n"
        )
        if selected and used+len(block)>budget:
            continue
        if not selected and len(block)>budget:
            block=block[:budget]
        selected.append((doc,score,meta,block))
        used+=len(block)
        seen_titles.add(dedupe)
        if len(selected)>=limit or used>=budget:
            break

    header=[
        "# Verse AI Context Pack",
        "",
        f"Query: {args.query}",
        f"Routes: {', '.join(route(args.query)) or 'generic'}",
        f"Exact API matches: {', '.join(exact_api_matches(args.query)) or 'none'}",
        f"Budget: {budget} chars",
        f"Selected sources: {len(selected)}",
        "",
        "## Agent rules",
        "",
        "- Use this context as retrieval evidence, not as proof of compilation.",
        "- Prefer higher-trust sources when claims conflict.",
        "- Verify uncertain/current APIs against official Epic documentation.",
        "- If UEFN MCP is available, compile after meaningful changes.",
        "- Never claim `verified` without real evidence.",
        "",
        "## Retrieved context",
        ""
    ]

    body="\n".join(header)+"\n"
    for _,_,_,block in selected:
        body+=block

    out=Path(args.output)
    if not out.is_absolute():
        out=ROOT/out
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(body,encoding="utf-8")

    manifest={
        "query":args.query,
        "routes":route(args.query),
        "exact_api_matches":exact_api_matches(args.query),
        "budget_chars":budget,
        "used_chars":used,
        "sources":[
            {
                "path":doc["path"],
                "title":doc["title"],
                "score":round(score,3),
                "trust":round(meta["trust"],2),
                "status":doc.get("status"),
                "verification":doc.get("verification")
            } for doc,score,meta,_ in selected
        ]
    }
    manifest_path=out.with_suffix(".json")
    manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding="utf-8")

    print(out)
    print(manifest_path)
    print(f"Selected {len(selected)} source(s), ~{used} chars")

if __name__=="__main__":
    main()
