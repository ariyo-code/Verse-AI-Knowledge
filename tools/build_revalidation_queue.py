#!/usr/bin/env python3
from pathlib import Path
import json
from maintenance_lib import load_json, save_json, now

ROOT=Path(__file__).resolve().parents[1]

def source_config():
    cfg=load_json("maintenance/sources.json")
    return {x["id"]:x for x in cfg["sources"]}

def main():
    report=load_json("maintenance/change_report.json")
    deps=load_json("maintenance/source_dependencies.json")
    cfg=source_config()

    items=[]
    seen=set()

    def add(kind,source_id,url,reason,files,priority):
        key=(kind,source_id,reason)
        if key in seen:
            return
        seen.add(key)
        items.append({
            "kind":kind,
            "source_id":source_id,
            "source_url":url,
            "priority":priority,
            "reason":reason,
            "impacted_files":sorted(set(files)),
            "status":"pending",
            "required_actions":[
                "review current official source",
                "compare impacted knowledge",
                "update only confirmed differences",
                "compile/test affected Verse systems when relevant",
                "accept new baseline only after review"
            ]
        })

    # Version changes affect broad knowledge even when URLs are stable.
    if report.get("version_change"):
        add(
            "verse-api-version",
            "verse-api-root",
            cfg.get("verse-api-root",{}).get("url"),
            f"Verse API changed {report['version_change']['from']} -> {report['version_change']['to']}",
            ["manifest.json","VERSION.md","knowledge/api_catalog.json","docs/api/"],
            "critical"
        )

    if report.get("release_change"):
        add(
            "ecosystem-release",
            "uefn-whats-new",
            cfg.get("uefn-whats-new",{}).get("url"),
            f"Latest ecosystem release changed {report['release_change']['from']} -> {report['release_change']['to']}",
            ["docs/releases/","errors/deprecations.md","knowledge/api_catalog.json"],
            "critical"
        )

    depmap=deps.get("sources",{})
    for change in report.get("source_changes",[]):
        sid=change["source_id"]
        url=change["url"]
        meta=cfg.get(sid,{})
        files=depmap.get(url,[])
        add(
            "source-content",
            sid,
            url,
            "Official Epic source fingerprint changed",
            files,
            meta.get("priority","medium")
        )

    queue={
        "generated_at":now(),
        "baseline_version":load_json("maintenance/baseline.json").get("verse_api_version"),
        "detected_version":load_json("maintenance/live_snapshot.json").get("verse_api_version"),
        "items":items
    }
    save_json("maintenance/revalidation_queue.json",queue)
    print(f"Revalidation items: {len(items)}")
    for x in items:
        print(f"- [{x['priority']}] {x['reason']} ({len(x['impacted_files'])} file hints)")

if __name__=="__main__":
    main()
