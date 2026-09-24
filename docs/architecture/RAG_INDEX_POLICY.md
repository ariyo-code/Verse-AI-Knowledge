# RAG index policy — V25

`rag/index.json` remains versioned because it is small enough for this repository, deterministic from tracked source files, and useful for offline agents immediately after checkout.

V25 excludes evaluation corpora, reports, tests, tooling, GitHub metadata, archived prompts and generated context from retrieval. This reduces self-retrieval and benchmark leakage.

The index must be reproducible with:

```bash
python tools/rag_build_index.py
```

A retrieval score is relevance, not evidence. Exact API claims still require field-level evidence and claim resolution.
