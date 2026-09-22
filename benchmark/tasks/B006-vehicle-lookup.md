# B006-vehicle-lookup — Find player's vehicle

Level: `static+compile`

## Goal

Obtenir le véhicule d'un agent via son fort_character.

## Required concepts

- `GetFortCharacter`
- `GetVehicle`
- `fort_vehicle`

## Must consider

- both conversions can fail
- player respawn

## Forbidden

- assuming every character is in vehicle

## Verification

- static-review
- uefn-compile
