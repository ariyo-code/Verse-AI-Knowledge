# Persistence Verse

Source officielle :
https://dev.epicgames.com/documentation/fortnite/using-persistable-data-in-verse

Dernière vérification : 2026-09-22.

## Principe

Verse prend en charge des données persistantes associées aux joueurs.

La documentation actuelle distingue notamment :

- `weak_map(session, t)` pour des données liées à la session actuelle ;
- `weak_map(player, t)` pour des données persistables associées à un joueur.

## Important

Une donnée persistante doit utiliser un type autorisé comme type persistable.

Ne pas supposer qu'une classe ou structure arbitraire peut être stockée.

## Architecture recommandée

Séparer :

1. modèle persistable ;
2. état runtime ;
3. migration ;
4. initialisation d'un joueur ;
5. sauvegarde / mise à jour ;
6. logique gameplay.

## Migration

Une nouvelle version d'un système ne doit pas casser les données enregistrées des joueurs.

Pour toute modification d'un schéma :

- documenter l'ancienne structure ;
- documenter la nouvelle ;
- définir une stratégie de migration ;
- tester les joueurs existants ;
- tester un nouveau joueur sans données.

## Règle IA

Pour tout système RP avec économie, inventaire, whitelist, profil ou progression, l'IA doit explicitement dire quelles données sont :

- runtime seulement ;
- persistantes ;
- recalculables ;
- sensibles aux migrations.
