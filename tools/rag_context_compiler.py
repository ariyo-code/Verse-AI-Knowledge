#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from rag_query import score_doc, excerpt, exact_api_matches  # noqa: E402
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.claims import resolve_claim  # noqa: E402

INDEX = json.loads((ROOT / "rag/index.json").read_text(encoding="utf-8"))


def role(doc: dict) -> str:
    p = doc["path"].lower()
    if p.startswith("projects/"):
        return "project_context"
    if "docs/api/" in p or p.endswith("api_catalog.json") or p.startswith("knowledge/api/") or p.endswith("module_catalog.json"):
        return "api_evidence"
    if p.startswith("errors/"):
        return "error_memory"
    if p.startswith("docs/patterns/") or "lifecycle" in p or "async" in p:
        return "lifecycle"
    if p.startswith("mcp/") or p.startswith("lab/") or "verification" in p or "quality" in p:
        return "verification"
    if p.startswith("external/corpus/"):
        return "external_examples"
    return "supporting"


def required(query: str) -> list[str]:
    q = query.lower()
    out = {"api_evidence", "verification"}
    if any(x in q for x in ["system", "vehicle", "inventory", "staff", "rp", "ui", "phone"]):
        out.add("project_context")
    if "error" in q or "compiler" in q:
        out.add("error_memory")
    if any(x in q for x in ["cleanup", "lifecycle", "leave", "join", "respawn", "async", "race", "spawn"]):
        out.add("lifecycle")
    return sorted(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--output", default="rag/generated/EVIDENCE_PACK.md")
    args = ap.parse_args()

    rows = []
    for doc in INDEX["documents"]:
        score, meta = score_doc(args.query, doc)
        if score > 0:
            rows.append((score, doc, meta))
    rows.sort(key=lambda x: (-x[0], x[1]["path"]))

    req = required(args.query)
    chosen = []
    used = set()
    for wanted in req:
        candidate = next((x for x in rows if role(x[1]) == wanted and x[1]["path"] not in used), None)
        if candidate:
            chosen.append((wanted, *candidate))
            used.add(candidate[1]["path"])
    for wanted in ["project_context", "api_evidence", "lifecycle", "error_memory", "verification", "external_examples"]:
        if len(chosen) >= 10:
            break
        candidate = next((x for x in rows if role(x[1]) == wanted and x[1]["path"] not in used), None)
        if candidate:
            chosen.append((wanted, *candidate))
            used.add(candidate[1]["path"])
    for item in rows:
        if len(chosen) >= 12:
            break
        if item[1]["path"] not in used:
            chosen.append((role(item[1]), *item))
            used.add(item[1]["path"])

    packed = [
        {
            "role": rr,
            "score": round(score, 3),
            "source_trust": meta["source_trust"],
            "validation": meta["validation"],
            "path": doc["path"],
            "title": doc["title"],
            "excerpt": excerpt(doc["path"], args.query, max_chars=1500),
        }
        for rr, score, doc, meta in chosen
    ]
    present = {x["role"] for x in packed}
    missing = [x for x in req if x not in present]
    exact = exact_api_matches(args.query)
    exact_claims = {
        name: {
            "signature": resolve_claim(name, "signature", root=ROOT),
            "parameters": resolve_claim(name, "parameters", root=ROOT),
            "return_type": resolve_claim(name, "return_type", root=ROOT),
            "effects": resolve_claim(name, "effects", root=ROOT),
        }
        for name in exact
    }

    lines = [
        "# Evidence Pack — V24",
        "",
        f"Query: `{args.query}`",
        f"Required: {', '.join(req)}",
        f"Missing: {', '.join(missing) or 'none'}",
        f"Exact API matches: {', '.join(exact) or 'none'}",
        "",
        "## Claim guard",
        "",
        "- Source trust and local validation are independent.",
        "- Presence evidence does not prove an exact signature or any other exact field.",
        "- Resolve signatures, parameters, return types, effects and event payloads independently.",
        "- External compile claims are not local compile proof.",
        "- Static checks do not prove UEFN compilation.",
        "- Unsupported exact API claims must use `TODO(API VERIFY)`.",
        "",
    ]
    for i, item in enumerate(packed, 1):
        lines += [
            f"## {i}. {item['role']} — `{item['path']}`",
            "",
            f"- source_trust: `{item['source_trust']}`",
            f"- validation: `{item['validation']}`",
            "",
            "```text",
            item["excerpt"],
            "```",
            "",
        ]

    out = ROOT / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    out.with_suffix(".json").write_text(
        json.dumps(
            {
                "schema_version": 2,
                "query": args.query,
                "required_roles": req,
                "missing_required_roles": missing,
                "exact_api_matches": exact,
                "exact_api_claims": exact_claims,
                "sources": [{k: v for k, v in x.items() if k != "excerpt"} for x in packed],
            },
            indent=2,
            ensure_ascii=False,
        ) + "\n",
        encoding="utf-8",
    )
    print(f"Evidence sources: {len(packed)}")
    print(f"Missing roles: {missing}")
    if missing:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
