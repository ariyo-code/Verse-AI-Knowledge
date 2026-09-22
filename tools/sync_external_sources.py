#!/usr/bin/env python3
"""
License-aware GitHub corpus synchronizer.

- Downloads ONLY sources marked import_mode=approved.
- Pins to the reviewed tree SHA.
- Downloads text files only.
- Preserves LICENSE / README.
- Writes provenance metadata.
- Never changes verification status of imported Verse code.
"""

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import argparse, json, hashlib, time

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "external" / "sources.json"
DEST = ROOT / "external" / "corpus"

ALLOWED_SUFFIXES = {".verse", ".md", ".txt", ".json", ".yml", ".yaml"}
ALLOWED_SPECIAL = {"LICENSE", "NOTICE", "COPYING", "README"}

def get_json(url):
    req=Request(url,headers={
        "Accept":"application/vnd.github+json",
        "User-Agent":"Verse-AI-Knowledge-External-Sync/1.0"
    })
    with urlopen(req, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))

def get_text(url):
    req=Request(url,headers={
        "User-Agent":"Verse-AI-Knowledge-External-Sync/1.0"
    })
    with urlopen(req, timeout=45) as r:
        raw=r.read()
    return raw.decode("utf-8", errors="strict")

def wanted(path):
    p=Path(path)
    if p.name in ALLOWED_SPECIAL or p.name.startswith("README"):
        return True
    return p.suffix.lower() in ALLOWED_SUFFIXES

def safe_rel(path):
    p=Path(path)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"Unsafe path: {path}")
    return p

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source", action="append", help="Optional source id; may be repeated.")
    ap.add_argument("--verse-only", action="store_true")
    ap.add_argument("--examples-only", action="store_true")
    ap.add_argument("--max-files", type=int)
    args=ap.parse_args()

    registry=json.loads(REGISTRY.read_text(encoding="utf-8"))
    approved=[x for x in registry["approved_sources"] if x.get("import_mode")=="approved"]
    if args.source:
        wanted_ids=set(args.source)
        approved=[x for x in approved if x["id"] in wanted_ids]

    DEST.mkdir(parents=True, exist_ok=True)

    for src in approved:
        repo=src["repository"]
        owner,name=repo.split("/",1)
        sha=src["reviewed_tree_sha"]
        base=DEST/src["id"]/sha
        base.mkdir(parents=True, exist_ok=True)

        tree_url=f"https://api.github.com/repos/{owner}/{name}/git/trees/{sha}?recursive=1"
        tree=get_json(tree_url)
        if tree.get("truncated"):
            raise RuntimeError(f"GitHub tree was truncated for {repo}")

        blobs=[x for x in tree.get("tree",[]) if x.get("type")=="blob" and wanted(x["path"])]
        if args.examples_only:
            blobs=[x for x in blobs if x["path"].startswith("examples/") and x["path"].endswith(".verse")]
        elif args.verse_only:
            blobs=[x for x in blobs if x["path"].endswith(".verse") or Path(x["path"]).name in ALLOWED_SPECIAL]
        if args.max_files:
            blobs=blobs[:args.max_files]

        imported=[]
        for i,item in enumerate(blobs,1):
            path=item["path"]
            rel=safe_rel(path)
            raw_url=f"https://raw.githubusercontent.com/{owner}/{name}/{sha}/{quote(path, safe='/')}"
            try:
                content=get_text(raw_url)
            except UnicodeDecodeError:
                continue

            out=base/rel
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(content, encoding="utf-8")

            imported.append({
                "path":path,
                "blob_sha":item.get("sha"),
                "size":item.get("size"),
                "local_sha256":hashlib.sha256(content.encode("utf-8")).hexdigest()
            })

            if i % 100 == 0:
                print(f"{src['id']}: {i}/{len(blobs)}")
            time.sleep(0.01)

        provenance={
            "source_id":src["id"],
            "repository":repo,
            "source_url":src["url"],
            "reviewed_tree_sha":sha,
            "license":src["license"],
            "license_file_sha":src["license_file_sha"],
            "trust":src["trust"],
            "upstream_claims":src.get("claimed_verification",{}),
            "local_verification":{
                "compiled":False,
                "runtime_tested":False,
                "multiplayer_tested":False
            },
            "imported_file_count":len(imported),
            "files":imported
        }
        (base/"PROVENANCE.json").write_text(
            json.dumps(provenance,indent=2,ensure_ascii=False),
            encoding="utf-8"
        )
        print(f"{src['id']}: imported {len(imported)} file(s) into {base}")

if __name__=="__main__":
    main()
