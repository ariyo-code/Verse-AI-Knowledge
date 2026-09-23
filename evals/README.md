# V22 Evals

`evals/` contains deterministic policy/retrieval evaluations. These tests do not pretend to measure a model unless a model is actually invoked.

- `hallucination/` — anti-hallucination guard fixtures.
- `retrieval/` — evidence/retrieval fixtures.
- `results/` — generated reports (normally not authoritative evidence).

A passing policy eval is **not** a UEFN compile.
