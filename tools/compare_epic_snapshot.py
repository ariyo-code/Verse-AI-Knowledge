#!/usr/bin/env python3
from maintenance_lib import load_json, save_json, now

def main():
    baseline=load_json("maintenance/baseline.json")
    live=load_json("maintenance/live_snapshot.json")

    report={
        "generated_at":now(),
        "status":"ok",
        "version_change":None,
        "release_change":None,
        "source_changes":[],
        "baseline_missing_fingerprints":[],
        "fetch_failures":[]
    }

    old_v=baseline.get("verse_api_version")
    new_v=live.get("verse_api_version")
    if new_v and old_v and new_v!=old_v:
        report["version_change"]={"from":old_v,"to":new_v}
        report["status"]="changes-detected"

    old_r=baseline.get("latest_release_version")
    new_r=live.get("latest_release_version")
    if new_r and old_r and new_r!=old_r:
        report["release_change"]={"from":old_r,"to":new_r}
        report["status"]="changes-detected"

    old_sources=baseline.get("source_snapshots",{})
    for sid,item in live.get("sources",{}).items():
        if not item.get("ok"):
            report["fetch_failures"].append({
                "source_id":sid,
                "error":item.get("error")
            })
            continue

        old=old_sources.get(sid,{})
        old_hash=old.get("sha256_text")
        new_hash=item.get("sha256_text")

        if not old_hash:
            report["baseline_missing_fingerprints"].append(sid)
        elif new_hash and old_hash!=new_hash:
            report["source_changes"].append({
                "source_id":sid,
                "url":item.get("url"),
                "old_sha256":old_hash,
                "new_sha256":new_hash
            })
            report["status"]="changes-detected"

    if report["fetch_failures"] and report["status"]=="ok":
        report["status"]="partial-fetch-failure"

    save_json("maintenance/change_report.json",report)
    print(report["status"])
    if report["version_change"]:
        print("Verse API:",report["version_change"])
    if report["release_change"]:
        print("Latest release:",report["release_change"])
    print("Source changes:",len(report["source_changes"]))
    print("Missing baselines:",len(report["baseline_missing_fingerprints"]))
    print("Fetch failures:",len(report["fetch_failures"]))

if __name__=="__main__":
    main()
