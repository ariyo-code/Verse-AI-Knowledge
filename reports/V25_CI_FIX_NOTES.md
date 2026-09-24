# V25 CI stabilization notes

## What the latest GitHub run actually showed

Latest checked `main` HEAD before this candidate:

```text
80b8140ee718aa5aa390ac03f9cf73aae60b7973
```

Working checks on that HEAD:

- `lint-types-package` — PASS
- `retrieval-policy` — PASS
- Docs — PASS
- CodeQL — PASS

Failing jobs:

- `integrity`
- `prompts-generated`
- `schemas-tests`
- `security`
- `preflight`

The logs point to one shared root cause: the canonical `portable/current/` artifacts were absent from the Git commit.

## Candidate correction

This package contains and validates:

```text
portable/current/VERSE_AI_MASTER_PROMPT.txt
portable/current/VERSE_AI_MASTER_PROMPT_WITH_UI.txt
portable/current/TASK_TEMPLATE.txt
```

It also contains the generated public prompt:

```text
PROMPT_AI_CHAT_FR_EN.md
```

`tools/build_prompts.py` was run twice against the candidate and the hashes remained identical, confirming deterministic generation in this environment.

The current `.gitignore` allows the V25 canonical portable prompt files to be versioned.

## Local candidate validation

Executed successfully:

```text
V25 integrity
repository integrity
verification evidence
API revalidation gate
pytest 13/13
Epic URL security tests
internal path validation
secret scan
legacy RAG benchmark 8/8
RAG metrics V25
Evidence benchmark 3/3
anti-hallucination policy 14/14
verse-ai doctor
verse-ai validate
Python compileall
prompt determinism
```

GitHub already confirmed on the current main branch that `ruff`, `mypy`, and `python -m build` pass in `lint-types-package`.

## Not claimed

- UEFN compile: NOT TESTED
- Runtime: NOT TESTED
- Multiplayer: NOT TESTED
- Live LLM benchmark: SKIPPED
- Candidate GitHub V25 CI: UNKNOWN until pushed
