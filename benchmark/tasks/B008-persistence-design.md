# B008-persistence-design — Persistent profile design

Level: `architecture`

## Goal

Concevoir état runtime vs persistent pour profil joueur.

## Required concepts

- `weak_map`
- `persistable data`
- `migration`

## Must consider

- schema changes
- new player
- existing player

## Forbidden

- persisting arbitrary runtime references

## Verification

- architecture-review
