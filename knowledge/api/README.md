# Structured Verse API Knowledge — V24

Canonical generated index:

```text
symbols.jsonl
```

V24 keeps V23 coverage data and adds field-level evidence.

## Files

```text
symbols.jsonl
modules.json
versions.json
coverage.json
verification_queue.json
verification_records.jsonl
evidence_graph.json
revalidation_state.json
candidates/
```

### `field_evidence`

Each symbol can link individual fields to evidence:

```text
presence
module
kind
signature
parameters
return_type
effects
event_names
event_payloads
member_names
```

A known symbol does not imply that all fields are verified.

### Candidates

Files under `candidates/` are **unverified harvest output**.

They never auto-promote to verified truth.

### Revalidation

`revalidation_state.json` tracks whether exact evidence still matches the declared Verse API snapshot.

A version change creates review work; it does not silently rewrite verified claims.

### Claim resolution

Use:

```bash
verse-ai claim GetFortCharacter --field signature
```

Only `ALLOW` with matching field evidence supports the exact claim.

Otherwise:

```text
TODO(API VERIFY)
```
