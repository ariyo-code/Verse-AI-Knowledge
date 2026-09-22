# Verse AI Context Pack

Query: Create a vehicle ownership system with authorized keys and multiplayer cleanup
Routes: project, vehicle
Exact API matches: none
Budget: 12000 chars
Selected sources: 12

## Agent rules

- Use this context as retrieval evidence, not as proof of compilation.
- Prefer higher-trust sources when claims conflict.
- Verify uncertain/current APIs against official Epic documentation.
- If UEFN MCP is available, compile after meaningful changes.
- Never claim `verified` without real evidence.

## Retrieved context

## system
Source file: `projects/rp-framework/systems/vehicle-manager/system.json`
Retrieval score: 45.82
Trust: 0.40

"name": "Vehicle Manager",
  "status": "planned",
  "purpose": "Gestion de propriété, autorisations, verrouillage et contrôle des véhicules RP.",
  "responsibilities": [
    "owner par véhicule",
    "authorized keys",
    "locked/unlocked state",
    "blocked players",
    "eject / remove agent",
    "teleport/reset vehicle state",
    "cleanup player lifecycle"
  ],
  "runtime_state": [
    "vehicle owner mapping",
    "authorized players per vehicle",
    "lock state",
    "blocked players",
    "active vehicle references"
  ],
  "persistent_state": [
    "ownership only if explicitly required by project design",
    "authorized keys only if intended to survive sessions"
  ],
  "dependencies": [
    "Fortnite.com/Vehicles",
    "Fortnite.com/Characters",
    "Fortnite.com/Playspaces"
  ],
  "related_api": [
    "fort_vehicle",
    "GetVehicle",
    "fort_vehicle.GetDrivers",
    "fort_vehicle.GetSeats",
    "GetFortCharacter"
  ],

## Vehicle Manager
Source file: `projects/rp-framework/systems/vehicle-manager/README.md`
Retrieval score: 24.61
Trust: 0.40

# Vehicle Manager

Status: `planned`

Gestion de propriété, autorisations, verrouillage et contrôle des véhicules RP.

Machine-readable manifest: `system.json`

## Verse AI Knowledge
Source file: `README.md`
Retrieval score: 24.53
Trust: 0.50

```bash
python tools/rag_build_index.py

python tools/rag_query.py   "vehicle owner authorized keys"

python tools/rag_context_pack.py   "Create a multiplayer-safe vehicle ownership system"

python tools/prepare_codex_context.py   "Create a multiplayer-safe vehicle ownership system"
```

The ranker combines lexical relevance, exact API matches, routing, project/error knowledge, trust, verification status and API freshness.

It deliberately uses a bounded context budget rather than dumping the entire repository into the model.

## retrieval_benchmark
Source file: `rag/retrieval_benchmark.json`
Retrieval score: 21.44
Trust: 0.50

"docs/language/failure-and-effects.md"
      ]
    },
    {
      "id": "R003",
      "query": "vehicle owner authorized keys locked blocked players",
      "must_include_any": [
        "projects/rp-framework/systems/vehicle-manager/system.json"
      ]
    },
    {
      "id": "R004",
      "query": "UEFN compiler error memory exact message",
      "must_include_any": [
        "mcp/ERROR_FEEDBACK_LOOP.md",
        "errors/README.md"
      ]
    },
    {
      "id": "R005",
      "query": "player ui canvas widget leave cleanup",
      "must_include_any": [
        "docs/ui/CURRENT_UI_API.md",
        "docs/patterns/ui-lifecycle.md"
      ]
    },
    {
      "id": "R006",
      "query": "Epic update revalidation version API maintenance",
      "must_include_any": [
        "maintenance/README.md",
        "prompts/MAINTENANCE_AGENT.md"
      ]
    },
    {

## Verse Engineering Orchestrator
Source file: `prompts/VERSE_ENGINEERING_ORCHESTRATOR.md`
Retrieval score: 20.65
Trust: 0.50

Do not code yet.

## 2. Planner

Produce:
- affected systems;
- state ownership;
- files;
- APIs;
- failure/async/lifecycle concerns;
- verification plan.

## 3. Implementer

Make the smallest coherent change.

Generated code begins as `draft`.

## 4. Verifier

Check:
- catalog/API support;
- failure/effects;
- project ownership;
- error memory;
- compile result;
- runtime result;
- multiplayer result when relevant.

## Loop

```text
retrieve
→ plan
→ implement small slice

## ADR-0003 — Player lifecycle obligatoire
Source file: `projects/rp-framework/decisions/ADR-0003-player-lifecycle.md`
Retrieval score: 20.20
Trust: 0.50

- initialisation des joueurs déjà présents ;
- join ;
- leave ;
- respawn si pertinent ;
- cleanup subscriptions ;
- cleanup async tasks ;
- cleanup UI.

Un système qui ignore le départ joueur n'est pas considéré terminé.

## Verse knowledge change
Source file: `.github/PULL_REQUEST_TEMPLATE.md`
Retrieval score: 19.74
Trust: 0.50

## Verification

- API / UEFN version:
- Compiled:
- Behavior tested:
- Multiplayer tested:
- Official source checked:

## Notes

Explain assumptions and remaining uncertainty.

Do not mark generated code as verified without a real UEFN test.

## Vehicle System
Source file: `systems/vehicle-system/README.md`
Retrieval score: 19.34
Trust: 0.40

# Vehicle System

Status: planned

Objectifs possibles :

- propriétaire ;
- clés autorisées ;
- verrouillage ;
- liste de joueurs bloqués ;
- expulsion ;
- téléportation / reset ;
- gestion du départ du propriétaire ;
- nettoyage de l'état ;
- comportement multijoueur.

Ajouter ici uniquement du code testé ou clairement marqué `draft`.

## B010-modular-system — Design modular RP system
Source file: `benchmark/tasks/B010-modular-system.md`
Retrieval score: 19.05
Trust: 0.50

# B010-modular-system — Design modular RP system

Level: `architecture+runtime`

## Goal

Ajouter une fonctionnalité RP sans créer un second propriétaire du même état.

## Required concepts

- `project memory`
- `system ownership`
- `interfaces`

## Must consider

- dependencies
- runtime state
- persistent state
- player lifecycle

## Forbidden

- monolithic god device
- duplicate state ownership

## Verification

- project-memory-review
- uefn-compile
- runtime

## Sync Project Memory with UEFN
Source file: `mcp/PROJECT_SYNC.md`
Retrieval score: 18.71
Trust: 0.50

# Sync Project Memory with UEFN

## Initial discovery

1. Read actual Verse files through MCP or local project folder.
2. Run static scan if filesystem access exists:

```bash
python tools/scan_verse_project.py /path/to/project --output project_scan.json
```

3. Generate a discovered project profile:

```bash
python tools/create_project_profile.py project_scan.json --name "My UEFN Project"
```

4. Compare discovered code with planned manifests.
5. Update system manifests only after confirming the real architecture.

## During development

After a meaningful system change:

- update system file list;
- update dependencies;
- update public interfaces;
- update runtime/persistent state;
- update ADR if the architectural decision changed;
- compile;
- update verification status only with evidence.

## Never

Do not let the project memory silently overwrite the actual UEFN project.

## Live UEFN Quality Gate
Source file: `mcp/QUALITY_GATE.md`
Retrieval score: 18.63
Trust: 0.50

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

## HUD / UI System
Source file: `projects/rp-framework/systems/hud-system/README.md`
Retrieval score: 18.31
Trust: 0.40

Status: `planned`

HUD RP et composants UI réutilisables.

Machine-readable manifest: `system.json`

