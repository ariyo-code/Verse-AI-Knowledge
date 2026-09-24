# Installation V25 — FIXED v2

Cette archive corrige les échecs observés sur la CI GitHub du commit V25 initial.

## Corrections principales

- `portable/current/` est présent et doit être versionné.
- `.gitignore` ré-inclut explicitement `portable/current/**`.
- le package `src/verse_ai_knowledge/` a été nettoyé pour les erreurs Ruff réellement observées (`E401`, `E701`, `E702`, `F401`, `I001`).
- le doublon V25 du `CHANGELOG.md` a été supprimé.
- le workflow Docs reste séparé du déploiement GitHub Pages.

## Installation recommandée

1. Fais une sauvegarde de ton dépôt local.
2. Garde uniquement le dossier caché `.git` de ton dépôt local actuel.
3. Remplace les autres fichiers par le contenu de cette archive.
4. Vérifie que `.gitignore` a bien été remplacé.
5. Dans GitHub Desktop, vérifie que les fichiers suivants apparaissent bien dans les changements :

```text
portable/current/VERSE_AI_MASTER_PROMPT.txt
portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt
portable/current/TASK_TEMPLATE.txt
```

6. Commit puis push.

Commit conseillé :

```text
fix: stabilize V25 CI and track canonical portable prompts
```

## Limites de validation

```text
UEFN compile: NOT TESTED
Runtime: NOT TESTED
Multiplayer: NOT TESTED
LLM live benchmark: SKIPPED unless explicitly configured
```
