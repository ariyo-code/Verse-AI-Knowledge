#!/usr/bin/env python3
"""
Conservative heuristic for API review.
It does NOT prove unknown identifiers are fake.
It flags likely external API-looking identifiers that are absent from the local catalog.
"""
from pathlib import Path
import argparse,json,re

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"knowledge/api_catalog.json").read_text(encoding="utf-8"))["entries"]
KNOWN=set(catalog)

TYPE_RE=re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*(?:_device|_component|_ui|_character|_vehicle|_collection))\b")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("file")
    args=p.parse_args()

    path=Path(args.file)
    text=path.read_text(encoding="utf-8",errors="ignore")

    candidates=sorted(set(TYPE_RE.findall(text)))
    unknown=[x for x in candidates if x not in KNOWN]

    print(f"Candidates: {len(candidates)}")
    if unknown:
        print("Needs verification (not proof of hallucination):")
        for x in unknown:
            print("-",x)
    else:
        print("No catalog-missing API-like type names detected.")

if __name__=="__main__":
    main()
