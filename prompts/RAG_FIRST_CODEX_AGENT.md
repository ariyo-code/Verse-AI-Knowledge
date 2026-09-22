# RAG-First Verse / UEFN Agent

For every substantial task:

## Step 1 — Build context

Run:

```bash
python tools/prepare_codex_context.py "USER TASK"
```

Read:

- `AGENTS.md`
- `rag/generated/CODEX_CONTEXT.md`
- actual project files relevant to the task

## Step 2 — Respect trust

When two retrieved files disagree, prefer:

1. actual UEFN compiler/runtime evidence;
2. current official Epic API;
3. signature-verified;
4. api-page-verified;
5. verified repository artifacts;
6. compiled;
7. module-index-verified;
8. planned/draft.

## Step 3 — Plan

Identify:

- system owner;
- files;
- APIs;
- state;
- failure contexts;
- async lifecycle;
- player lifecycle;
- persistence;
- verification plan.

## Step 4 — Implement small slices

Do not generate a giant feature before first compile.

## Step 5 — Verify

Use UEFN MCP when available.

Store real errors in error memory.

Promote only with evidence.
