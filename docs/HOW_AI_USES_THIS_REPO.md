# Comment une IA doit utiliser ce repo

## Retrieval first

Ce dépôt n'est utile que si l'agent le consulte AVANT de générer du code.

Pour toute tâche Verse non triviale :

```bash
python tools/search_knowledge.py "termes importants"
```

Exemples :

```bash
python tools/search_knowledge.py "teleport agent"
python tools/search_knowledge.py "button event subscription"
python tools/search_knowledge.py "player ui"
python tools/search_knowledge.py "failure decides transacts"
```

Ensuite :

1. ouvrir les fichiers les mieux classés ;
2. lire l'API card correspondante ;
3. lire le système existant si présent ;
4. vérifier les erreurs/deprecations ;
5. seulement après, écrire le code.

## Pourquoi

Un modèle qui possède beaucoup de connaissances en paramètres peut encore :

- se souvenir d'une ancienne API ;
- confondre deux signatures ;
- inventer une fonction plausible ;
- oublier un effet ;
- oublier un cas multijoueur.

Le retrieval local réduit ces erreurs.

## Quand utiliser Internet

Si l'information peut avoir changé depuis `last_verified`, vérifier la documentation officielle Epic actuelle avant de coder.

## Règle de version

Ne jamais supposer que `latest` signifie compatible avec le projet de l'utilisateur.

Si le projet utilise une version UEFN plus ancienne, comparer les API.
