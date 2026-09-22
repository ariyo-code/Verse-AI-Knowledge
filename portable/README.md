# Verse AI Portable v20

Objectif : rendre le savoir Verse utilisable dans **n'importe quel LLM** sans avoir besoin du repo complet.

## Le plus simple

Ouvre :

`VERSE_AI_MASTER_PROMPT.txt`

Copie tout le contenu dans :
- ChatGPT
- Gemini
- Codex
- Claude
- autre assistant IA

Puis ajoute ton besoin après `=== USER TASK ===`.

## Exemple

```text
=== USER TASK ===

Fais-moi un système de véhicules RP.
Chaque joueur peut acheter 2 véhicules.
Il peut donner une clé, la retirer, verrouiller le véhicule,
transférer le véhicule et le vendre.
Nettoie tout quand le joueur quitte.
```

## Ce que le prompt force

- ne pas inventer d'API Verse;
- architecture modulaire;
- gestion correcte des joueurs;
- UI propre;
- gestion async;
- cleanup;
- failure contexts;
- séparation runtime/persistence;
- prise en compte du multijoueur;
- explication du setup UEFN;
- signalement clair des APIs incertaines.

## Limite

Aucun prompt ne peut garantir qu'un code Verse compile sans disposer de la version exacte d'UEFN et de ses APIs.

Le but de ce pack est donc :
**réduire fortement les hallucinations et obtenir du code beaucoup plus propre**, quel que soit le modèle utilisé.
