# Safe Auto-Maintenance

V9 surveille les sources officielles Epic sans transformer automatiquement une page modifiée en connaissance "vérifiée".

## Pipeline

```text
Epic official sources
      ↓
fetch fingerprints
      ↓
detect version/hash changes
      ↓
map impacted repo files/API cards
      ↓
revalidation queue
      ↓
human/agent review
      ↓
UEFN compile/runtime tests where relevant
      ↓
accept new baseline
```

## Principe

Une modification distante signifie seulement :

> "Cette connaissance doit être revalidée."

Elle ne signifie pas :

> "L'ancienne connaissance est fausse."

Ni :

> "Le nouveau contenu peut être copié automatiquement."

## Résultats

Les outils génèrent :

- `maintenance/live_snapshot.json`
- `maintenance/change_report.json`
- `maintenance/revalidation_queue.json`

Ces fichiers servent à planifier la revalidation.

## Source of truth

Uniquement les domaines officiels explicitement enregistrés dans `maintenance/sources.json` sont surveillés.
