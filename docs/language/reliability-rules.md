# Reliability Rules

## Interdictions

L'IA ne doit jamais :

- inventer une classe Verse ;
- inventer un chemin `using`;
- inventer une surcharge ;
- supposer qu'une API ancienne existe encore ;
- déclarer un snippet `verified` sans test réel ;
- transformer une erreur de compilation en hypothèse présentée comme certaine ;
- recopier une solution communautaire sans vérifier ses API.

## Avant génération

Créer une petite fiche mentale :

```text
Concepts nécessaires:
API nécessaires:
Effets/failure:
Événements:
Async:
État:
Cas multijoueur:
Persistence:
Version API:
```

## Après génération

Faire une seconde passe uniquement consacrée à :

1. noms des API ;
2. signatures ;
3. imports ;
4. effets ;
5. contexte de failure ;
6. lifetime async ;
7. départ joueur ;
8. respawn ;
9. duplication d'abonnements ;
10. version / dépréciations.

## Statut

Tout nouveau code généré commence en `draft`.
