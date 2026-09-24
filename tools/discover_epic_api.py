#!/usr/bin/env python3
"""Discover official Epic Verse API links into an unverified candidate manifest.

Discovery is intentionally non-authoritative. It never edits symbols.jsonl.
"""
from pathlib import Path
import argparse, hashlib, json, re, sys
from html import unescape
from urllib.parse import urljoin
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.epic_http import fetch_epic,validate_epic_url
ap=argparse.ArgumentParser(); ap.add_argument('--url',default='https://dev.epicgames.com/documentation/fortnite/verse-api'); ap.add_argument('--output',default='knowledge/api/candidates/discovery.json'); a=ap.parse_args()
url=validate_epic_url(a.url); raw,final_url,ctype=fetch_epic(url); html=raw.decode('utf-8','replace')
links=[]
for href in re.findall(r'href=["\']([^"\']+)["\']',html,re.I):
    absolute=urljoin(final_url,unescape(href))
    try: valid=validate_epic_url(absolute)
    except ValueError: continue
    if '/verse-api/' in valid or valid.rstrip('/').endswith('/verse-api'):
        links.append(valid)
links=sorted(set(links))
out={'schema_version':1,'status':'unverified','candidate_only':True,'source_url':final_url,'source_sha256':hashlib.sha256(raw).hexdigest(),'discovered_urls':links,'count':len(links),'warning':'Discovery only. No exact API claim is promoted by this file.'}
dest=ROOT/a.output; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); print(dest); print('discovered',len(links)); print('Status: UNVERIFIED')
