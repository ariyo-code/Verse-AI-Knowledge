# VerseLab Runner Agent

You are validating one external Verse candidate inside a dedicated UEFN lab.

## Mandatory order

1. Read `lab/current_candidate.json`.
2. Inspect the staged file exactly as provided.
3. Do not edit it before the first compile attempt.
4. Ask UEFN to compile Verse.
5. Capture exact compiler output.
6. Classify:
   - success
   - syntax/language
   - API/version
   - missing dependency
   - project/environment
   - unknown
7. Record the result with `tools/lab_result.py`.
8. Only after the original attempt is recorded may you propose a correction.

## Truth rules

An upstream claim that a sample compiled is historical upstream evidence.

A successful local UEFN build is local `compiled`.

A playtest is required for `verified`.

A multiplayer playtest is required for `multiplayer-verified`.
