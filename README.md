<div align="center">

# Verse AI Knowledge

**Une base de connaissances pour aider une IA à écrire du Verse / UEFN sans inventer d'API.**

**V25 — Professionalization, API Expansion & Reproducible Verification**

> **Règle n°1 : Never invent a Verse API.**

</div>

## À quoi ça sert ?

Tu donnes une tâche Verse à une IA. Le dépôt l'aide à :

```text
chercher → vérifier l'API → coder → signaler les incertitudes → tester ce qui est testable
```

Si une API exacte n'est pas prouvée :

```text
TODO(API VERIFY)
```

## Utilisation la plus simple

**1.** Donne à l'IA le lien du dépôt.  
**2.** Dis-lui de lire `AI_BOOTSTRAP.md` en premier.  
**3.** Donne ta demande Verse.

Prompt public prêt à copier : `PROMPT_AI_CHAT_FR_EN.md`.

## Les 3 choses à retenir

1. **API vérifiée ≠ code compilé.**
2. **Une CI Python ≠ une compilation UEFN.**
3. **Si ce n'est pas prouvé, le dépôt doit dire `TODO(API VERIFY)`.**

## Projets privés

Le dépôt public ne publie plus les vrais profils de projets.

Il utilise **Opaque Project Recognition** : des empreintes hashées peuvent reconnaître qu'un code ressemble à une architecture protégée, sans stocker le vrai nom du projet ni son code privé.

```bash
python tools/opaque_project_match.py MonFichier.verse
```

L'IA utilise un match silencieusement pour préserver l'architecture. Si on lui demande l'identité cachée :

```text
Protected project identity is intentionally unavailable.
```

Détails : `docs/privacy/OPAQUE_PROJECT_RECOGNITION.md`.

## Commandes utiles

```bash
python -m pip install -e .
verse-ai doctor
verse-ai claim GetFortCharacter --field signature
verse-ai coverage
verse-ai validate
```

## Statut réel

```text
Repository / Python checks: disponibles via la CI
UEFN compile: NOT TESTED sauf preuve réelle
Runtime: NOT TESTED sauf preuve réelle
Multiplayer: NOT TESTED sauf preuve réelle
```

## Pour aller plus loin

- `AI_BOOTSTRAP.md` — règles principales pour l'IA
- `knowledge/ROUTING.md` — où chercher
- `docs/` — documentation détaillée
- `ROADMAP.md` — suite du projet
- `SECURITY.md` — sécurité
- `CONTRIBUTING.md` — contribuer

---

**English:** start with `README_EN.md` or `AI_BOOTSTRAP.md`.
