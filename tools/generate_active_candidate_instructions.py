#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
CURRENT=ROOT/"lab/current_candidate.json"
OUT=ROOT/"lab/generated/AFTER_COMPILE.txt"

if not CURRENT.exists():
    raise SystemExit("No active candidate.")

c=json.loads(CURRENT.read_text(encoding="utf-8"))

text=f"""VERSELAB - RESULTAT DE COMPILATION

Candidat actif:
{c['candidate_id']}

Source:
{c['source_path']}

Fichier stage:
{c['staged_path']}

==================================================
SI UEFN COMPILE SANS ERREUR
==================================================

Ouvre un terminal dans le dossier Verse-AI-Knowledge et execute:

python tools/lab_result.py success --evidence "UEFN Build Verse Code succeeded"

Ensuite, pour le playtest:

python tools/record_playtest.py {c['candidate_id']} --runtime --evidence "UEFN playtest passed"

==================================================
SI UEFN AFFICHE UNE ERREUR
==================================================

Copie le message EXACT.

Erreur d'API/version:

python tools/lab_result.py fail --classification api-or-version --error "COLLE ICI LE MESSAGE EXACT"

Erreur de syntaxe/langage:

python tools/lab_result.py fail --classification syntax-or-language --error "COLLE ICI LE MESSAGE EXACT"

Dependance / asset manquant:

python tools/lab_result.py blocked --classification missing-dependency --error "COLLE ICI LE MESSAGE EXACT"

Probleme de projet UEFN:

python tools/lab_result.py blocked --classification project-environment --error "COLLE ICI LE MESSAGE EXACT"

IMPORTANT:
Ne modifie pas le candidat avant d'avoir enregistre ce premier resultat.
"""
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(text,encoding="utf-8")
print(OUT)
