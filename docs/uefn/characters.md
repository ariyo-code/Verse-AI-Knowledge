# Players, agents et fort_character

Sources :

- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/characters/fort_character
- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/characters/getfortcharacter

Dernière vérification : 2026-09-22.

## `fort_character`

`fort_character` représente l'API principale du personnage Fortnite.

Module :

`/Fortnite.com/Characters`

L'interface expose plusieurs capacités liées notamment à :

- position ;
- santé ;
- soins ;
- dégâts ;
- bouclier ;
- élimination ;
- actions de gameplay.

## Agent vers personnage

`GetFortCharacter` permet d'obtenir le `fort_character` associé à un `agent`.

L'opération est faillible.

Ne jamais écrire une architecture qui suppose que chaque `agent` possède toujours un personnage valide.

Situations à prendre en compte :

- apparition pas encore terminée ;
- joueur éliminé ;
- respawn ;
- joueur qui quitte ;
- type d'agent sans personnage Fortnite exploitable.

## Événements

Le personnage expose des événements de gameplay tels que l'élimination ou le saut.

Toute subscription doit être pensée avec sa durée de vie.
