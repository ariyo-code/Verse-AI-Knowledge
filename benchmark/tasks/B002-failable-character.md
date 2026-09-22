# B002-failable-character — Safely obtain fort_character

Level: `static+compile`

## Goal

Obtenir le fort_character d'un agent sans ignorer le caractère faillible de GetFortCharacter.

## Required concepts

- `GetFortCharacter`
- `decides`
- `failure context`

## Must consider

- agent without valid character
- respawn

## Forbidden

- treating GetFortCharacter as guaranteed

## Verification

- static-review
- uefn-compile
