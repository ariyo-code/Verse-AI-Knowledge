# Live UEFN Quality Gate

Before calling a task complete:

## Static gate

- relevant API references checked;
- no unresolved suspicious API-like identifiers;
- failure contexts reviewed;
- player lifecycle reviewed;
- async lifetime reviewed;
- system ownership reviewed.

## Compile gate

UEFN compile must succeed.

## Runtime gate

For behavioral features:
- run session;
- observe expected behavior;
- inspect relevant logs.

## Multiplayer gate

Required where correctness depends on:
- multiple players;
- late join;
- disconnect;
- respawn;
- shared state.

## Promotion

Only after evidence:

```bash
python tools/promote_artifact.py path/to/artifact   --from-status draft   --to-status verified   --compiled   --runtime-tested   --evidence "UEFN compile succeeded"   --evidence "Playtest passed"
```
