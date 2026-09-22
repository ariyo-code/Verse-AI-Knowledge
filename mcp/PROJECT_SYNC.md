# Sync Project Memory with UEFN

## Initial discovery

1. Read actual Verse files through MCP or local project folder.
2. Run static scan if filesystem access exists:

```bash
python tools/scan_verse_project.py /path/to/project --output project_scan.json
```

3. Generate a discovered project profile:

```bash
python tools/create_project_profile.py project_scan.json --name "My UEFN Project"
```

4. Compare discovered code with planned manifests.
5. Update system manifests only after confirming the real architecture.

## During development

After a meaningful system change:

- update system file list;
- update dependencies;
- update public interfaces;
- update runtime/persistent state;
- update ADR if the architectural decision changed;
- compile;
- update verification status only with evidence.

## Never

Do not let the project memory silently overwrite the actual UEFN project.

The memory documents and indexes the project; UEFN remains the execution truth.
