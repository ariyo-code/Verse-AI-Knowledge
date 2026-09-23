# End-to-end LLM evaluation harness — V24

This directory is intentionally provider-independent.

The deterministic policy suite elsewhere in the repository is **not** an end-to-end LLM benchmark.

## Default behavior

Without explicitly supplied model responses:

```bash
python evals/llm/runner.py
```

returns:

```text
SKIPPED — no LLM provider or saved responses configured
```

This is not a PASS.

## Evaluate saved responses

Create a local JSON file outside the repository, for example:

```json
{
  "provider": "example",
  "model": "example-model",
  "responses": {
    "LLM001": "..."
  }
}
```

Then run:

```bash
python evals/llm/runner.py --responses /path/to/responses.json
```

The runner performs conservative repository-grounded checks and writes a result under `evals/llm/results/`.

Do not commit provider secrets.

## UEFN

The LLM runner does not compile Verse.

Compile/runtime/multiplayer fields must come from a separate real UEFN workflow.
