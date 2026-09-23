# Verse AI Knowledge — Français

**V22 — Knowledge Integrity & Agent Reliability**

> **Ne jamais inventer une API Verse.**

Verse AI Knowledge est une base de connaissances et un ensemble d'outils pour aider une IA à produire du Verse / UEFN en s'appuyant sur des sources et des preuves explicites.

## Commencer

Un agent qui lit le dépôt doit ouvrir `AI_BOOTSTRAP.md`, puis `knowledge/ROUTING.md` et récupérer uniquement les connaissances pertinentes.

V22 sépare :

- `source_trust` : fiabilité/autorité de la source ;
- `validation` : validation réellement effectuée localement.

Si une API exacte n'est pas suffisamment vérifiée : `TODO(API VERIFY)`.

## Validation

`draft` → `static-checked` → `compiled` → `verified` → `multiplayer-verified`.

Les trois derniers niveaux exigent des preuves UEFN correspondantes. Une analyse statique n'est jamais une compilation UEFN.

## CLI

```bash
python -m pip install -e .
verse-ai doctor
verse-ai search "vehicle ownership"
verse-ai api GetFortCharacter
verse-ai validate
```

Le prompt portable V21 avec UI reste présent pour compatibilité : `portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt`.

Voir aussi `README.md`, `AGENTS.md`, `CHANGELOG.md`, `CONTRIBUTING.md` et `docs/architecture/V22_KNOWLEDGE_INTEGRITY.md`.
