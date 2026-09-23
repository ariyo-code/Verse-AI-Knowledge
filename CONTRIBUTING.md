# Contributing

Thanks for helping improve Verse AI Knowledge.

## Core rule

Do not submit fabricated APIs or guessed signatures presented as facts.

## Evidence model

Every API/knowledge contribution should distinguish:

**Source trust** — for example `official-current`, `signature-verified`, `api-page-verified`, `community-unverified`, or `reference-only`.

**Local validation** — one of `draft`, `static-checked`, `compiled`, `verified`, or `multiplayer-verified`.

These are independent axes.

## API contributions

Include:

- exact symbol/module involved;
- source URL or provenance;
- Verse/UEFN API version when known;
- the exact fields supported by the source (presence, signature, parameters, return type, effects, events, members);
- local compile/runtime/multiplayer evidence only if it truly exists.

If an exact claim cannot be verified, use `TODO(API VERIFY)` rather than guessing.

## Never submit

- credentials, tokens, private `.env` files, or private project secrets;
- copyrighted code without permission;
- fabricated compiler output;
- code labelled `compiled` without real UEFN compile evidence;
- code labelled `verified` without relevant runtime evidence;
- code labelled `multiplayer-verified` without relevant multiplayer evidence.

## Pull requests

Keep changes focused. Explain what changed, why, evidence/provenance, API version if relevant, and the strongest **actual** validation performed.


## V24 field evidence

Do not treat a verified symbol as if every field were verified.

When contributing exact API knowledge, state which fields are supported and attach them to evidence:

```text
signature
parameters
return_type
effects
event_names
event_payloads
member_names
```

A missing field stays unknown.

Use `tools/review_api_candidate.py` and regenerate V24 derived data with:

```bash
python tools/migrate_api_catalog_v24.py
```
