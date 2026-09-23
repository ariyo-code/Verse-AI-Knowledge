# Staging

Tout nouveau code généré par l'IA devrait d'abord être considéré comme staging/draft.

Pipeline :

```text
generated
↓
static review
↓
UEFN compile
↓
runtime test
↓
multiplayer test if relevant
↓
promotion
```

Ne jamais copier automatiquement un artifact non compilé vers `examples/verified`.
