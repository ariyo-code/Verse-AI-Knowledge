#!/usr/bin/env python3
"""
Conservative log extractor.

It does NOT diagnose errors.
It only extracts candidate error lines from a real log and prepares JSON records.
"""
from pathlib import Path
import argparse, re, json
from error_memory_lib import make_id, normalize_message, utc_now

PATTERNS = [
    re.compile(r".*\berror\b.*", re.I),
    re.compile(r".*\bfatal\b.*", re.I),
    re.compile(r".*\bexception\b.*", re.I),
]

def is_candidate(line):
    s=line.strip()
    if not s:
        return False
    return any(p.match(s) for p in PATTERNS)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("logfile")
    p.add_argument("--version",default="42.20")
    p.add_argument("--output",default="errors/log_candidates.json")
    args=p.parse_args()

    path=Path(args.logfile)
    lines=path.read_text(encoding="utf-8",errors="ignore").splitlines()

    seen=set()
    out=[]
    for idx,line in enumerate(lines, start=1):
        if not is_candidate(line):
            continue
        norm=normalize_message(line)
        if norm in seen:
            continue
        seen.add(norm)
        out.append({
            "id":make_id(line,"unknown"),
            "created_at":utc_now(),
            "status":"observed",
            "category":"unknown",
            "exact_message":line.strip(),
            "normalized_message":norm,
            "source":{"type":"runtime-log","file":str(path),"line":idx,"column":None},
            "version":{"uefn_or_api":args.version,"project_revision":None},
            "verification":{"compiled":False,"runtime_tested":False,"multiplayer_tested":False,"evidence":None},
            "tags":["log-candidate"],
            "related_api":[],
            "related_files":[],
            "notes":"Candidate only. Human/agent must classify and diagnose from real project context."
        })

    output=Path(args.output)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Extracted {len(out)} candidate(s) to {output}")

if __name__=="__main__":
    main()
