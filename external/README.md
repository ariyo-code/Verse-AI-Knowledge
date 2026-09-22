# External Verse Corpus

This directory is for **third-party public Verse sources**.

## Important distinction

External code is never equivalent to locally verified knowledge.

Trust examples:

- `external-compiler-claimed`
- `external-community`
- `reference-only`

Even when an upstream repository says its files compile, this repository records that as an **upstream claim** until we reproduce the compilation ourselves.

## Approved imports

Current approved, license-verified sources:

- `uefncentral/uefn-verse-examples` — MIT
- `OsirionGG/Verse-Samples` — reference-only for now because its LICENSE file and README disagree on the license
- `NeurealUEFN/Verse` — MIT

Run:

```bash
python tools/sync_external_sources.py
```

This will download approved text sources from their reviewed commit SHA, preserve LICENSE/README, and write provenance metadata.

## Not vendored

Repos with unverified repository licenses, incompatible policy, or mixed attribution remain `reference-only`.

See `external/sources.json`.
