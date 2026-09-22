# Verse AI Knowledge

> Portable knowledge base and prompting system for generating cleaner, safer, and more maintainable **Verse / UEFN** code with ChatGPT, Codex, Gemini, Claude, and other capable LLMs.

Verse AI Knowledge is designed around one core rule:

> **Never invent a Verse API.**

The repository combines a portable master prompt, UEFN/Verse knowledge, architecture patterns, UI-generation guidance, project examples, evidence rules, and validation tooling.

## Highlights

- Portable Verse master prompt
- AI UI Creator
- Anti-hallucination API rules
- Verse lifecycle and cleanup patterns
- Multiplayer-aware architecture guidance
- Vehicle, inventory, staff panel, UI and RP patterns
- Evidence-aware context generation
- Claim Ledger
- External example provenance
- VerseLab tooling
- Static dependency analysis
- GitHub-friendly project structure

## Quick Start

If you only want to use the portable AI brain, open:

```text
portable/VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
```

Copy it into ChatGPT, Gemini, Codex, Claude, or another LLM.

Then append:

```text
=== USER TASK ===

Create a complete RP garage system in Verse.
Each player can own several vehicles.
Players can lock/unlock vehicles and give temporary keys.
Handle player leave, respawn and cleanup.
```

## UI Creator

The UI Creator is available at:

```text
portable/ui_creator/VERSE_UI_CREATOR_MASTER_PROMPT.txt
```

Supported modes include:

```text
/ui create
/ui redesign
/ui from-image
/ui component
/ui bind-event
/ui responsive
/ui refactor
```

It uses an intermediate UI specification so a model can reason about layout and state before generating Verse.

## Hidden Generated-Code Marker

Generated Markdown responses should contain a hidden provenance marker:

```html
<!-- verse-ai-generated:v21 -->
```

This marker is invisible in rendered Markdown but remains visible in the raw Markdown source.

For safety and code integrity, Verse AI Knowledge **does not use invisible Unicode characters** inside generated source code.

See:

```text
docs/GENERATED_CODE_MARKER.md
```

## Project Structure

```text
Verse-AI-Knowledge/
├── AGENTS.md
├── README.md
├── VERSION.md
├── portable/
│   ├── VERSE_AI_MASTER_PROMPT_v21_WITH_UI.txt
│   └── ui_creator/
├── knowledge/
├── docs/
├── patterns/
├── examples/
├── projects/
├── templates/
├── rag/
├── errors/
├── dependencies/
├── bridge/
├── lab/
├── tools/
└── .github/
```

## Evidence Rules

Not every source can prove the same thing.

General priority:

```text
actual UEFN compiler/runtime evidence
        ↓
actual project source
        ↓
current official API evidence
        ↓
verified local knowledge
        ↓
upstream examples
        ↓
planned architecture
        ↓
model memory
```

An upstream example must never be described as locally compiled unless local UEFN evidence exists.

## Verification Status

This repository contains tooling and static knowledge.

It does **not** claim that all generated Verse code compiles in every current UEFN version.

Models are instructed to:
- avoid inventing APIs;
- isolate uncertain integrations;
- distinguish verified signatures from API presence;
- never claim a successful compile without evidence.

## External Sources

Third-party examples remain subject to their original licenses.

See:

```text
THIRD_PARTY_NOTICES.md
external/
```

## Contributing

Contributions are welcome for:
- verified API information;
- reproducible Verse compiler errors;
- clean architecture patterns;
- UI patterns;
- multiplayer edge cases;
- verified examples.

Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## Security

Do not commit:
- Epic account credentials;
- API tokens;
- `.env` files;
- private project secrets;
- Discord bot tokens;
- database credentials.

See [SECURITY.md](SECURITY.md).

## Disclaimer

Verse, UEFN, Fortnite and related names are trademarks of their respective owners.

This project is an independent knowledge/prompting project and is not affiliated with or endorsed by Epic Games.
