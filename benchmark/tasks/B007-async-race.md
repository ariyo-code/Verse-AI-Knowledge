# B007-async-race — Structured async race

Level: `static+compile+runtime`

## Goal

Attendre action joueur ou timeout avec concurrence structurée.

## Required concepts

- `race`
- `suspends`

## Must consider

- cancellation
- task lifetime

## Forbidden

- unbounded spawn loop

## Verification

- static-review
- uefn-compile
- runtime
