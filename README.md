<div align="center">

# Verse AI Knowledge

**Source-grounded Verse / UEFN knowledge, API evidence, claim resolution and reliability tooling for AI agents.**

🇫🇷 Français · 🇬🇧 English · **V24 — Claim Resolution, Evidence Graph & Continuous Verification**

> **Never invent a Verse API. / Ne jamais inventer une API Verse.**

</div>

---

## V24

V24 builds on V23 API coverage and adds **field-level claim resolution**.

A known Verse symbol is no longer treated as if every detail about it were equally verified.

```text
presence
≠ signature
≠ parameters
≠ return type
≠ effects
≠ event payload
≠ UEFN behavior
```

The current repository snapshot targets **Verse API 42.20**.

Current V24 stored coverage: **164 known structured symbols**, **12 exact signatures verified**, **24 symbols with known event names**, and **0 verified event payloads**. These figures describe repository-known evidence, not the total Epic API surface.

### Quick start

Repository-aware agents start with:

```text
AI_BOOTSTRAP.md
```

Install the local CLI:

```bash
python -m pip install -e .
```

Useful commands:

```bash
verse-ai api GetFortCharacter
verse-ai claim GetFortCharacter --field signature
verse-ai lint path/to/code.verse
verse-ai coverage
verse-ai api-queue
verse-ai doctor
verse-ai validate
```

Unknown or unsupported exact API claims remain:

```text
TODO(API VERIFY)
```

### V24 reliability pipeline

```text
Retrieve
→ Resolve API Claims
→ Verify Sources
→ Build Evidence
→ Validate Claims
→ Implement
→ Attach Provenance
→ Static Check
→ Compile in UEFN
→ Runtime Test
→ Multiplayer Test
→ Promote with Evidence
```

### API evidence graph

V24 generates:

```text
knowledge/api/evidence_graph.json
```

It links individual fields such as signatures, parameters, effects and event payloads to explicit evidence nodes.

Version changes trigger revalidation instead of silently trusting stale exact claims.

### Generated Verse provenance

Generated Verse in Markdown uses a visible block:

```markdown
> **Verse AI Knowledge · V24**  
> Status: `draft` · API snapshot: `42.20` · UEFN compile: `NOT TESTED` · Runtime: `NOT TESTED` · Multiplayer: `NOT TESTED`
```

and a normal HTML comment after the code:

```html
<!-- verse-ai-generated:v24;lang=verse;artifact=VAI-...;status=draft;api=42.20;compiled=false;runtime=false;multiplayer=false;api_verify_required=false;uncertain_api_count=0;claim_resolution=field-level -->
```

**No invisible Unicode watermark is used.**

### Coverage

Run:

```bash
verse-ai coverage
```

Coverage metrics describe **symbols currently known to this repository**. They do not claim to measure every Verse API published by Epic unless a complete official denominator is available.

### Reliability evaluation

- deterministic policy evals test repository guardrails;
- `evals/llm/` provides a provider-optional end-to-end harness;
- without configured responses/provider, LLM evals report `SKIPPED`, never `PASS`;
- UEFN compile/runtime/multiplayer metrics are populated only from real evidence.

### Validation levels

```text
draft → static-checked → compiled → verified → multiplayer-verified
```

Static CI does not equal a UEFN compile.

### Documentation

- `AI_BOOTSTRAP.md`
- `AGENTS.md`
- `docs/architecture/V24_CLAIM_RESOLUTION.md`
- `docs/GENERATED_CODE_MARKER.md`
- `knowledge/api/README.md`
- `evals/llm/README.md`
- `reports/PUBLIC_RELEASE_AUDIT_V24.md`

Original repository content is governed by `LICENSE.md`. Third-party material keeps its own license and provenance requirements.

Verse, UEFN, Fortnite, Epic Games and related marks belong to their respective owners. This project is independent and is not affiliated with, endorsed by or sponsored by Epic Games.
