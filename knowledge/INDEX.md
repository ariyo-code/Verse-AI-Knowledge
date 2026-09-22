# Knowledge Index

Index principal que l'IA doit consulter avant de coder.

## Langage Verse

- `docs/language/style.md` — conventions de style officielles
- `docs/language/failure-and-effects.md` — failure contexts, `<decides>`, `<transacts>`
- `docs/language/concurrency.md` — `sync`, `race`, `rush`, `branch`, `spawn`
- `docs/language/reliability-rules.md` — règles anti-hallucination et validation

## UEFN

- `docs/uefn/creative-devices.md` — `creative_device`, lifecycle, transforms
- `docs/uefn/characters.md` — `agent` / `fort_character`
- `docs/uefn/persistence.md` — données persistantes
- `docs/uefn/events.md` — Subscribe / Await et durée de vie
- `docs/uefn/debugging.md` — runtime errors, diagnostic
- `docs/uefn/api-versioning.md` — version actuelle et migrations

## Architecture

- `docs/architecture/multiplayer.md`
- `docs/architecture/state-management.md`
- `docs/architecture/async-lifetime.md`
- `docs/architecture/system-design.md`

## Erreurs

- `errors/compiler-errors.md`
- `errors/runtime-errors.md`
- `errors/deprecations.md`

## Systèmes

- `systems/vehicle-system/`
- `systems/inventory-system/`
- `systems/staff-panel/`

## Prompts agent

- `prompts/VERSE_AGENT_SYSTEM.md`
- `prompts/BUILD_SYSTEM_PROMPT.md`
- `prompts/REVIEW_VERSE_PROMPT.md`
- `prompts/COMPILER_FEEDBACK_PROMPT.md`

## Règle

Un agent ne doit pas répondre à partir de sa seule mémoire lorsque l'information peut être récupérée dans ce dépôt ou dans la documentation Epic actuelle.
