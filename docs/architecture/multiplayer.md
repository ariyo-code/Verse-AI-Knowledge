# Architecture multijoueur

## Principe

Un système Verse qui fonctionne pour un joueur n'est pas nécessairement correct à plusieurs.

## Checklist

Pour chaque fonctionnalité, vérifier :

- deux joueurs déclenchent l'action exactement au même moment ;
- le propriétaire du state est clair ;
- les données par joueur ne sont pas stockées dans une variable globale unique ;
- un joueur qui quitte libère son état runtime ;
- un nouveau joueur peut être initialisé après `OnBegin`;
- le respawn ne duplique pas les listeners ;
- un round suivant ne conserve pas un état runtime invalide ;
- une tâche async liée à un joueur ne continue pas inutilement après son départ.

## Modèle mental

```text
GLOBAL STATE
    ├── configuration
    ├── registries
    └── services

PLAYER STATE
    ├── runtime
    ├── UI
    ├── subscriptions
    └── tasks

PERSISTENT STATE
    └── données persistables seulement
```

Ne pas mélanger ces trois niveaux.
