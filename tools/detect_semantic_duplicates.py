#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"external/corpus"

def normalized(text):
    kept=[]
    for line in text.splitlines():
        s=line.strip()
        if not s or s.startswith("#"):
            continue
        if "#" in line:
            line=line.split("#",1)[0]
        kept.append(line)
    return re.sub(r"\s+","", "\n".join(kept))

groups=defaultdict(list)
for p in sorted(BASE.rglob("*.verse")):
    h=hashlib.sha256(normalized(p.read_text(encoding="utf-8",errors="ignore")).encode()).hexdigest()
    groups[h].append(str(p.relative_to(ROOT)).replace("\\","/"))

dups=[{"normalized_sha256":h,"files":v} for h,v in groups.items() if len(v)>1]
out=ROOT/"curation/semantic_duplicates.json"
out.write_text(json.dumps({"duplicate_group_count":len(dups),"groups":dups},indent=2,ensure_ascii=False),encoding="utf-8")
print(f"Semantic duplicate groups: {len(dups)}")
for g in dups:
    print("-", " | ".join(g["files"]))
