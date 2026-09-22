# B003-player-lifecycle — Player lifecycle service

Level: `static+compile+runtime`

## Goal

Initialiser joueurs existants + join + leave et nettoyer l'état.

## Required concepts

- `fort_playspace`
- `GetPlayers`
- `PlayerAddedEvent`
- `PlayerRemovedEvent`

## Must consider

- late join
- leave cleanup
- duplicate initialization

## Forbidden

- only handling PlayerAddedEvent

## Verification

- static-review
- uefn-compile
- runtime
