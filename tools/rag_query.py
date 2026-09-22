#!/usr/bin/env python3
from pathlib import Path
import argparse,json,math,re
from collections import Counter
from rag_route_query import route

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/"rag/config.json").read_text(encoding="utf-8"))
INDEX=json.loads((ROOT/"rag/index.json").read_text(encoding="utf-8"))
CATALOG=json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8")).get("entries",{})

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_./<>:-]+",text.lower())

def bm25(query_tokens,doc,k1=1.5,b=0.75):
    N=INDEX["document_count"]
    avgdl=INDEX["avg_document_length"] or 1
    dl=doc.get("token_count",1)
    tf=doc.get("term_freq",{})
    df=INDEX.get("document_frequency",{})
    score=0.0
    for t in query_tokens:
        f=tf.get(t,0)
        if not f:
            continue
        n=df.get(t,0)
        idf=math.log(1+(N-n+0.5)/(n+0.5))
        score+=idf*((f*(k1+1))/(f+k1*(1-b+b*dl/avgdl)))
    return score

def trust_score(doc):
    table=CONFIG["trust_levels"]
    vals=[]
    for key in (doc.get("verification"),doc.get("status")):
        if key:
            vals.append(table.get(str(key).lower(),0.5))
    return max(vals) if vals else table.get("unspecified",0.5)

def path_route_bonus(path,routes):
    p=path.lower()
    bonus=0
    if "api" in routes and ("docs/api/" in p or "api_catalog" in p):
        bonus+=1
    if "project" in routes and "projects/" in p:
        bonus+=1
    if "error" in routes and "errors/" in p:
        bonus+=1
    if "mcp" in routes and "mcp/" in p:
        bonus+=1
    if "ui" in routes and ("/ui/" in p or "ui" in p):
        bonus+=1
    if "vehicle" in routes and "vehicle" in p:
        bonus+=1
    if "persistence" in routes and "persist" in p:
        bonus+=1
    if "maintenance" in routes and "maintenance/" in p:
        bonus+=1
    return bonus

def exact_api_matches(query):
    q=query.lower()
    found=[]
    for name in CATALOG:
        if name.lower() in q:
            found.append(name)
    return found

def score_doc(query,doc):
    weights=CONFIG["weights"]
    tokens=tokenize(query)
    routes=route(query)
    exact_apis=exact_api_matches(query)

    score=bm25(tokens,doc)*weights["bm25"]
    path=doc["path"].lower()
    title=doc["title"].lower()
    qlower=query.lower()

    for t in tokens:
        if t in path:
            score+=weights["path_exact"]*0.35
        if t in title:
            score+=weights["title_exact"]*0.35

    for api in exact_apis:
        if api in doc.get("api_symbols",[]):
            score+=weights["api_symbol_exact"]
        elif api.lower() in path:
            score+=weights["api_symbol_exact"]*0.8

    rbonus=path_route_bonus(doc["path"],routes)
    score+=rbonus*weights["routing_match"]

    if "projects/" in path and "project" in routes:
        score+=weights["project_match"]
    if "errors/" in path and "error" in routes:
        score+=weights["error_match"]

    score+=trust_score(doc)*weights["trust"]

    # Version freshness: exact current 42.20 gets slight boost; unknown stays neutral.
    if doc.get("verse_api")=="42.20":
        score+=weights["freshness"]

    status=(doc.get("status") or "").lower()
    if status in {"verified","multiplayer-verified","compiled"}:
        score+=weights["verified_status"]

    return score,{
        "routes":routes,
        "exact_api_matches":exact_apis,
        "trust":trust_score(doc)
    }

def excerpt(path,query,max_chars=2200):
    p=ROOT/path
    text=p.read_text(encoding="utf-8",errors="ignore")
    qtokens=tokenize(query)
    lines=text.splitlines()
    best=0
    best_score=-1
    for i,line in enumerate(lines):
        low=line.lower()
        s=sum(1 for t in qtokens if t in low)
        if s>best_score:
            best_score=s
            best=i
    start=max(0,best-5)
    chunk="\n".join(lines[start:start+35]).strip()
    if len(chunk)>max_chars:
        chunk=chunk[:max_chars]+"\n…"
    return chunk

def retrieve(query,limit=12):
    rows=[]
    for doc in INDEX["documents"]:
        score,meta=score_doc(query,doc)
        if score>0:
            rows.append((score,doc,meta))
    rows.sort(key=lambda x:(-x[0],x[1]["path"]))
    return rows[:limit]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--limit",type=int,default=12)
    p.add_argument("--json",action="store_true")
    args=p.parse_args()

    rows=retrieve(args.query,args.limit)
    if args.json:
        out=[]
        for score,doc,meta in rows:
            out.append({
                "score":round(score,3),
                "path":doc["path"],
                "title":doc["title"],
                "status":doc.get("status"),
                "verification":doc.get("verification"),
                "trust":round(meta["trust"],2)
            })
        print(json.dumps({
            "query":args.query,
            "routes":route(args.query),
            "results":out
        },indent=2,ensure_ascii=False))
    else:
        print("Routes:",", ".join(route(args.query)) or "generic")
        for score,doc,meta in rows:
            print(f"[{score:.2f}] trust={meta['trust']:.2f} {doc['path']}")
            print(" ",doc["title"])

if __name__=="__main__":
    main()
