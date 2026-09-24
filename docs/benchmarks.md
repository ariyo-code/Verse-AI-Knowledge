# Benchmarks

V25 keeps separate benchmark classes:

- retrieval metrics (`Recall@1`, `Recall@5`, `Recall@10`, MRR, nDCG);
- deterministic policy guardrail evals;
- provider-neutral LLM evaluation harness;
- UEFN compile/runtime/multiplayer evidence when a real environment exists.

A policy-eval PASS is not an LLM-quality claim. An LLM benchmark without a configured provider is `SKIPPED`. UEFN results are `NOT TESTED` unless real editor/compiler evidence exists.
