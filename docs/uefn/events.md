# Événements Verse / UEFN

Source :
https://dev.epicgames.com/documentation/fortnite/coding-device-interactions-in-verse

Dernière vérification : 2026-09-22.

## Deux patterns principaux

### Subscribe

Utiliser une subscription lorsqu'un handler doit réagir aux occurrences futures d'un événement.

Questions obligatoires :

- peut-on souscrire deux fois ?
- faut-il annuler / nettoyer ?
- le handler référence-t-il un joueur qui peut quitter ?
- la subscription survit-elle à un respawn ?

### Await

Certains événements peuvent être attendus avec `Await()` dans un contexte async.

Ce pattern est utile lorsqu'un flux séquentiel doit attendre un événement précis.

## Await + race

Un pattern puissant consiste à attendre plusieurs événements concurrents avec `race`.

Exemple conceptuel :

```text
race:
    attendre interaction A
    attendre interaction B
    attendre timeout
    attendre départ joueur
```

La branche gagnante détermine la suite et les autres sont annulées.

## Anti-pattern

Ne pas créer une boucle qui ajoute une nouvelle subscription à chaque itération sans retirer ou réutiliser l'ancienne.
