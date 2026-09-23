# COMMENCE ICI — V24

Pour une IA capable de lire le dépôt :

```text
AI_BOOTSTRAP.md
```

C'est l'entrée principale.

Ensuite, l'agent suit `knowledge/ROUTING.md`, utilise le retrieval ciblé, résout les claims API, construit les preuves puis valide.

Commandes utiles :

```bash
verse-ai api GetFortCharacter
verse-ai claim GetFortCharacter --field signature
verse-ai coverage
verse-ai doctor
verse-ai validate
```

Les anciens prompts portables V21/V23 restent disponibles pour compatibilité. Pour un agent repository-aware, `AI_BOOTSTRAP.md` est autoritaire.

Règle absolue : **ne jamais inventer une API Verse**.
