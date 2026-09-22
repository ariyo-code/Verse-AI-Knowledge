# Debugging Verse

Source :
https://dev.epicgames.com/documentation/fortnite/debugging-and-troubleshooting-in-verse

Dernière vérification : 2026-09-22.

## Deux catégories

### Erreur de compilation / analyse

Le langage ou le compilateur détecte une incohérence avant exécution.

À stocker dans :

`errors/compiler-errors.md`

### Erreur runtime / logique

Le code compile mais peut :

- provoquer une runtime error ;
- s'exécuter dans le mauvais ordre ;
- produire une logique incorrecte ;
- créer trop de tâches asynchrones ;
- causer des problèmes de timing.

À stocker dans :

`errors/runtime-errors.md`

## Workflow de diagnostic

1. Réduire le problème à une reproduction minimale.
2. Conserver le message exact.
3. Identifier la première hypothèse testable.
4. Modifier une chose à la fois.
5. Recompiler.
6. Tester en session.
7. Tester avec plusieurs joueurs si pertinent.
8. Enregistrer la cause confirmée et la correction.

## Important

Une runtime error peut stopper l'exécution Verse restante.

L'IA doit donc traiter les risques runtime comme des erreurs graves, même si le code compile.
