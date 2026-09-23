# Design d'un gros système Verse

Pour chaque système, séparer autant que possible :

```text
Configuration
    ↓
Domain / State
    ↓
Services
    ↓
Event handlers
    ↓
Presentation / UI
```

## Exemple RP

Un système d'inventaire ne devrait pas mélanger dans une seule classe :

- calcul du poids ;
- persistence ;
- rendu des slots ;
- contrôles joueur ;
- logs staff ;
- gestion du coffre entreprise.

Créer des composants avec des responsabilités précises réduit les erreurs et facilite les tests.

## Taille

Quand un fichier devient difficile à comprendre sans scrolling massif, revoir son découpage.

La modularité doit suivre les responsabilités, pas seulement le nombre de lignes.
