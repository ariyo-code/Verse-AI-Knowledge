# B004-player-ui — Per-player UI

Level: `static+compile+runtime`

## Goal

Afficher une UI par joueur et la retirer proprement.

## Required concepts

- `GetPlayerUI`
- `player_ui`
- `widget`

## Must consider

- GetPlayerUI failure
- duplicate widgets
- leave cleanup

## Forbidden

- shared mutable widget without justification

## Verification

- static-review
- uefn-compile
- runtime
