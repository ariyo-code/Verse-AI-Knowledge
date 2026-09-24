# V25 CI fix notes

This package addresses the first GitHub Actions run of V25.

## Corrected

- `portable/current/` generated prompt artifacts are included and regenerated deterministically.
- prompt drift CI now detects untracked generated files, not only tracked-file diffs.
- Ruff/format checks are scoped to the installable V25 package (`src/verse_ai_knowledge/`) while legacy tooling is migrated progressively.
- normal documentation CI validates MkDocs without requiring GitHub Pages to be enabled.
- Pages deployment moved to a manual workflow (`pages.yml`) and requires the repository Pages source to be set to GitHub Actions first.

## Validation boundary

GitHub CI status for this corrected package is **UNKNOWN until pushed**.

UEFN compile: **NOT TESTED**  
Runtime: **NOT TESTED**  
Multiplayer: **NOT TESTED**  
Live LLM benchmark: **SKIPPED unless explicitly configured**
