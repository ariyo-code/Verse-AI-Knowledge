#!/usr/bin/env python3
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]
URL_RE=re.compile(r"https://dev\.epicgames\.com/[^\s\]\)\"'<>]+")
allowed={".md",".json",".py",".verse",".yml",".yaml"}

mapping={}
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in allowed:
        continue
    if "maintenance" in p.parts and p.name in {"live_snapshot.json","change_report.json","revalidation_queue.json"}:
        continue
    text=p.read_text(encoding="utf-8",errors="ignore")
    rel=str(p.relative_to(ROOT)).replace("\\","/")
    for url in set(URL_RE.findall(text)):
        url=url.rstrip(".,;")
        mapping.setdefault(url,[]).append(rel)

out={
    "generated_by":"tools/index_source_dependencies.py",
    "source_count":len(mapping),
    "sources":{
        url:sorted(files) for url,files in sorted(mapping.items())
    }
}
(ROOT/"maintenance/source_dependencies.json").write_text(
    json.dumps(out,indent=2,ensure_ascii=False),
    encoding="utf-8"
)
print(f"{len(mapping)} official source URL(s) indexed.")
