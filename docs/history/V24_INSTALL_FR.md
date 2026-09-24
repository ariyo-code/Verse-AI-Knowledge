# Installer V24 manuellement

Cette archive contient le dépôt complet V24.

## Méthode recommandée

1. Fais une sauvegarde de ton dossier local actuel.
2. Garde le dossier caché `.git` de ton dépôt local.
3. Remplace le reste du contenu par les fichiers de cette archive.
4. Ouvre un terminal dans le dépôt.
5. Lance :

```bash
python -m pip install -e .
python tools/migrate_api_catalog_v24.py
verse-ai validate
```

6. Vérifie ensuite :

```bash
python tools/preflight.py
python tools/rag_benchmark.py
python tools/run_evidence_benchmark.py
python tools/run_hallucination_evals.py
python evals/llm/runner.py
```

Le runner LLM doit afficher `SKIPPED` si aucune réponse/provider n'est configuré. C'est normal.

## Commit conseillé

```text
Release V24 — Claim Resolution, Evidence Graph & Continuous Verification
```

## Important

Une CI verte ne signifie pas que tout code Verse a été compilé dans UEFN.

Le statut de release reste honnête :

```text
UEFN compile status: NOT TESTED
```
