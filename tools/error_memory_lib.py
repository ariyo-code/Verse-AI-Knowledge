#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, re
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
MEMORY = ROOT / "errors" / "error_memory.jsonl"

def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def normalize_message(message: str) -> str:
    s = message.strip().lower()
    s = re.sub(r"[A-Za-z]:\\[^\s:]+", "<path>", s)
    s = re.sub(r"/[^\s:]+\.verse", "<file>.verse", s)
    s = re.sub(r"\bline\s+\d+\b", "line <n>", s)
    s = re.sub(r"\bcolumn\s+\d+\b", "column <n>", s)
    s = re.sub(r":\d+:\d+", ":<line>:<column>", s)
    s = re.sub(r"\s+", " ", s)
    return s

def make_id(message: str, category: str = "unknown") -> str:
    normalized = normalize_message(message)
    digest = hashlib.sha256(f"{category}|{normalized}".encode("utf-8")).hexdigest()[:16]
    return f"err-{digest}"

def read_entries():
    if not MEMORY.exists():
        return []
    out=[]
    for i,line in enumerate(MEMORY.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception as exc:
            raise RuntimeError(f"Invalid JSONL on line {i}: {exc}")
    return out

def write_entries(entries):
    MEMORY.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(x, ensure_ascii=False, sort_keys=True) for x in entries)
    if text:
        text += "\n"
    MEMORY.write_text(text, encoding="utf-8")

def upsert(entry):
    entries = read_entries()
    for i,old in enumerate(entries):
        if old.get("id") == entry.get("id"):
            entries[i] = entry
            write_entries(entries)
            return "updated"
    entries.append(entry)
    write_entries(entries)
    return "created"
