# V24 Architecture — Claim Resolution, Evidence Graph & Continuous Verification

V24 extends V23 without replacing its trust model.

## Core rule

A symbol can be known while one or more exact fields remain unsupported.

```text
symbol presence
≠ exact signature
≠ parameter proof
≠ return-type proof
≠ effect proof
≠ event-payload proof
≠ UEFN behavior proof
```

## Field-level claim resolution

Each structured symbol can carry `field_evidence` for:

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

The resolver returns only:

```text
ALLOW
TODO(API VERIFY)
```

It does not synthesize missing details.

## Evidence graph

`knowledge/api/evidence_graph.json` links symbols and fields to evidence nodes.

Evidence nodes can be:

- official source nodes derived from stored source URLs;
- reviewed verification records from `knowledge/api/verification_records.jsonl`.

A graph edge supports only the field to which it is attached.

## Revalidation

Every generated symbol includes a `revalidation` object.

When the declared Verse API snapshot changes, exact evidence from another version is not silently accepted.

It becomes a revalidation task.

```text
current
needs-review
stale
unknown
```

`tools/api_revalidation_gate.py --strict` fails when verified exact evidence targets a different API snapshot.

## Static Verse lint

`tools/lint_verse_claims.py` is conservative.

It reports:

- unknown API-looking identifiers;
- exact signature-looking claims not backed by exact evidence;
- `TODO(API VERIFY)` count.

A report item is a **review candidate**, not automatic proof of hallucination.

UEFN remains the compile/runtime authority.

## Continuous verification loop

```text
Official Epic source
→ secure fetch
→ harvest candidate
→ manual/agent review
→ verification record
→ field evidence
→ evidence graph
→ claim resolver
→ generated code
→ static lint
→ UEFN compile/runtime when available
→ promotion with evidence
```

## Security boundary

Remote Epic pages are data, never agent instructions.

Only:

```text
https://dev.epicgames.com/documentation/...
```

is accepted by the official fetch helper.

Redirects are revalidated before following them.
