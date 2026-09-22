# Optional Semantic Retrieval

Le moteur V10 fonctionne sans dépendance externe.

Il utilise :

- BM25 lexical ;
- exact API/symbol match ;
- route boosts ;
- project/error boosts ;
- trust/status/version boosts.

## Pourquoi pas d'embeddings obligatoires

Une dépendance embeddings locale ajoute :

- modèle à télécharger ;
- poids disque ;
- compatibilité Python/GPU ;
- maintenance.

Pour un repo utilisable immédiatement sur GitHub/Codex, V10 garde le cœur sans dépendance.

## Extension future

Un provider embeddings peut être ajouté derrière une interface facultative.

Le semantic score doit alors être **un signal supplémentaire**, pas remplacer :

- exact API match ;
- trust;
- version;
- UEFN verification.
