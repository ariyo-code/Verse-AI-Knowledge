# Local Hybrid RAG

V10 ajoute un moteur de retrieval local conçu pour les agents Verse / UEFN.

Le but n'est pas de charger tout le repo dans le contexte.

Le but est de sélectionner **le plus petit contexte utile et fiable**.

## Pipeline

```text
user request
   ↓
query routing
   ↓
exact symbol/API detection
   ↓
BM25 lexical retrieval
   ↓
trust/version/project/error boosts
   ↓
deduplication
   ↓
context-budget packing
   ↓
Codex / agent
```

## Pourquoi hybride

Une simple recherche de mots-clés rate souvent :

- les noms d'API exacts ;
- les synonymes ;
- les liens projet → système ;
- les erreurs déjà connues ;
- les fichiers plus fiables que d'autres.

Le moteur V10 combine plusieurs signaux déterministes.

## Important

Ce moteur ne remplace pas UEFN.

Il choisit le meilleur contexte à donner à l'agent.

UEFN reste la vérité pour compilation/runtime.
