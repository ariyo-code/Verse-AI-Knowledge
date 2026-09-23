#!/usr/bin/env python3
from pathlib import Path
import json,re,sys

ROOT=Path(__file__).resolve().parents[1]

def tokens(s):
    return re.findall(r"[a-zA-Z0-9_./-]+",s.lower())

def collect():
    files=list((ROOT/"projects").rglob("*.json"))+list((ROOT/"projects").rglob("*.md"))
    return sorted(set(files))

def main():
    if len(sys.argv)<2:
        print('Usage: python tools/search_projects.py "query"')
        raise SystemExit(2)

    q=tokens(" ".join(sys.argv[1:]))
    rows=[]
    for p in collect():
        txt=p.read_text(encoding="utf-8",errors="ignore")
        low=txt.lower()
        rel=str(p.relative_to(ROOT)).replace("\\","/")
        score=0
        for t in q:
            if t in rel.lower():
                score+=10
            score+=min(low.count(t),8)
        if score:
            rows.append((score,rel,txt[:400].replace("\n"," ")))
    rows.sort(key=lambda x:(-x[0],x[1]))
    for score,rel,excerpt in rows[:15]:
        print(f"[{score}] {rel}")
        print(" ",excerpt[:280])

if __name__=="__main__":
    main()
