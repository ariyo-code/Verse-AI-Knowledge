# UEFN MCP Error Feedback Loop

## But

Transformer les erreurs réelles du projet en mémoire réutilisable.

## Workflow

```text
modification Verse
    ↓
compile UEFN
    ↓
succès ? ── oui → continuer
    │
    non
    ↓
capturer message exact
    ↓
search_errors.py
    ↓
erreur connue ?
  ┌───────┴────────┐
 oui              non
 ↓                 ↓
appliquer          add_error.py
fix connu          ↓
 ↓              diagnostiquer
compile            ↓
 ↓              corriger
succès ?           ↓
 ↓              compile
update_error.py ←──┘
    ↓
preuve enregistrée
```

## Règle

Une erreur `observed` n'est pas encore une règle.

Elle ne devient `fixed` qu'après compilation réussie.

Elle ne devient `verified` qu'après compilation + test runtime.

## Commandes

Ajouter une vraie erreur :

```bash
python tools/add_error.py   --message "MESSAGE EXACT UEFN"   --category compiler   --file path/to/file.verse   --version 42.20
```

Rechercher avant de corriger :

```bash
python tools/search_errors.py "texte de l'erreur"
```

Après correction compilée :

```bash
python tools/update_error.py ERR_ID   --status fixed   --cause "cause confirmée"   --correction "correction appliquée"   --compiled   --evidence "UEFN compile succeeded"
```

Après playtest :

```bash
python tools/update_error.py ERR_ID   --status verified   --compiled   --runtime-tested   --evidence "UEFN compile + playtest succeeded"
```
