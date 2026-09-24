# AI Guide — V25

Verse AI Knowledge is a retrieval, evidence, claim-resolution and evaluation system.

UEFN remains the authority for compilation and runtime behavior.

## Workflow

```text
request
→ routing
→ targeted retrieval
→ field-level API claim resolution
→ Evidence Pack
→ Claim Ledger
→ implementation
→ generated-code provenance
→ static claim lint
→ UEFN validation when available
```

## API exactness

Use `field_evidence` and the claim resolver before asserting exact API details.

```bash
verse-ai claim GetFortCharacter --field signature
```

Presence-only evidence never justifies guessing a signature.

## Evidence graph

`knowledge/api/evidence_graph.json` records which evidence supports which fields.

A version mismatch triggers revalidation.

## Generation quality

Deterministic policy evals validate repository guardrails only.

The optional `evals/llm/` harness is for end-to-end model outputs. Without configured saved responses/provider integration it reports `SKIPPED`.

No static evaluator may invent UEFN compile success.

## Coverage loop

```bash
verse-ai coverage
verse-ai api-queue
python tools/harvest_epic_api.py --symbol SYMBOL
# review official evidence
python tools/review_api_candidate.py SYMBOL --signature "..." --source-url "https://dev.epicgames.com/documentation/..."
python tools/migrate_api_catalog_v25.py
verse-ai validate
```
