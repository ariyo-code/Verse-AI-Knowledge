# Project Memory

Cette couche permet à l'agent de comprendre non seulement Verse, mais aussi **les projets UEFN du développeur**.

Elle mémorise :

- systèmes existants ;
- responsabilités ;
- dépendances ;
- fichiers Verse ;
- devices requis ;
- état runtime ;
- état persistant ;
- événements ;
- interfaces publiques ;
- décisions d'architecture ;
- dette technique ;
- statut de validation ;
- compatibilité de version.

## Principe

```text
Knowledge Base
    ↓
Project Registry
    ↓
System Manifests
    ↓
Architecture Decisions
    ↓
Actual UEFN Project
```

Les profils de projet de ce dépôt peuvent être :

- `template`
- `planned`
- `discovered`
- `compiled`
- `verified`

Ne jamais marquer un projet `compiled` ou `verified` sans preuve réelle venant d'UEFN.
