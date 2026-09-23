# GitHub publication guide — V24

## Before pushing

From the repository root:

```bash
python -m pip install -e .
verse-ai validate
python tools/check_internal_paths.py
python tools/scan_secrets.py
```

Also confirm that `LICENSE.md` and `THIRD_PARTY_NOTICES.md` are present.

## Suggested commit

```text
Release V24 — Claim Resolution, Evidence Graph & Continuous Verification
```

## After pushing

Open **Actions** and confirm that **V24 CI** is fully green.

The recommended AI entry point is:

```text
AI_BOOTSTRAP.md
```

Historical Master Prompts remain compatibility / portable packs.

Green CI validates repository checks; it does not prove arbitrary Verse compiled in UEFN.
