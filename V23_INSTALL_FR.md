# Installer V23 manuellement

Cette archive contient le dépôt complet V23, pas un simple overlay.

1. Fais une sauvegarde de ton dépôt actuel.
2. Extrais l'archive V23.
3. Copie tout le contenu extrait dans ton dossier local `Verse-AI-Knowledge`.
4. **Ne supprime pas le dossier caché `.git` de ton dépôt local.**
5. Remplace les fichiers existants lorsque Windows le demande.
6. Ouvre un terminal à la racine et lance :

```powershell
python tools/preflight.py
python tools/validate_all.py
python tools/rag_benchmark.py
python tools/run_evidence_benchmark.py
```

Puis commit/push si tout est vert.

Commit conseillé :

```text
Release V23 — API Coverage, Generation Reliability & Provenance
```
