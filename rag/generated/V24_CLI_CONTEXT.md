# Verse AI Context Pack — V24

Query: create RP phone
Routes: project
Exact API matches: none
Budget: 4000 chars
Selected sources: 5

## Agent rules

- `source_trust` and `validation` are independent.
- Retrieval score is not proof of an API signature.
- Prefer exact verified API evidence over semantic/lexical similarity.
- Use `TODO(API VERIFY)` when an exact API claim cannot be verified.
- Never claim a UEFN compile/runtime/multiplayer result without real evidence.

## Retrieved context

## RP Phone
Source file: `projects/rp-framework/systems/phone-system/README.md`
Retrieval score: 28.58
Source trust: `unknown`
Local validation: `draft`

# RP Phone

Status: `planned`

Téléphone RP avec appels, messages, contacts, radio et UI par joueur.

Machine-readable manifest: `system.json`

## system
Source file: `projects/rp-framework/systems/phone-system/system.json`
Retrieval score: 24.89
Source trust: `unknown`
Local validation: `draft`

{
  "schema_version": 1,
  "id": "phone-system",
  "name": "RP Phone",
  "status": "planned",
  "purpose": "Téléphone RP avec appels, messages, contacts, radio et UI par joueur.",
  "responsibilities": [
    "contacts",
    "messages",
    "call state",
    "radio/messages audio",
    "PIN/cooldown",
    "UI lifecycle",
    "anti-duplication related integration"
  ],
  "runtime_state": [
    "open/closed UI state",
    "active call",
    "current screen",
    "temporary notification queue"
  ],
  "persistent_state": [
    "contacts if desired",
    "message history if desired",
    "phone settings",
    "PIN if project explicitly persists it"
  ],
  "dependencies": [
    "UnrealEngine.com/Temporary/UI",
    "Fortnite.com/UI",
    "Playspaces/player lifecycle"
  ],
  "related_api": [
    "player_ui",
    "GetPlayerUI",

## project
Source file: `projects/rp-framework/project.json`
Retrieval score: 21.39
Source trust: `unknown`
Local validation: `draft`

"id": "rp-framework",
  "name": "RP Framework",
  "status": "planned",
  "source": "user-defined architecture",
  "verse_api_snapshot": "42.20",
  "description": "Framework modulaire pour projets RP UEFN avec véhicules, téléphone, inventaire, staff, économie, whitelist, sessions et HUD.",
  "systems": [
    "vehicle-manager",
    "phone-system",
    "inventory-system",
    "staff-panel",
    "economy-system",
    "whitelist-system",
    "session-system",
    "hud-system"
  ],
  "architecture_rules": [
    "séparer état runtime et état persistant",
    "éviter un unique device monolithique",
    "nettoyer subscriptions et tâches liées aux joueurs",
    "tester join/leave/respawn/rounds",
    "privilégier les interfaces entre systèmes",
    "compiler après petites modifications",
    "aucune API inventée"
  ],
  "verification": {
    "compiled": false,
    "runtime_tested": false,
    "multiplayer_tested": false
  },
  "validation": "draft",
  "lifecycle_status": "planned",
  "source_trust": "unknown"
}

## dependency_graph
Source file: `projects/rp-framework/dependency_graph.json`
Retrieval score: 17.76
Source trust: `unknown`
Local validation: `draft`

"name": "Inventory System",
      "status": "planned"
    },
    {
      "id": "phone-system",
      "name": "RP Phone",
      "status": "planned"
    },
    {
      "id": "session-system",
      "name": "Session System",
      "status": "planned"
    },
    {
      "id": "staff-panel",
      "name": "Staff Panel",
      "status": "planned"
    },
    {
      "id": "vehicle-manager",
      "name": "Vehicle Manager",
      "status": "planned"
    },
    {
      "id": "whitelist-system",
      "name": "Whitelist",
      "status": "planned"
    }
  ],
  "edges": [
    {
      "from": "economy-system",
      "to": "Persistence",
      "type": "depends-on"
    },

## ADR-0001 — Modulariser les systèmes RP
Source file: `projects/rp-framework/decisions/ADR-0001-modular-services.md`
Retrieval score: 16.98
Source trust: `unknown`
Local validation: `draft`

# ADR-0001 — Modulariser les systèmes RP

Status: accepted-for-template

## Décision

Éviter un seul `creative_device` géant.

Séparer les responsabilités :

- vehicle service ;
- inventory service ;
- phone/UI ;
- staff tools ;
- economy ;
- whitelist ;
- session manager ;
- HUD.

## Pourquoi

Cela réduit :

- coupling ;
- duplication ;
- difficulté de test ;
- risque qu'une modification casse tout le projet.

## Limite

Le découpage exact doit rester adapté au projet réel et à ce qu'UEFN/Verse permet proprement.

