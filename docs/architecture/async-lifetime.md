# Async lifetime

Chaque opération `<suspends>` doit avoir une durée de vie compréhensible.

## Questions obligatoires

- Qui démarre la tâche ?
- Peut-elle démarrer deux fois ?
- Quel événement la termine ?
- Est-elle liée à un joueur ?
- Que se passe-t-il au départ du joueur ?
- Que se passe-t-il à la fin de manche ?
- `race` peut-il modéliser proprement l'annulation ?
- `spawn` est-il vraiment nécessaire ?

## Règle anti-fuite

Ne jamais créer des tâches infinies depuis une boucle qui peut elle-même répéter la création de ces tâches.

## Préférence

Quand c'est possible :

événement -> tâche limitée -> fin explicite

plutôt que :

boucle infinie -> polling -> nouvelle tâche -> nouvelle tâche...
