# VerseLab Runner

V15 transforme la file de recompilation en workflow exécutable.

## Principe

Un seul candidat non vérifié est testé à la fois.

```text
pending
  ↓
staged
  ↓
compiling
  ├─ compile-failed
  ├─ blocked-environment
  └─ compiled
         ↓
   runtime-pending
         ↓
      verified
         ↓
 multiplayer-verified
```

## Pourquoi un seul candidat à la fois

Si dix fichiers inconnus sont présents dans le projet et que le build échoue,
on ne peut plus attribuer proprement les erreurs.

VerseLab isole donc les essais.
