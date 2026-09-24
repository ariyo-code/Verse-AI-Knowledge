# Contributing

Start with `AI_BOOTSTRAP.md`, `AGENTS.md`, and `manifest.json`. Preserve the two-axis trust model and never promote exact Verse claims without evidence.

Run `python -m pip install -e ".[dev]"`, then `verse-ai validate` and `pytest` before submitting changes. Generated prompt files must be rebuilt with `python tools/build_prompts.py`.

Third-party material requires provenance and compatible redistribution terms. Do not vendor `reference-only` content.

## Contribution licensing
The repository uses the terms in `LICENSE.md`; it is not automatically an open-source license. Contribution terms must remain compatible with that license. If legal ownership/licensing of a contribution is unclear, maintainer review is required before merge; this document is not legal advice.
