#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re

def slugify(s):
    s=re.sub(r"[^a-zA-Z0-9]+","-",s.strip()).strip("-").lower()
    return s or "project"

def main():
    p=argparse.ArgumentParser()
    p.add_argument("scan_json")
    p.add_argument("--name",required=True)
    p.add_argument("--output-dir",default="projects/discovered")
    p.add_argument("--verse-api",default="42.20")
    args=p.parse_args()

    scan=json.loads(Path(args.scan_json).read_text(encoding="utf-8"))
    pid=slugify(args.name)
    out=Path(args.output_dir)/pid
    out.mkdir(parents=True,exist_ok=True)

    imports=sorted({
        imp
        for f in scan.get("files",[])
        for imp in f.get("imports",[])
    })
    classes=sorted({
        c
        for f in scan.get("files",[])
        for c in f.get("classes",[])
    })

    project={
        "schema_version":1,
        "id":pid,
        "name":args.name,
        "status":"discovered",
        "source":"static-project-scan",
        "verse_api_snapshot":args.verse_api,
        "systems":[],
        "discovered":{
            "verse_file_count":scan.get("verse_file_count",0),
            "imports":imports,
            "classes":classes,
            "files":[x["path"] for x in scan.get("files",[])]
        },
        "verification":{
            "compiled":False,
            "runtime_tested":False,
            "multiplayer_tested":False
        },
        "warning":"Discovered means scanned, not compiled."
    }

    (out/"project.json").write_text(
        json.dumps(project,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )
    (out/"project_scan.json").write_text(
        json.dumps(scan,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )
    print(out/"project.json")

if __name__=="__main__":
    main()
