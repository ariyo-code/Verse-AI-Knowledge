#!/usr/bin/env python3
from pathlib import Path
import argparse, os

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"lab/generated/verse_dir.txt"

COMMON_ROOTS=[
    Path.home()/"Documents"/"Fortnite Projects",
    Path.home()/"OneDrive"/"Documents"/"Fortnite Projects",
]

def candidates():
    seen=set()
    result=[]
    for base in COMMON_ROOTS:
        if not base.exists():
            continue
        for p in base.rglob("Verse"):
            if not p.is_dir():
                continue
            key=str(p.resolve()).lower()
            if key in seen:
                continue
            seen.add(key)
            result.append(p)
    return sorted(result,key=lambda p:str(p).lower())

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--interactive",action="store_true")
    ap.add_argument("--path")
    args=ap.parse_args()

    if args.path:
        p=Path(args.path).expanduser()
        if not p.exists() or not p.is_dir():
            raise SystemExit(f"Invalid Verse directory: {p}")
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(str(p.resolve()),encoding="utf-8")
        print(p.resolve())
        return

    found=candidates()

    if not args.interactive:
        for p in found:
            print(p)
        return

    if found:
        print("Dossiers Verse detectes:")
        for i,p in enumerate(found,1):
            print(f"  {i}. {p}")
        print("  0. Entrer le chemin manuellement")
        raw=input("Choix: ").strip()
        try:
            choice=int(raw)
        except ValueError:
            choice=-1
        if 1<=choice<=len(found):
            selected=found[choice-1]
        else:
            selected=Path(input("Chemin complet du dossier Verse: ").strip().strip('"'))
    else:
        print("Aucun dossier Verse detecte automatiquement.")
        selected=Path(input("Chemin complet du dossier Verse: ").strip().strip('"'))

    if not selected.exists() or not selected.is_dir():
        raise SystemExit(f"Dossier invalide: {selected}")

    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(str(selected.resolve()),encoding="utf-8")
    print(f"Saved: {selected.resolve()}")

if __name__=="__main__":
    main()
