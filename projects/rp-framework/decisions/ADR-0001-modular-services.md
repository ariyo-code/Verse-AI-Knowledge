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
