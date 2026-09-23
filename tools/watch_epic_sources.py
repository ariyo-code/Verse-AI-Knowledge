#!/usr/bin/env python3
"""
Fetch official Epic pages registered in maintenance/sources.json and build a
fingerprint snapshot. This script never promotes knowledge automatically.
"""
from maintenance_lib import (
    load_json, save_json, fetch, html_to_normalized_text, fingerprint_text,
    extract_verse_api_version, extract_latest_release_version, now
)

def main():
    cfg=load_json("maintenance/sources.json")
    snapshot={
        "schema_version":1,
        "fetched_at":now(),
        "verse_api_version":None,
        "latest_release_version":None,
        "sources":{}
    }

    for src in cfg["sources"]:
        if not src.get("watch",True):
            continue
        sid=src["id"]
        try:
            raw,headers=fetch(src["url"])
            text=html_to_normalized_text(raw)
            item={
                "id":sid,
                "url":src["url"],
                "ok":True,
                "sha256_text":fingerprint_text(text),
                "etag":headers.get("etag"),
                "last_modified":headers.get("last-modified"),
                "fetched_at":snapshot["fetched_at"],
                "text_length":len(text)
            }

            for extractor in src.get("extractors",[]):
                if extractor=="verse_api_version":
                    item["verse_api_version"]=extract_verse_api_version(text)
                    if item["verse_api_version"]:
                        snapshot["verse_api_version"]=item["verse_api_version"]
                elif extractor=="latest_release_version":
                    item["latest_release_version"]=extract_latest_release_version(text)
                    if item["latest_release_version"]:
                        snapshot["latest_release_version"]=item["latest_release_version"]

            snapshot["sources"][sid]=item
            print(f"OK {sid}")
        except Exception as exc:
            snapshot["sources"][sid]={
                "id":sid,
                "url":src["url"],
                "ok":False,
                "error":str(exc),
                "fetched_at":snapshot["fetched_at"]
            }
            print(f"ERROR {sid}: {exc}")

    save_json("maintenance/live_snapshot.json",snapshot)
    print("maintenance/live_snapshot.json")

if __name__=="__main__":
    main()
