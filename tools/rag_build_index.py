#!/usr/bin/env python3
from pathlib import Path
import json,re,math,hashlib
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/"rag/config.json").read_text(encoding="utf-8"))

ALLOWED={".md",".json",".jsonl",".verse",".py",".yml",".yaml"}

def tokenize(text):
    return re.findall(r"[a-zA-Z0-9_./<>:-]+",text.lower())

def extract_title(text,path):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem

def detect_status(text):
    patterns=[
        r"\bstatus\s*:\s*`?([a-zA-Z0-9_-]+)",
        r'"status"\s*:\s*"([^"]+)"',
        r"\*\*Statut\s*:\*\*\s*`?([^`\n]+)"
    ]
    for pat in patterns:
        m=re.search(pat,text,re.I)
        if m:
            return m.group(1).strip().lower()
    return None

def detect_verification(text):
    pats=[
        r'"verification"\s*:\s*"([^"]+)"',
        r"\*\*Vérification\s*:\*\*\s*`?([^`\n]+)"
    ]
    for pat in pats:
        m=re.search(pat,text,re.I)
        if m:
            return m.group(1).strip().lower()
    return None

def detect_version(text):
    m=re.search(r"\b(?:verse_api|Verse API(?: version)?|verse api snapshot)\b[^0-9]{0,20}([0-9]{2}\.[0-9]{2})",text,re.I)
    return m.group(1) if m else None


def external_trust_for_path(path):
    parts=path.parts
    try:
        idx=parts.index("corpus")
    except ValueError:
        return None
    # external/corpus/<source-id>/<sha>/...
    if len(parts) <= idx+2:
        return None
    base=ROOT.joinpath(*parts[:idx+3])
    provenance=base/"PROVENANCE.json"
    if not provenance.exists():
        return "external-community"
    try:
        return json.loads(provenance.read_text(encoding="utf-8")).get("trust","external-community")
    except Exception:
        return "external-community"

def detect_api_symbols(text):
    # API-ish names and exact catalog identifiers are added later by lookup.
    vals=set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`",text))
    vals.update(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*(?:_device|_component|_ui|_character|_vehicle|_collection))\b",text))
    return sorted(vals)

def main():
    catalog={}
    p=ROOT/"knowledge/api_catalog.json"
    if p.exists():
        catalog=json.loads(p.read_text(encoding="utf-8")).get("entries",{})

    docs=[]
    df=Counter()

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ALLOWED:
            continue
        rel=str(path.relative_to(ROOT)).replace("\\","/")
        if rel.startswith("rag/index"):
            continue
        if any(rel.startswith(x) for x in CONFIG.get("excluded_paths",[])):
            continue

        text=path.read_text(encoding="utf-8",errors="ignore")
        tokens=tokenize(text)
        tf=Counter(tokens)
        for t in tf:
            df[t]+=1

        symbols=set(detect_api_symbols(text))
        for name in catalog.keys():
            if name in text:
                symbols.add(name)

        doc={
            "id":hashlib.sha1(rel.encode()).hexdigest()[:16],
            "path":rel,
            "title":extract_title(text,path),
            "extension":path.suffix.lower(),
            "size_chars":len(text),
            "token_count":len(tokens),
            "term_freq":dict(tf),
            "status":detect_status(text),
            "verification":external_trust_for_path(path.relative_to(ROOT)) or detect_verification(text),
            "verse_api":detect_version(text),
            "api_symbols":sorted(symbols),
            "sha256":hashlib.sha256(text.encode("utf-8")).hexdigest()
        }
        docs.append(doc)

    avgdl=sum(x["token_count"] for x in docs)/max(len(docs),1)
    index={
        "schema_version":1,
        "document_count":len(docs),
        "avg_document_length":avgdl,
        "document_frequency":dict(df),
        "documents":docs
    }

    out=ROOT/"rag/index.json"
    out.write_text(json.dumps(index,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Indexed {len(docs)} document(s).")

if __name__=="__main__":
    main()
