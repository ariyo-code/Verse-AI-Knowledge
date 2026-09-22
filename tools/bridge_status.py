#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project-path",required=True)
    p.add_argument("--project-name",required=True)
    p.add_argument("--scan",required=True)
    p.add_argument("--output",required=True)
    args=p.parse_args()

    scan=json.loads(Path(args.scan).read_text(encoding="utf-8"))
    files=scan.get("files",[])

    imports=sorted({
        imp
        for f in files
        for imp in f.get("imports",[])
    })

    classes=sorted({
        c
        for f in files
        for c in f.get("classes",[])
    })

    editable_count=sum(len(f.get("editable_references",[])) for f in files)
    function_count=sum(len(f.get("functions",[])) for f in files)

    status={
        "generated_at":now(),
        "project_name":args.project_name,
        "project_path":args.project_path,
        "static_scan_only":True,
        "verse_file_count":len(files),
        "class_count":len(classes),
        "function_count":function_count,
        "editable_reference_count":editable_count,
        "imports":imports,
        "classes":classes,
        "uefn_compile_verified":False,
        "runtime_verified":False,
        "multiplayer_verified":False,
        "next_steps":[
            "connect/discover UEFN MCP",
            "inspect actual Verse files",
            "compile through UEFN",
            "store exact errors in error memory",
            "runtime test",
            "multiplayer test where relevant"
        ]
    }

    Path(args.output).write_text(
        json.dumps(status,indent=2,ensure_ascii=False),
        encoding="utf-8"
    )
    print(json.dumps(status,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
