# V24 Evals

`evals/` contains several different evaluation layers.

They must not be confused.

## Deterministic repository checks

- `hallucination/` — policy/guardrail fixtures;
- `retrieval/` — evidence/retrieval fixtures;
- `generation/` — saved generation run scoring/comparison;
- `results/` — generated deterministic reports.

These checks do **not** prove that a model never hallucinates.

## End-to-end LLM harness

`llm/` contains provider-independent prompts and a saved-response runner.

Without explicitly supplied responses/provider integration:

```text
SKIPPED — no LLM provider or saved responses configured
```

This is not a PASS.

## UEFN

No eval in this directory automatically proves Verse compilation.

Compile/runtime/multiplayer results require real UEFN evidence.
