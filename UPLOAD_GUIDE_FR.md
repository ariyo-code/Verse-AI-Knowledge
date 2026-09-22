# Mettre Verse AI Knowledge sur GitHub — Guide PC

## Dossier à envoyer

Après avoir décompressé l'archive, ouvre :

```text
Verse-AI-Knowledge/
```

À l'intérieur, tu dois voir directement :

```text
README.md
README_FR.md
README_EN.md
AGENTS.md
AI_GUIDE.md
portable/
knowledge/
docs/
projects/
rag/
tools/
lab/
.github/
...
```

**C'est le contenu de ce dossier qu'il faut mettre à la racine du dépôt GitHub.**

Il ne faut pas obtenir :

```text
Verse-AI-Knowledge/
└── Verse-AI-Knowledge/
    └── README.md
```

## Méthode recommandée : GitHub Desktop

1. Installe GitHub Desktop.
2. Connecte ton compte GitHub.
3. Clone ton dépôt `Verse-AI-Knowledge`.
4. Ouvre le dossier local cloné.
5. Copie **tout le contenu** du dossier fourni `Verse-AI-Knowledge/` dans le dossier cloné.
6. Dans GitHub Desktop, vérifie les changements.
7. Message de commit conseillé :

```text
Initial release - Verse AI Knowledge v21
```

8. Clique sur `Commit to main`.
9. Clique sur `Push origin`.

## Branches conseillées

Garde `main` stable.

Branches principales possibles :

```text
main
dev
ui-creator
rag
verselab
external-corpus
examples
experimental
```

Pour les modifications ponctuelles :

```text
feature/phone-system
feature/ui-preview
fix/api-catalog
fix/ui-cleanup
```

## Après l'upload

Vérifie sur GitHub que la page d'accueil affiche bien `README.md` et que les dossiers `portable`, `knowledge`, `docs`, `.github` et `tools` sont directement visibles.

## Ne pas publier de secrets

Ne mets jamais dans GitHub :

```text
.env
tokens
mots de passe
clés API
identifiants Epic
DATABASE_URL privée
token Discord
```

Le `.gitignore` du projet bloque déjà plusieurs fichiers sensibles courants.
