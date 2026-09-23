# Verse AI Portable — V24

Recommended current portable prompt:

```text
VERSE_AI_MASTER_PROMPT_v24_WITH_UI.txt
```

It combines the established Verse/UI prompt with V24 field-level API claim rules and generated-code provenance.

## Repository-aware agents

If the agent can read the repository, prefer:

```text
AI_BOOTSTRAP.md
```

The portable prompt is mainly for assistants that cannot directly retrieve repository files.

## Compatibility

Historical prompts remain available:

```text
VERSE_AI_MASTER_PROMPT_v23_WITH_UI.txt
VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
VERSE_AI_MASTER_PROMPT.txt
```

They are compatibility artifacts, not the current repository authority.

## V24 output provenance

Generated Verse in Markdown uses:

- a visible V24 status block before code;
- a V24 HTML comment after code;
- no invisible Unicode watermark.

See `../docs/GENERATED_CODE_MARKER.md`.
