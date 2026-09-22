# SceneGraph component lifecycle

Sources :

- https://dev.epicgames.com/documentation/fortnite/verse-api/versedotorg/scenegraph
- https://dev.epicgames.com/documentation/fortnite/verse-api/versedotorg/scenegraph/component/onbeginsimulation
- https://dev.epicgames.com/documentation/fortnite/verse-api/versedotorg/scenegraph/component/onsimulate

Ordre conceptuel actuel documenté :

```text
OnAddedToScene
↓
OnBeginSimulation
↓
OnSimulate
↓
OnEndSimulation
↓
OnRemovingFromScene
```

`OnBeginSimulation` sert au setup qui doit finir immédiatement.

```verse
OnBeginSimulation<protected><native><native_callable>()<transacts><no_rollback>:void
```

`OnSimulate` sert à la logique async et est annulé avant `OnEndSimulation`.

```verse
OnSimulate<protected><native_callable>()<transacts><suspends><no_rollback>:void
```

Cela donne une meilleure gestion de lifetime que des `spawn` non structurés.
