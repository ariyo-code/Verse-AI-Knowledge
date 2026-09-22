# External Corpus Trust

## Why this exists

A public GitHub repository can be useful without being equivalent to official or locally verified knowledge.

## Trust order

```text
UEFN local compiler/runtime
> current official Epic API
> locally multiplayer-verified
> locally verified
> locally compiled
> external compiler-claimed
> external community
> reference-only
```

## `external-compiler-claimed`

The upstream maintainer explicitly claims real compilation/validation.

This repository records that claim, but does not silently convert it to our local `compiled` status.

## `external-community`

Public community code under a verified reusable license.

Useful as patterns and retrieval evidence, but signatures and behaviors may be stale.

## `reference-only`

Useful repository to inspect/search, but code is not vendored into the reusable corpus because licensing/provenance is not approved.

## Promotion

An external example may become locally `compiled` or `verified` only after being copied into staging and going through the normal UEFN quality gate.
