# Query Routing

Le moteur classe grossièrement la demande avant de rechercher.

## Routes principales

### `api`
Noms de devices, classes, fonctions, effets, modules.

### `project`
Systèmes RP, architecture existante, dépendances, state ownership.

### `error`
Message compilateur, runtime error, erreur connue.

### `ui`
UI, widgets, HUD.

### `vehicle`
Véhicules, conducteurs, sièges, ownership.

### `persistence`
weak_map, données persistantes, migration.

### `async`
race, spawn, suspends, tasks, lifetime.

### `mcp`
UEFN MCP, compile, playtest, logs.

### `maintenance`
release, version API, dépréciation, revalidation.

Une requête peut appartenir à plusieurs routes.
