#!/usr/bin/env python3
from pathlib import Path
import argparse, json
from error_memory_lib import make_id, normalize_message, utc_now, upsert

def main():
    p=argparse.ArgumentParser(description="Add one REAL Verse/UEFN error to structured memory.")
    p.add_argument("--message", required=True, help="Exact compiler/runtime message.")
    p.add_argument("--category", default="compiler",
                   choices=["compiler","runtime","logic","deprecation","mcp","unknown"])
    p.add_argument("--source-type", default="verse-compiler",
                   choices=["uefn","verse-compiler","runtime-log","manual"])
    p.add_argument("--file")
    p.add_argument("--line", type=int)
    p.add_argument("--column", type=int)
    p.add_argument("--version", default="42.20")
    p.add_argument("--faulty-code")
    p.add_argument("--tags", nargs="*", default=[])
    p.add_argument("--related-api", nargs="*", default=[])
    args=p.parse_args()

    now=utc_now()
    entry={
        "id":make_id(args.message,args.category),
        "created_at":now,
        "updated_at":None,
        "status":"observed",
        "category":args.category,
        "exact_message":args.message,
        "normalized_message":normalize_message(args.message),
        "source":{
            "type":args.source_type,
            "file":args.file,
            "line":args.line,
            "column":args.column
        },
        "version":{
            "uefn_or_api":args.version,
            "project_revision":None
        },
        "faulty_code":args.faulty_code,
        "minimal_reproduction":None,
        "cause":None,
        "correction":None,
        "corrected_code":None,
        "verification":{
            "compiled":False,
            "runtime_tested":False,
            "multiplayer_tested":False,
            "evidence":None
        },
        "tags":sorted(set(args.tags)),
        "related_api":sorted(set(args.related_api)),
        "related_files":[args.file] if args.file else [],
        "notes":None
    }

    action=upsert(entry)
    print(f"{action}: {entry['id']}")
    print(json.dumps(entry,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
