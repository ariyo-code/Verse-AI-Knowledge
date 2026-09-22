# Architecture de la mémoire d'erreurs

## Pourquoi JSONL

`errors/error_memory.jsonl` est :

- simple à versionner ;
- lisible sans base de données ;
- facile à rechercher ;
- facile à convertir vers SQLite / embeddings plus tard ;
- compatible avec une ligne = une connaissance.

## Identifiant

L'ID est dérivé d'une version normalisée du message.

Objectif : dédupliquer les mêmes erreurs qui apparaissent avec des chemins ou positions différentes.

La normalisation ne doit pas supprimer les parties sémantiques importantes.

## Niveau de preuve

```text
observed
   ↓
diagnosed
   ↓
fixed
   ↓
verified
```

`fixed` exige une preuve de compilation.

`verified` exige au minimum :
- compilation ;
- test runtime pertinent.

Un test multijoueur reste un champ séparé.

## Recherche

La recherche doit favoriser :

1. message normalisé ;
2. API liée ;
3. tags ;
4. cause/correction ;
5. entrées `verified` ou `fixed`.

## Limitation

Une erreur identique peut parfois avoir plusieurs causes.

L'agent doit toujours comparer le contexte actuel avant d'appliquer une ancienne correction.
