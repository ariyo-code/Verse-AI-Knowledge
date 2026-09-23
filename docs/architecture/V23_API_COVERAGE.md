# V23 — API Coverage, Generation Reliability & Provenance

## Objective

V23 keeps the V22 architecture and concentrates on one question: **does better exact API evidence make generated Verse measurably more reliable?**

## Coverage model

A symbol can have several independently measured fields:

```text
presence → signature → parameters → return type → effects → events/members
```

Presence never proves an exact signature. A harvested page never auto-promotes a candidate to verified knowledge.

## Verification states

```text
missing   = no exact signature evidence stored
candidate = a possible signature was harvested or inherited but is not approved
verified  = the exact signature is supported by reviewed official evidence
```

Local artifact validation (`draft`, `compiled`, etc.) remains separate from API source evidence.

## Safe pipeline

```text
Official Epic page
      ↓
Harvester
      ↓
Candidate JSON
      ↓
Human/agent review against the exact page
      ↓
Verification evidence record
      ↓
Structured symbol index
      ↓
Coverage report + retrieval
      ↓
Generation benchmark
      ↓
UEFN compile/runtime evidence when available
```

## Commands

```bash
verse-ai coverage
verse-ai api-queue
python tools/harvest_epic_api.py --symbol GetFortCharacter
python tools/review_api_candidate.py GetFortCharacter --signature "..." --source-url "https://dev.epicgames.com/..."
python tools/migrate_api_catalog_v23.py
python tools/evaluate_generation_run.py path/to/run.json
python tools/compare_generation_runs.py v22-result.json v23-result.json
```

## Success criteria

V23 is not successful because the symbol count increases. It is successful if repeatable evals show fewer unsupported API claims, fewer incorrect exact signatures/effects, fewer compile corrections, and a higher first-pass UEFN compile rate when real compile evidence is available.
