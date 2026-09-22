# State management

## Trois types d'état

### Configuration

Références de devices et paramètres fixes.

### Runtime state

Informations uniquement valables pendant l'expérience ou le round.

Exemples :

- menu ouvert ;
- véhicule actuellement utilisé ;
- cooldown actif ;
- tâche async en cours.

### Persistent state

Informations explicitement destinées à survivre aux sessions.

Exemples possibles :

- progression ;
- argent ;
- préférences ;
- profil RP.

## Règle

Le code qui modifie un état doit avoir un propriétaire clairement identifié.

Éviter qu'une UI, un handler d'événement et un service modifient directement la même donnée sans abstraction commune.
