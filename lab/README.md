# Verse Lab — Recompilation Program

The Verse Lab progressively converts useful external examples into locally proven knowledge.

## One-time preparation

```bash
python tools/sync_external_sources.py   --source uefncentral-examples   --verse-only

python tools/curate_external_examples.py   --source uefncentral-examples   --limit 100

python tools/build_compile_queue.py --limit 50
```

## Get next candidate

```bash
python tools/compile_queue.py next
```

## Stage it into a dedicated UEFN lab project

```bash
python tools/stage_compile_candidate.py CANDIDATE_ID   --uefn-verse-dir "C:\Path\To\Your\VerseLab\Verse"
```

The exact Verse source folder is supplied by you because UEFN project layouts can differ.

## Compile with UEFN MCP

Generate the agent prompt:

```bash
python tools/generate_compile_prompt.py CANDIDATE_ID
```

Then make a real UEFN build.

## Success

```bash
python tools/record_uefn_compile.py CANDIDATE_ID   --success   --uefn-version 42.20   --evidence "UEFN Verse build succeeded"
```

Then:

```bash
python tools/promote_compiled_candidate.py CANDIDATE_ID
```

## Failure

Record exact messages:

```bash
python tools/record_uefn_compile.py CANDIDATE_ID   --failure   --classification api-or-version   --error "EXACT COMPILER ERROR"
```

## Environment block

If the sample depends on a missing local asset/file/project setup:

```bash
python tools/record_uefn_compile.py CANDIDATE_ID   --blocked   --classification missing-dependency   --error "EXACT COMPILER ERROR"
```

That candidate is not treated as invalid Verse.
