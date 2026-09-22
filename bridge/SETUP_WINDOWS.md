# Setup Windows — Real Project Bridge

## 1. Extraire le repo

Exemple :

```text
C:\Verse-AI-Knowledge
```

## 2. Trouver le dossier contenant les fichiers `.verse`

Tu peux viser :
- la racine du projet ;
- ou un sous-dossier contenant les sources Verse.

## 3. Lancer le bootstrap

PowerShell :

```powershell
.\bridge\bootstrap-project.ps1 `
  -ProjectPath "C:\CHEMIN\VERS\TON_PROJET" `
  -ProjectName "Mon Projet UEFN"
```

## 4. Résultat

Le script génère :

```text
bridge/generated/
├── project_scan.json
├── project_profile/
├── PROJECT_CONTEXT.md
└── BRIDGE_STATUS.json
```

## 5. Ensuite dans Codex

Utilise :

```text
Read AGENTS.md.
Read bridge/generated/PROJECT_CONTEXT.md.
Read rag/generated/CODEX_CONTEXT.md if present.
Discover UEFN MCP.
Inspect the real Verse project before editing.
Compile after each meaningful change.
```
