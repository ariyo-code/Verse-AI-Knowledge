#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re
from collections import defaultdict

ROOT=Path(__file__).resolve().parents[1]
REG=json.loads((ROOT/"external/sources.json").read_text(encoding="utf-8"))
POLICY=json.loads((ROOT/"curation/policy.json").read_text(encoding="utf-8"))
CATALOG=json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8")).get("entries",{})

DEVICE_RE=re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*_device)\b")
USING_RE=re.compile(r"^\s*using\s*\{\s*([^}]+)\s*\}",re.M)
CREATIVE_RE=re.compile(r"\bclass\s*\(\s*creative_device\s*\)")
EDITABLE_RE=re.compile(r"@editable\b")

FEATURES={
    "ui":["player_ui","canvas","stack_box","button_loud","button_regular","button_quiet","text_block","color_block","GetPlayerUI"],
    "player-lifecycle":["GetPlayers","PlayerAddedEvent","PlayerRemovedEvent"],
    "character":["GetFortCharacter","fort_character"],
    "vehicles":["vehicle_spawner_","fort_vehicle","AgentEntersVehicleEvent","AgentExitsVehicleEvent"],
    "persistence":["weak_map","Save","Load","persist"],
    "async":["spawn{","spawn {","race:","<suspends>","Await()","Sleep("],
    "events":["Subscribe(",".Await()"],
    "teams":["GetTeamCollection","fort_team_collection","AddToTeam","GetTeam["],
    "teleport":["teleporter_device","Teleport("],
}

def source_root(source_id):
    parent=ROOT/"external/corpus"/source_id
    if not parent.exists():
        raise SystemExit(
            f"External source not synchronized: {parent}\n"
            f"Run: python tools/sync_external_sources.py --source {source_id} --verse-only"
        )
    shas=[p for p in parent.iterdir() if p.is_dir()]
    if not shas:
        raise SystemExit(f"No synchronized revision under {parent}")
    # source registry pins one SHA; prefer that.
    src=next((x for x in REG["approved_sources"] if x["id"]==source_id),None)
    if src:
        pinned=parent/src["reviewed_tree_sha"]
        if pinned.exists():
            return pinned
    return sorted(shas)[-1]

def user_project_tokens():
    # Public distribution contains no private/user-provided project source.
    return set()

def category_for(path):
    parts=path.parts
    try:
        i=parts.index("examples")
        return parts[i+1] if len(parts)>i+1 else "examples"
    except ValueError:
        return "unknown"

def analyse(path,base,source_id,trust,user_tokens):
    text=path.read_text(encoding="utf-8",errors="ignore")
    rel=str(path.relative_to(base)).replace("\\","/")
    lines=text.splitlines()
    devices=sorted(set(DEVICE_RE.findall(text)))
    imports=sorted(set(x.strip() for x in USING_RE.findall(text)))

    api_symbols=sorted(name for name in CATALOG if name in text)

    features=[]
    for label,needles in FEATURES.items():
        if any(n in text for n in needles):
            features.append(label)

    relevance=[]
    for d in devices:
        if d in user_tokens:
            relevance.append(d)
    for a in api_symbols:
        if a in user_tokens:
            relevance.append(a)
    for f in features:
        if "feature:"+f in user_tokens:
            relevance.append("feature:"+f)
    relevance=sorted(set(relevance))

    score=0.0

    # Upstream compile claim is useful, but does not become local compiled.
    if trust=="external-compiler-claimed":
        score+=18
    elif trust=="external-community":
        score+=8

    if CREATIVE_RE.search(text):
        score+=10
    if EDITABLE_RE.search(text):
        score+=4

    # Prefer manageable, focused examples.
    n=len(lines)
    if 20<=n<=500:
        score+=10
    elif n<20:
        score+=3
    elif n>900:
        score-=12
    elif n>500:
        score-=4

    # Current catalog overlap.
    score+=min(len(api_symbols)*1.8,18)
    score+=min(len(devices)*1.2,12)
    score+=min(len(features)*1.5,9)

    # Optional project-context relevance.
    score+=min(len(relevance)*4.0,24)

    category=category_for(path)
    preferred=POLICY.get("preferred_categories",[])
    if category in preferred:
        score+=max(0,10-preferred.index(category))

    # Avoid overweighting suspicious/unrelated samples for RP learning.
    low=path.name.lower()
    if "aimbot" in low or "aim-bot" in low:
        score-=20

    normalized=re.sub(r"\s+","",text)
    content_hash=hashlib.sha256(normalized.encode("utf-8")).hexdigest()

    cid=hashlib.sha1(f"{source_id}|{rel}".encode()).hexdigest()[:14]

    return {
        "id":f"ext-{cid}",
        "source_id":source_id,
        "path":rel,
        "category":category,
        "score":round(score,2),
        "line_count":n,
        "devices":devices,
        "api_symbols":api_symbols,
        "imports":imports,
        "features":features,
        "project_relevance":relevance,
        "status":trust,
        "content_hash":content_hash
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",default=POLICY.get("target_source","uefncentral-examples"))
    ap.add_argument("--limit",type=int,default=POLICY.get("default_max_candidates",100))
    args=ap.parse_args()

    src=next((x for x in REG["approved_sources"] if x["id"]==args.source),None)
    if not src:
        raise SystemExit(f"Source is not approved for import: {args.source}")

    base=source_root(args.source)
    examples_root=base/"examples"
    if not examples_root.exists():
        raise SystemExit(f"Expected /examples directory missing: {examples_root}")

    user_tokens=user_project_tokens()
    rows=[
        analyse(p,base,args.source,src["trust"],user_tokens)
        for p in sorted(examples_root.rglob("*.verse"))
    ]

    # Deduplicate normalized code.
    best_by_hash={}
    for row in sorted(rows,key=lambda x:(-x["score"],x["path"])):
        best_by_hash.setdefault(row["content_hash"],row)
    unique=list(best_by_hash.values())

    # Balanced selection: first secure high-value examples for each device/category.
    selected={}
    per_device=defaultdict(int)
    per_cat=defaultdict(int)

    for row in sorted(unique,key=lambda x:(-x["score"],x["path"])):
        should_take=False

        if per_cat[row["category"]] < POLICY.get("top_per_category",10):
            should_take=True

        for d in row["devices"]:
            if per_device[d] < POLICY.get("top_per_device",5):
                should_take=True

        if row["project_relevance"]:
            should_take=True

        if should_take or len(selected)<min(20,args.limit):
            selected[row["id"]]=row
            per_cat[row["category"]]+=1
            for d in row["devices"]:
                per_device[d]+=1

        if len(selected)>=args.limit:
            break

    chosen=sorted(selected.values(),key=lambda x:(-x["score"],x["path"]))

    out={
        "schema_version":1,
        "source_id":args.source,
        "source_revision":src["reviewed_tree_sha"],
        "upstream_trust":src["trust"],
        "analysed_examples":len(rows),
        "unique_examples":len(unique),
        "selected_examples":len(chosen),
        "selection_note":"Static ranking only. UEFN recompilation required for local compiled status.",
        "examples":chosen
    }

    dest=ROOT/"curation/curated_examples.json"
    dest.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")

    report=[
        "# Curated External Examples",
        "",
        f"Source: `{args.source}`",
        f"Analysed: {len(rows)}",
        f"Unique: {len(unique)}",
        f"Selected: {len(chosen)}",
        "",
        "## Top candidates",
        ""
    ]
    for i,row in enumerate(chosen[:50],1):
        report += [
            f"### {i}. `{row['path']}`",
            "",
            f"- ID: `{row['id']}`",
            f"- Score: **{row['score']}**",
            f"- Category: `{row['category']}`",
            f"- Devices: {', '.join(row['devices']) or 'none'}",
            f"- Features: {', '.join(row['features']) or 'none'}",
            f"- Relevant to user project: {', '.join(row['project_relevance']) or 'none'}",
            ""
        ]
    (ROOT/"curation/REPORT.md").write_text("\n".join(report),encoding="utf-8")

    print(f"Analysed {len(rows)} example(s)")
    print(f"Unique {len(unique)}")
    print(f"Selected {len(chosen)}")
    print(dest)

if __name__=="__main__":
    main()
