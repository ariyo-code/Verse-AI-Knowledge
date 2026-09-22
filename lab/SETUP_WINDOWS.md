# VerseLab — Setup Windows

## 1. Créer un projet UEFN vide

Nom conseillé :

```text
VerseLab
```

Ajoute un simple niveau vide.

## 2. Identifier le dossier contenant les fichiers Verse

Tu le passeras aux scripts avec `-VerseDir`.

## 3. Initialiser le runner

PowerShell :

```powershell
.\lab\setup-verselab.ps1 `
  -VerseDir "C:\CHEMIN\VERS\TON\DOSSIER\VERSE"
```

Le script :

1. vérifie Python ;
2. synchronise le corpus UEFN Central si nécessaire ;
3. construit l'index RAG ;
4. garde/crée la queue ;
5. fabrique les batches ;
6. lance le diagnostic VerseLab.

## 4. Préparer le prochain candidat

```powershell
.\lab\next-candidate.ps1 `
  -VerseDir "C:\CHEMIN\VERS\TON\DOSSIER\VERSE"
```

## 5. Compile dans UEFN

Le fichier est copié dans VerseLab avec un nom commençant par `VAI_`.

Compile Verse dans UEFN.

## 6. Enregistrer le résultat

Succès :

```bash
python tools/lab_result.py success \
  --evidence "UEFN build succeeded"
```

Échec API :

```bash
python tools/lab_result.py fail \
  --classification api-or-version \
  --error "MESSAGE EXACT"
```

Dépendance manquante :

```bash
python tools/lab_result.py blocked \
  --classification missing-dependency \
  --error "MESSAGE EXACT"
```

Le runner passe ensuite au candidat suivant.
