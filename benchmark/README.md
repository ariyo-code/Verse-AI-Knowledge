# Verse AI Benchmark

Le benchmark sert à mesurer la qualité de l'agent au lieu de se fier à une impression.

## Ce qu'on mesure

- utilisation d'API réellement connues ;
- absence d'API inventées ;
- respect des failure contexts ;
- lifecycle joueur ;
- concurrence / async ;
- séparation runtime / persistence ;
- architecture modulaire ;
- prise en compte multijoueur ;
- compilation UEFN ;
- test runtime ;
- correction à partir d'un vrai message d'erreur.

## Niveaux

### Static
Peut être contrôlé sans UEFN.

### Compile
Exige une vraie compilation UEFN.

### Runtime
Exige un playtest.

### Multiplayer
Exige un test pertinent avec plusieurs joueurs.

## Règle

Un score statique élevé ne prouve jamais qu'un code compile.
