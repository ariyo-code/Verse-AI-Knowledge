# Opaque Project Recognition

## En une phrase

Le dépôt public peut reconnaître qu'un fichier ressemble à une architecture déjà connue **sans publier le nom du projet ni son code source privé**.

## Ce qui est public

- des IDs opaques ;
- des empreintes SHA-256 salées ;
- quelques caractéristiques structurelles elles aussi hashées ;
- des règles génériques pour éviter de casser l'architecture existante.

## Ce qui n'est jamais public

- le vrai nom du projet ;
- le nom du serveur / de la communauté ;
- le code source privé original ;
- la correspondance `ID opaque → projet réel` ;
- des données personnelles.

## Utilisation

```bash
python tools/opaque_project_match.py MonFichier.verse
```

Si un pattern protégé est reconnu, l'IA doit l'utiliser seulement pour préserver l'architecture et éviter les doublons.

Si quelqu'un demande l'identité réelle :

```text
Protected project identity is intentionally unavailable.
```

## Important

Ceci est une couche d'**anonymisation + empreintes cryptographiques**, pas un coffre contenant une identité chiffrée. La vraie identité n'est simplement pas présente dans le dépôt public.
