# V22 Knowledge Integrity Architecture

V22 separates two questions that were previously mixed:

1. **Why should this source be trusted?** → `source_trust`
2. **What did we actually validate locally?** → `validation`

## Source trust

Canonical values are defined by `schemas/trust.schema.json` and mirrored by `manifest.json`:

- `official-current`
- `official-stale`
- `signature-verified`
- `api-page-verified`
- `community-verified`
- `community-unverified`
- `external-compiler-claimed`
- `reference-only`
- `deprecated`
- `unknown`

`source_trust` must never be inferred from local compilation status.

## Local validation

Canonical values are defined by `schemas/validation_status.schema.json`:

- `draft`
- `static-checked`
- `compiled`
- `verified`
- `multiplayer-verified`

Local validation does not make a third-party or stale source authoritative.

## Claim rule

An exact claim should be emitted only when its evidence supports the scope of that claim. In particular:

- source presence is not an exact signature;
- an upstream compile claim is not a local compile;
- static checks are not UEFN compilation;
- runtime correctness is not implied by compilation;
- multiplayer correctness requires multiplayer evidence.

## API symbol migration

`knowledge/api_catalog.json` remains for compatibility. V22 generates a progressive structured index under `knowledge/api/`.

Unknown fields stay `null` or omitted. Migration must never synthesize a signature.

For legacy catalog records whose signature existed but whose signature evidence was not classified, V22 keeps the stored text but marks `exact_signature_claim_allowed: false` until revalidated.

## Retrieval order

The default policy is:

```text
exact verified API evidence
  > current official evidence
  > verified local artifacts
  > lexical/semantic similarity
  > unverified external material
```

Optional semantic retrieval is a secondary signal and is disabled by default.

## Evidence lifecycle

```text
retrieval
  → Evidence Pack
  → Claim Ledger
  → implementation
  → static checks
  → UEFN compile (when available)
  → runtime test (when relevant)
  → multiplayer test (when relevant)
```

Promotion is evidence-driven, never confidence-driven.
