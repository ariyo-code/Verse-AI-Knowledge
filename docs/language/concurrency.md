# Concurrence Verse

Sources :

- https://dev.epicgames.com/documentation/fortnite/debugging-and-troubleshooting-in-verse
- https://dev.epicgames.com/documentation/fortnite/verse-glossary
- https://dev.epicgames.com/documentation/fortnite/coding-device-interactions-in-verse

Dernière vérification : 2026-09-22.

## Objectif

La concurrence Verse permet d'organiser plusieurs opérations asynchrones sans transformer chaque système en boucle globale.

## Outils importants

### `sync`

Lance plusieurs expressions asynchrones et attend que toutes se terminent.

À utiliser lorsque toutes les tâches doivent finir.

### `race`

Lance plusieurs expressions et continue avec celle qui termine en premier.

Les autres branches sont annulées.

Très utile pour :

- action joueur vs timeout ;
- fin de manche vs départ d'un joueur ;
- attente de plusieurs événements exclusifs.

### `rush`

Attend le premier résultat, mais les autres expressions peuvent continuer à s'exécuter.

À utiliser seulement lorsque ce comportement est volontaire.

### `branch`

Concurrence structurée dont la durée de vie reste liée au contexte qui la contient.

### `spawn`

Lance une fonction asynchrone indépendamment de la suite immédiate du code.

Epic avertit qu'un `spawn` mal contrôlé, notamment créé continuellement dans une boucle, peut multiplier les tâches jusqu'à provoquer une erreur runtime.

## Règle de conception

Préférer la concurrence structurée lorsque la durée de vie de la tâche doit être contrôlée.

Ne pas utiliser `spawn` comme solution universelle.

Avant chaque tâche asynchrone, répondre à :

- Qui la démarre ?
- Quand doit-elle s'arrêter ?
- Que se passe-t-il si le joueur quitte ?
- Que se passe-t-il si le round se termine ?
- Peut-elle être créée plusieurs fois ?
- Existe-t-il un mécanisme d'annulation ?
