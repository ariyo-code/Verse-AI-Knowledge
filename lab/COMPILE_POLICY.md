# Compile Policy

## A successful local UEFN build means

Status may become:

`compiled`

It does **not** mean:

- runtime behavior is correct;
- multiplayer behavior is correct;
- the architecture is recommended.

## A compiler failure means

Store the exact error first.

Only classify the failure when the evidence supports the classification.

## Missing dependency

Examples from larger projects can reference:

- generated asset symbols;
- custom classes;
- another Verse file;
- editor assets;
- project-specific modules.

This is `blocked-environment`, not automatically `compile-failed`.

## Promotion hierarchy

```text
external-compiler-claimed
      ↓
local UEFN compile
      ↓
compiled
      ↓
runtime playtest
      ↓
verified
      ↓
multiplayer playtest
      ↓
multiplayer-verified
```
