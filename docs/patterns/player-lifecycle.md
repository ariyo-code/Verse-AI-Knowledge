# Pattern — lifecycle joueur

## À l'initialisation

Ne pas traiter uniquement les joueurs qui rejoignent après `OnBegin`.

Un système complet doit généralement considérer :

1. les joueurs déjà présents via `GetPlayers()`;
2. `PlayerAddedEvent()` pour les nouveaux joueurs ;
3. `PlayerRemovedEvent()` pour le nettoyage.

## Exemple d'architecture

```text
OnBegin
 ├─ initialize existing players
 ├─ subscribe PlayerAddedEvent
 └─ subscribe PlayerRemovedEvent

PlayerAdded
 └─ create runtime state

PlayerRemoved
 ├─ cancel subscriptions
 ├─ stop tasks
 ├─ remove UI
 └─ remove runtime state
```

## Respawn

Le `player` peut rester le même tandis que son `fort_character` change.

Ne pas stocker éternellement une ancienne référence `fort_character` sans revalider son cycle de vie.
