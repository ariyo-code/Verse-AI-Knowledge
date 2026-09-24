<div align="center">

# Verse AI Knowledge

**Source-grounded, evidence-aware infrastructure for Verse / UEFN agents.**

**V25 — Professionalization, API Expansion & Reproducible Verification**

> **Never invent a Verse API. / Ne jamais inventer une API Verse.**

</div>

## Problem

LLMs can produce plausible Verse that uses nonexistent APIs, wrong modules, incorrect signatures/effects, or unsupported event payloads. Static confidence is not compiler evidence.

## Solution

Verse AI Knowledge combines targeted retrieval, field-level API evidence, claim resolution, provenance, project/error memory, evals and optional UEFN verification workflows.

```text
Retrieve → Resolve → Verify → Build Evidence → Validate Claims
→ Design → Implement → Static Check → Compile → Runtime → Multiplayer
→ Promote with Evidence
```

## Quick start

```bash
python -m pip install -e .
verse-ai doctor
verse-ai search "vehicle ownership"
verse-ai claim GetFortCharacter --field signature
verse-ai explain GetFortCharacter
verse-ai coverage
```

Unknown exact API:

```bash
verse-ai claim definitely_fake_api --field signature
# TODO(API VERIFY)
```

## Architecture

- `AI_BOOTSTRAP.md`: authoritative agent entry point.
- `knowledge/api/`: structured API evidence and candidates.
- `rag/`: targeted retrieval and evidence-aware ranking.
- `src/verse_ai_knowledge/`: reusable Python SDK + CLI.
- `verification/`: real validation evidence only.
- `evals/`: synthetic/retrieval/LLM evaluation data, separate from real error memory.
- `portable/current/`: generated current portable prompts.
- `portable/archive/`: compatibility/history.

## Evidence model

Source trust and local validation are independent. Symbol presence never implies an exact signature. Exact claims remain blocked unless matching field-level evidence exists.

## API coverage

Run `verse-ai coverage --json` for the current measured repository-known coverage. Coverage is **not automatically the percentage of Epic's entire Verse API surface**.

## Generated-code provenance

Generated Verse uses the current rules in `docs/GENERATED_CODE_MARKER.md`: a visible status block plus a machine-readable HTML provenance comment. No invisible Unicode is used.

## Validation boundaries

```text
Repository/Python CI: testable here
UEFN compile: NOT TESTED unless real compiler evidence exists
Runtime: NOT TESTED unless a session result exists
Multiplayer: NOT TESTED unless 2+ player evidence exists
LLM benchmark: SKIPPED unless provider/saved responses are explicitly configured
```

## CLI / SDK / MCP

`verse-ai` is the primary human/automation CLI. `KnowledgeBase` provides a Python API. `mcp/server.py` exposes a provider-neutral local knowledge-tool interface without inventing absent facts.

## Documentation

Static docs are configured with MkDocs (`mkdocs.yml`). See `docs/getting-started/`, `docs/architecture/`, `docs/security/`, the changelog and roadmap.

## Contributing / Security

Read `CONTRIBUTING.md` and `SECURITY.md`. Sensitive vulnerabilities should not be posted in public issues.

## License

Original repository content is governed by `LICENSE.md`. Third-party content retains its own terms; see `THIRD_PARTY_NOTICES.md` and `THIRD_PARTY_MANIFEST.json`.

## Disclaimer

Verse, Unreal Editor for Fortnite, Fortnite, Epic Games and related marks belong to their respective owners. This independent project is not affiliated with or endorsed by Epic Games.
