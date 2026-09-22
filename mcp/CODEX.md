# Codex + UEFN MCP

Source officielle :
https://dev.epicgames.com/documentation/fortnite/uefn-mcp

## Workflow

1. Ouvrir le projet dans UEFN.
2. Activer Python Editor Scripting + UEFN MCP Toolsets.
3. Générer la configuration client depuis UEFN.
4. Démarrer Codex depuis la racine indiquée.
5. Faire découvrir les toolsets disponibles.
6. Lire `AGENTS.md`.
7. Suivre `mcp/agent-workflow.md`.

## Test de connexion

```text
Read AGENTS.md and knowledge/ROUTING.md.
Discover the UEFN MCP toolsets available to you.
List the Verse files in this project.
Do not modify anything yet.
Report whether Verse compilation and play-session tools are available.
```

## Test de compilation

```text
Read the main Verse device.
Make the smallest safe change that prints a diagnostic message in OnBegin.
Compile Verse through UEFN.
If compilation fails, show the exact error and fix only that error.
Do not start a play session until compilation succeeds.
```
