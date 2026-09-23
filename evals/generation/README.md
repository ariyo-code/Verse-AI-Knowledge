# Generation Reliability Evals

Use the same `tasks.json` prompts, model/configuration and output format for V22 and V23 comparisons.

The repository does not call a model automatically. Store a run as JSON matching `schemas/generation_eval_run.schema.json`, then run:

```bash
python tools/evaluate_generation_run.py run-v23.json --output reports/run-v23-result.json
python tools/compare_generation_runs.py reports/run-v22-result.json reports/run-v23-result.json
```

Compile metrics must come from real UEFN results. Missing compile evidence stays `null`; it is never inferred from static quality.
