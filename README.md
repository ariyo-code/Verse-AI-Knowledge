<div align="center">

# Verse AI Knowledge

**Source-grounded knowledge and tooling for Verse / UEFN agents.**

🇫🇷 Français · 🇬🇧 English · **V22 — Knowledge Integrity & Agent Reliability**

> **Never invent a Verse API. / Ne jamais inventer une API Verse.**

</div>

---

## 🇫🇷 Français

### Qu'est-ce que c'est ?

Verse AI Knowledge aide des assistants comme ChatGPT, Codex, Claude ou Gemini à travailler sur **Verse / UEFN** avec des sources, de la provenance, du retrieval, des garde-fous et des preuves de validation.

Le dépôt ne remplace pas UEFN et ne garantit pas qu'un code généré compile.

### Démarrage rapide

Pour un agent qui peut lire le dépôt, commence par :

```text
AI_BOOTSTRAP.md
```

Puis l'agent suit :

```text
AI_BOOTSTRAP → ROUTING → retrieval ciblé → Evidence Pack → Claim Ledger → implémentation → validation UEFN si disponible
```

Pour le pack portable historique Verse + UI, voir :

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Il reste disponible pour compatibilité ; **V22 concerne principalement l'intégrité de la base et la fiabilité de l'agent**.

### Comment le grounding fonctionne

V22 sépare deux axes :

- **`source_trust`** : qualité / autorité / fraîcheur de la source ;
- **`validation`** : ce qui a réellement été validé localement.

Un document officiel ne devient pas « compilé » automatiquement, et un code compilé ne rend pas sa source officielle.

Si une API ou une signature exacte n'est pas suffisamment vérifiée :

```text
TODO(API VERIFY)
```

### Capacités principales

- index API et modules Verse ;
- base de symboles structurée progressive ;
- RAG lexical/hybride explicable ;
- Evidence Packs et Claim Ledger ;
- mémoire d'erreurs réelles ;
- mémoire de projets/systèmes ;
- VerseLab et preuves de compilation ;
- UI Creator ;
- evals anti-hallucination ;
- veille des changements Epic avec revalidation humaine ;
- CLI unifié `verse-ai`.

### CLI

```bash
python -m pip install -e .
verse-ai search "vehicle ownership"
verse-ai context "create RP phone"
verse-ai api GetFortCharacter
verse-ai errors "compiler error"
verse-ai doctor
verse-ai validate
```

Les anciens scripts `tools/*.py` restent disponibles pour compatibilité.

### Validation

```text
draft → static-checked → compiled → verified → multiplayer-verified
```

`compiled`, `verified` et `multiplayer-verified` nécessitent de vraies preuves correspondantes. Une validation statique ne remplace jamais une compilation UEFN.

---

## 🇬🇧 English

### What is it?

Verse AI Knowledge helps AI assistants work with **Verse / UEFN** using source-aware retrieval, provenance, validation boundaries, and anti-hallucination guards.

The repository does not replace UEFN and does not guarantee that generated code compiles.

### Quick start

Repository-aware agents should start with:

```text
AI_BOOTSTRAP.md
```

The expected flow is:

```text
AI_BOOTSTRAP → ROUTING → targeted retrieval → Evidence Pack → Claim Ledger → implementation → UEFN validation when available
```

The historical portable Verse + UI prompt remains available at:

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

### Grounding model

V22 separates:

- **`source_trust`** — authority/currentness of the source;
- **`validation`** — what was actually validated locally.

If an exact API or signature cannot be supported:

```text
TODO(API VERIFY)
```

### Key capabilities

- Verse API/module knowledge;
- progressive structured symbol index;
- explainable local hybrid RAG;
- Evidence Packs and Claim Ledger;
- real-error memory;
- project/system memory;
- VerseLab and compile evidence workflows;
- UI Creator;
- anti-hallucination evals;
- safe Epic documentation revalidation;
- unified `verse-ai` CLI.

### Documentation

- `AI_BOOTSTRAP.md` — AI entry point
- `AGENTS.md` — complete agent rules
- `docs/architecture/V22_KNOWLEDGE_INTEGRITY.md` — trust/validation architecture
- `docs/MIGRATION_V21_TO_V22.md` — migration notes
- `CONTRIBUTING.md` — evidence requirements
- `SECURITY.md` — security policy

### License

Original repository content is governed by `LICENSE.md`. Third-party material keeps its own license and attribution requirements; see `THIRD_PARTY_NOTICES.md` and provenance files.

### Disclaimer

Verse, Unreal Editor for Fortnite, Fortnite, Epic Games and related marks belong to their respective owners. This is an independent project and is not affiliated with, endorsed by or sponsored by Epic Games.
