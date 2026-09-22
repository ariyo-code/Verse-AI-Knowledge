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
