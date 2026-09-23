#!/usr/bin/env python3
"""
Accept the current live snapshot as the new watcher baseline.

Run ONLY after reviewing the revalidation queue.
This changes maintenance metadata; it does not mark API cards verified.
"""
from maintenance_lib import load_json, save_json, now

def main():
    live=load_json("maintenance/live_snapshot.json")
    report=load_json("maintenance/change_report.json")
    queue=load_json("maintenance/revalidation_queue.json")

    pending=[x for x in queue.get("items",[]) if x.get("status","pending")=="pending"]
    if pending:
        raise SystemExit(
            f"Refusing baseline acceptance: {len(pending)} revalidation item(s) still pending. "
            "Resolve them and mark their queue status before accepting."
        )

    source_snapshots={}
    for sid,item in live.get("sources",{}).items():
        if item.get("ok"):
            source_snapshots[sid]={
                "url":item.get("url"),
                "sha256_text":item.get("sha256_text"),
                "etag":item.get("etag"),
                "last_modified":item.get("last_modified"),
                "fetched_at":item.get("fetched_at")
            }

    baseline={
        "schema_version":1,
        "created_at":now(),
        "state":"accepted-after-revalidation",
        "verse_api_version":live.get("verse_api_version"),
        "latest_release_version":live.get("latest_release_version"),
        "source_snapshots":source_snapshots
    }
    save_json("maintenance/baseline.json",baseline)
    print("Maintenance baseline accepted.")

if __name__=="__main__":
    main()
