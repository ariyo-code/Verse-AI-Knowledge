# AI Guide — V22

This repository is a retrieval and evidence system. It does not replace the Verse compiler or UEFN runtime.

Start with `AI_BOOTSTRAP.md`.

## Core workflow

```text
request
  → routing
  → targeted retrieval
  → Evidence Pack
  → Claim Ledger
  → implementation
  → static checks
  → UEFN compile/runtime/multiplayer evidence when available
```

## Confidence model

Never mix source authority with local validation.

`source_trust` answers **why the source is credible/current**. `validation` answers **what was actually tested locally**.

Canonical vocabularies live in `manifest.json`, `schemas/trust.schema.json`, and `schemas/validation_status.schema.json`.

## Exact API claims

Presence evidence does not automatically prove an exact signature. If a signature, effect, module, event, property, or other exact API detail is not supported at the required evidence level, use:

```text
TODO(API VERIFY)
```

## Source priority

Prefer, in context:

1. actual UEFN compiler/runtime evidence for local behavior;
2. actual project source for project state;
3. exact current official API evidence;
4. verified repository knowledge;
5. external examples according to provenance;
6. planned architecture;
7. model memory only as non-authoritative fallback.

A remote Epic documentation change triggers revalidation; it does not automatically rewrite verified truth.
