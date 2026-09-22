# Verse UI Creator v21

Ce dossier transforme le Verse AI Portable en **UI Creator UEFN**.

## Utilisation la plus simple

1. Ouvre `VERSE_UI_CREATOR_MASTER_PROMPT.txt`.
2. Copie tout dans ChatGPT, Gemini, Codex, Claude, etc.
3. Ajoute ta demande après `=== UI TASK ===`.

Exemple :

```text
=== UI TASK ===

/ui create

Crée un garage RP style GTA / Apple.
À gauche : liste des véhicules.
À droite : aperçu, nom, état, plaque.
En bas : Sortir, Ranger, Verrouiller, Donner une clé.
Pagination si plus de 5 véhicules.
```

## Modes

- `/ui create`
- `/ui redesign`
- `/ui from-image`
- `/ui component`
- `/ui bind-event`
- `/ui responsive`
- `/ui refactor`

## Important

Les composants `VehicleCard`, `Panel`, `Modal`, etc. sont des **abstractions de design**.
Le générateur doit les convertir en vrais widgets Verse supportés et ne jamais les inventer comme API Epic.

## Fichiers

- `VERSE_UI_CREATOR_MASTER_PROMPT.txt` : prompt principal.
- `UI_SPEC.schema.json` : format d'interface.
- `COMPONENT_LIBRARY.json` : bibliothèque logique.
- `TASK_TEMPLATE.txt` : modèle de demande.
- `examples/GARAGE_UI_SPEC.json` : exemple.
