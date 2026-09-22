#!/usr/bin/env python3
"""
Static Verse project scanner.

This tool does NOT compile Verse.
It only inventories files and extracts useful textual signals.
"""
from pathlib import Path
import argparse, json, re, hashlib

USING_RE = re.compile(r"^\s*using\s*\{\s*([^}]+)\s*\}", re.M)
CLASS_RE = re.compile(r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*:=\s*class(?:\([^)]*\))?")
EDITABLE_RE = re.compile(
    r"(?ms)@editable\s*(?:\n\s*)?([A-Za-z_][A-Za-z0-9_]*)\s*:\s*([A-Za-z_][A-Za-z0-9_./]*)"
)
FUNC_RE = re.compile(
    r"(?m)^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(?:<[^>]+>\s*)*\([^)]*\)\s*(?:<[^>]+>\s*)*:"
)

def scan_file(path, root):
    text=path.read_text(encoding="utf-8",errors="ignore")
    rel=str(path.relative_to(root)).replace("\\","/")
    return {
        "path":rel,
        "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "lines":len(text.splitlines()),
        "imports":sorted(set(x.strip() for x in USING_RE.findall(text))),
        "classes":sorted(set(CLASS_RE.findall(text))),
        "editable_references":[
            {"name":a,"type":b} for a,b in EDITABLE_RE.findall(text)
        ],
        "functions":sorted(set(FUNC_RE.findall(text)))
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("project_root")
    p.add_argument("--output",default="project_scan.json")
    args=p.parse_args()

    root=Path(args.project_root).resolve()
    verse=list(root.rglob("*.verse"))
    result={
        "scan_type":"static-only",
        "warning":"This report does not prove compilation or runtime correctness.",
        "project_root":str(root),
        "verse_file_count":len(verse),
        "files":[scan_file(x,root) for x in sorted(verse)]
    }

    out=Path(args.output)
    out.write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Scanned {len(verse)} Verse file(s) -> {out}")

if __name__=="__main__":
    main()
