# Style Verse

Source principale :
https://dev.epicgames.com/documentation/fortnite/verse-code-style-guide-in-unreal-editor-for-fortnite

Dernière vérification : 2026-09-22.

## Conventions importantes

Epic recommande un style cohérent et lisible.

### Indentation

Utiliser quatre espaces et éviter les tabulations.

### Nommage

Quelques conventions utiles de la documentation Epic :

- `IsX` pour une valeur logique qui représente une question ;
- `OnX` pour un handler ou une fonction appelée par un framework ;
- `SubscribeX` pour une fonction chargée de relier des événements.

### Événements

Les événements devraient avoir un nom clair terminant généralement par `Event`.

Les fonctions qui les traitent devraient utiliser un nom de type `OnSomething`.

### Fonctions suspendues

Ne pas ajouter automatiquement `Async` au nom d'une fonction simplement parce qu'elle utilise `<suspends>`.

Le préfixe `Await` peut être utile lorsque le but principal de la fonction est réellement d'attendre un événement.

### Attributs

Placer les attributs comme `@editable` sur leur propre ligne.

### Imports

Garder les imports organisés et stables.

### Encapsulation

Limiter la visibilité autant que possible.

Ne pas rendre tous les membres publics par défaut.

### Failure checks

Éviter les conditions énormes sur une seule ligne.

Si un bloc contient plusieurs opérations faillibles, préférer une présentation multiligne claire.

## Règles supplémentaires de ce repo

L'IA doit privilégier :

- lisibilité ;
- modularité ;
- fonctions courtes ;
- interfaces claires ;
- séparation entre logique métier, état, événements et UI ;
- aucun commentaire inutile décrivant simplement la ligne suivante.
