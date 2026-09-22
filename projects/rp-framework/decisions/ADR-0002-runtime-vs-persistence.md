# ADR-0002 — Séparer runtime et persistence

Status: accepted-for-template

## Décision

Chaque système doit déclarer explicitement :

- état runtime ;
- état persistant ;
- état dérivable/recalculable.

## Raison

Mélanger ces catégories augmente le risque de :

- données obsolètes ;
- migrations difficiles ;
- duplication ;
- incohérences après respawn/round/session.
