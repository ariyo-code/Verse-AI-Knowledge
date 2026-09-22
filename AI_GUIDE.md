# AI Guide

## Principe

Ce dépôt est une mémoire de travail et une base de récupération de connaissances.

Il ne remplace pas le compilateur Verse.

## Boucle recommandée

```text
Demande utilisateur
      ↓
Identifier les concepts nécessaires
      ↓
Chercher docs + exemples + systèmes
      ↓
Vérifier les erreurs connues
      ↓
Écrire l'implémentation
      ↓
Compiler dans UEFN
      ↓
Récupérer les erreurs réelles
      ↓
Corriger
      ↓
Enregistrer la correction
      ↓
Promouvoir l'exemple si validé
```

## Ne pas apprendre du mauvais code

Le volume n'est pas la qualité.

Un grand dossier rempli de snippets Internet non vérifiés peut dégrader la fiabilité de l'IA.

Classer les sources :

- `official`
- `verified`
- `community-unverified`
- `deprecated`

## Recherche recommandée

Exemple de demande :

> Crée un système de véhicule avec propriétaire, clés autorisées et verrouillage.

Ordre :

1. `/systems/vehicle-system`
2. `/examples/verified`
3. `/docs/uefn`
4. `/docs/language`
5. `/errors`
6. documentation Epic actuelle

## Règle de confiance

Si l'IA n'est pas sûre : elle doit le dire.

Une incertitude explicitement signalée est préférable à une API inventée.
