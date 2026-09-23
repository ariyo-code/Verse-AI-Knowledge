#!/usr/bin/env python3
from pathlib import Path
import hashlib, html, json, re
from datetime import datetime, timezone
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]

def now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")

def load_json(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

def save_json(rel, obj):
    p=ROOT/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,ensure_ascii=False),encoding="utf-8")

def fetch(url, timeout=30):
    req=Request(url, headers={
        "User-Agent":"Verse-AI-Knowledge-Maintenance/1.0 (+official-doc-change-monitor)"
    })
    with urlopen(req, timeout=timeout) as r:
        raw=r.read()
        headers={k.lower():v for k,v in r.headers.items()}
    return raw, headers

def html_to_normalized_text(raw):
    text=raw.decode("utf-8",errors="ignore")
    # Remove scripts/styles and markup. This is a fingerprint normalizer, not a content scraper.
    text=re.sub(r"(?is)<script.*?</script>"," ",text)
    text=re.sub(r"(?is)<style.*?</style>"," ",text)
    text=re.sub(r"(?s)<[^>]+>"," ",text)
    text=html.unescape(text)
    text=re.sub(r"\s+"," ",text).strip()
    return text

def fingerprint_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_verse_api_version(text):
    patterns=[
        r"Verse API version\s*[:：]\s*([0-9]+\.[0-9]+)",
        r"Version de l.?API Verse\s*[:：]\s*([0-9]+\.[0-9]+)"
    ]
    for pat in patterns:
        m=re.search(pat,text,re.I)
        if m:
            return m.group(1)
    return None

def extract_latest_release_version(text):
    # Current release index normally starts with the newest X.YY ecosystem release.
    matches=re.findall(r"\b([0-9]{2}\.[0-9]{2})\s+Fortnite Ecosystem Updates",text,re.I)
    if not matches:
        matches=re.findall(r"\b([0-9]{2}\.[0-9]{2})\b",text)
    return matches[0] if matches else None
