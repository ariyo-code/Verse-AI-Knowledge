# Guide de publication GitHub — V24

## Avant le push

Depuis la racine du dépôt :

```bash
python -m pip install -e .
verse-ai validate
python tools/check_internal_paths.py
python tools/scan_secrets.py
```

Vérifie également que `LICENSE.md` et `THIRD_PARTY_NOTICES.md` sont présents.

## Commit conseillé

```text
Release V24 — Claim Resolution, Evidence Graph & Continuous Verification
```

## Après le push

Ouvre l'onglet **Actions** et vérifie que **V24 CI** est entièrement vert.

Le démarrage recommandé pour les agents est :

```text
AI_BOOTSTRAP.md
```

Les anciens Master Prompts restent uniquement des packs de compatibilité / usage portable.

Une CI verte reste une validation du dépôt. Elle ne prouve pas une compilation UEFN de tout code Verse.
