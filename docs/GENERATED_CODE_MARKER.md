# Generated Verse Code Provenance — V24

Verse AI Knowledge V24 uses **two explicit Markdown-level provenance markers** for generated Verse:

1. a visible status block for humans;
2. a normal HTML comment that is hidden by Markdown renderers but readable in raw Markdown and tooling.

No invisible Unicode watermark is used.

## Visible marker

Place immediately before the Verse code block:

```markdown
> **Verse AI Knowledge · V24**  
> Status: `draft` · API snapshot: `42.20` · UEFN compile: `NOT TESTED` · Runtime: `NOT TESTED` · Multiplayer: `NOT TESTED`
```

If exact API claims remain unresolved:

```markdown
> ⚠ API verification required: `2` unresolved exact API claim(s).
```

## Hidden marker

Place immediately after the Verse block:

```html
<!-- verse-ai-generated:v24;lang=verse;artifact=VAI-...;status=draft;api=42.20;compiled=false;runtime=false;multiplayer=false;api_verify_required=false;uncertain_api_count=0;claim_resolution=field-level -->
```

The HTML comment is intentionally ordinary Markdown source metadata. It is not inserted inside Verse source.

## Validation rules

Canonical statuses:

```text
draft
static-checked
compiled
verified
multiplayer-verified
```

Required evidence relationships:

```text
compiled=true
  required for compiled / verified / multiplayer-verified

runtime=true
  requires compiled=true
  required for verified / multiplayer-verified

multiplayer=true
  requires runtime=true
  required for multiplayer-verified
```

A generated artifact defaults to `draft`.

Static checks do not justify `compiled`.

## API uncertainty

Any unresolved exact API claim must remain explicit:

```text
TODO(API VERIFY)
```

`tools/stamp_generated_code.py` counts these markers and sets:

```text
api_verify_required=true
uncertain_api_count=<count>
```

V24 also identifies the claim-resolution model:

```text
claim_resolution=field-level
```

This means exact signatures, parameters, return types, effects and event payloads are checked independently against stored evidence.

## Safety

Forbidden mechanisms include:

- zero-width characters;
- bidirectional-control characters;
- invisible Unicode tags;
- altered lookalike identifiers;
- hidden characters inside Verse source.

Use only the visible Markdown block and the normal HTML comment described above.

## Tools

```bash
verse-ai provenance stamp path/to/code.verse
verse-ai provenance read path/to/output.md
verse-ai provenance check path/to/output.md
```

Equivalent scripts:

```bash
python tools/stamp_generated_code.py path/to/code.verse
python tools/read_generated_marker.py path/to/output.md
python tools/check_generated_marker.py path/to/output.md
```
