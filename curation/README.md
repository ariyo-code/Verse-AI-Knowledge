# Automatic Example Curation

V14 transforme le corpus GitHub externe en une sélection utile pour l'entraînement Verse.

## Pipeline

```text
external/corpus
      ↓
static analysis
      ↓
API/device classification
      ↓
quality + relevance scoring
      ↓
deduplication
      ↓
curated_examples.json
      ↓
UEFN compile queue
      ↓
real compile result
      ↓
local compiled promotion
```

## Important

La sélection automatique ne prouve pas la qualité.

Elle sert uniquement à décider **quoi tester en premier**.

La compilation UEFN reste obligatoire avant promotion locale.
