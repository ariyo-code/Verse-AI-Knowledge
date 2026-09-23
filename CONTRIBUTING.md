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
- the scope actually supported by the source (presence vs exact signature);
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
