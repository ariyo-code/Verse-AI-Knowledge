# Versioning de l'API Verse

Sources :

- https://dev.epicgames.com/documentation/fortnite/verse-api
- https://dev.epicgames.com/documentation/fortnite/42-20-fortnite-ecosystem-updates-and-release-notes

Dernière vérification : 2026-09-22.

## Version actuelle observée

Verse API : **42.20**

La page API officielle affiche actuellement cette version.

## Pourquoi suivre la version

Une solution correcte dans une ancienne version peut :

- produire une dépréciation ;
- changer de namespace ;
- recevoir une nouvelle surcharge ;
- avoir un comportement différent ;
- disparaître.

## Changement documenté en 42.20

Les API Marketplace ont été déplacées de :

`/Fortnite.com/Marketplace`

vers :

`/UnrealEngine.com/Marketplace`

L'ancien chemin reste actuellement disponible comme alias, mais génère des avertissements de dépréciation.

Pour du nouveau code, utiliser le namespace actuel documenté.

## Procédure après chaque mise à jour UEFN

1. Lire les release notes.
2. Chercher les sections Verse / API / Upgrade Notes.
3. Mettre à jour `docs/uefn/api-versioning.md`.
4. Ajouter les dépréciations à `errors/deprecations.md`.
5. Revalider les systèmes importants.
6. Modifier `manifest.json`.
