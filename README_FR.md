# Verse AI Knowledge — Français

**V24 — Claim Resolution, Evidence Graph & Continuous Verification**

Verse AI Knowledge aide les agents IA à travailler avec Verse / UEFN en utilisant du retrieval, de la provenance, des preuves et des règles anti-hallucination.

> **Ne jamais inventer une API Verse.**

## Démarrage

Pour un agent capable de lire le dépôt :

```text
AI_BOOTSTRAP.md
```

Puis :

```text
ROUTING → retrieval ciblé → résolution des claims API → Evidence Pack → Claim Ledger → implémentation → provenance → validation
```

## Nouveautés V24

- résolution des claims au niveau du champ ;
- graphe de preuves API ;
- lint conservateur des claims Verse ;
- revalidation lors d’un changement de snapshot API ;
- snapshots/diffs de couverture ;
- récupération Epic sécurisée contre les redirections hors domaine ;
- marqueur visible + commentaire HTML invisible V24 ;
- harness d’evals LLM optionnel ;
- contrôles publication/secrets/liens internes.

## CLI

```bash
python -m pip install -e .
verse-ai api GetFortCharacter
verse-ai claim GetFortCharacter --field signature
verse-ai lint path/to/code.verse
verse-ai coverage
verse-ai doctor
verse-ai validate
```

Si une information exacte n’est pas suffisamment prouvée :

```text
TODO(API VERIFY)
```

## Validation

```text
draft → static-checked → compiled → verified → multiplayer-verified
```

Une validation statique ne remplace jamais une compilation UEFN.

Le contenu original suit `LICENSE.md`. Le contenu tiers conserve ses licences et sa provenance.
