# Architecture RAG + UEFN MCP

## Deux couches

**Mémoire** : docs, API cards, patterns, erreurs et systèmes.

**Vérité live** : fichiers réels, compilateur, devices et sessions via UEFN MCP.

```text
Epic Docs
   ↓
Verse-AI-Knowledge
   ↓ retrieval
Coding Agent
   ↓ MCP
UEFN → compile → session → logs
   ↓
knowledge confirmée
```

## Ordre de vérité

1. résultat réel du compilateur/runtime UEFN ;
2. référence API Epic actuelle ;
3. `multiplayer-verified` ;
4. `verified` ;
5. `compiled` ;
6. documentation interne ;
7. `draft` ;
8. mémoire brute du modèle.
