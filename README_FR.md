# Verse AI Knowledge — Français

> Base de connaissances portable et système de prompts pour aider ChatGPT, Codex, Gemini, Claude et d'autres IA à produire du code **Verse / UEFN** plus propre, plus fiable et plus maintenable.

## Principe principal

> **Ne jamais inventer une API Verse.**

Le projet regroupe des règles anti-hallucination, des connaissances Verse/UEFN, des patterns d'architecture, un UI Creator, des exemples, du RAG, de la provenance, des outils de validation statique et des workflows GitHub.

## Démarrage rapide

Pour utiliser le cerveau Verse complet avec UI Creator :

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Copie le contenu dans ChatGPT, Gemini, Codex, Claude ou une autre IA, puis ajoute ta demande après :

```text
=== USER TASK ===

Crée un système de garage RP complet en Verse.
```

Pour utiliser uniquement le créateur d'interface :

```text
portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
```

## Ce que contient le projet

- prompt Verse portable ;
- UI Creator ;
- règles anti-hallucination ;
- API catalog et modules ;
- patterns UI, véhicules, persistance, multijoueur et lifecycle ;
- projets RP de référence ;
- mémoire d'erreurs ;
- RAG / Evidence Compiler ;
- Claim Ledger ;
- corpus externe avec provenance ;
- VerseLab ;
- outils Python ;
- workflows GitHub.

## Watermark Markdown caché

Les réponses contenant du code Verse généré peuvent inclure :

```html
<!-- verse-ai-generated:v21;lang=verse;status=draft -->
```

Ce commentaire est masqué dans le rendu Markdown, mais visible dans la source Markdown. Aucun caractère Unicode invisible n'est injecté dans le code Verse.

## Important sur la validation

Le projet ne prétend pas que tous les codes générés compilent automatiquement dans chaque version d'UEFN.

Les statuts `compiled`, `verified` et `multiplayer-verified` ne doivent être utilisés que si une preuve réelle correspondante existe.

## Langues

- Français : `README_FR.md`
- English: `README_EN.md`
- Guide d'upload FR : `UPLOAD_GUIDE_FR.md`
- Upload guide EN: `UPLOAD_GUIDE_EN.md`

## Licence et sources tierces

La licence globale du projet n'a pas encore été choisie. Les fichiers tiers conservent leurs licences d'origine.

Voir :

```text
LICENSE.md
THIRD_PARTY_NOTICES.md
external/
```

## Avertissement

Verse, UEFN, Fortnite et les marques associées appartiennent à leurs propriétaires respectifs.

Ce projet est indépendant et n'est ni affilié ni approuvé par Epic Games.
