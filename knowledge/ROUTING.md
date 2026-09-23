# Routing table for AI agents

<!-- V23_ROUTING_ENTRY -->
## V23 entry route

For a new agent session: `AI_BOOTSTRAP.md` → this routing table → targeted retrieval → Evidence Pack → Claim Ledger → implementation → real UEFN validation when available. Use `verse-ai` as the preferred CLI; legacy `tools/*.py` entry points remain supported.

## V23 API coverage routing

| Besoin | Ouvrir / exécuter |
|---|---|
| vérifier une API exacte | `verse-ai api SYMBOL`, `knowledge/api/symbols.jsonl` |
| voir la couverture | `verse-ai coverage`, `knowledge/api/coverage.json` |
| prochaine API à vérifier | `verse-ai api-queue` |
| récolter page Epic | `tools/harvest_epic_api.py` — candidate uniquement |
| promouvoir après review | `tools/review_api_candidate.py` |
| provenance code généré | `docs/GENERATED_CODE_MARKER.md` |
| benchmark génération | `evals/generation/`, `tools/evaluate_generation_run.py` |


Quand la demande contient…

| Sujet | Ouvrir en priorité |
|---|---|
| bouton / interaction | `docs/api/core/button_device.md`, `docs/patterns/event-subscription.md` |
| téléportation | `docs/api/core/teleporter_device.md` |
| joueurs connectés | `docs/api/core/fort_playspace.md`, `docs/patterns/player-lifecycle.md` |
| personnage | `docs/api/core/GetFortCharacter.md`, `docs/api/core/fort_character.md` |
| HUD message | `docs/api/core/hud_message_device.md` |
| UI Verse | `docs/api/core/GetPlayerUI.md`, `docs/api/core/player_ui.md`, `docs/patterns/ui-lifecycle.md` |
| item / donner item | `docs/api/core/item_granter_device.md` |
| retirer item | `docs/api/core/item_remover_device.md` |
| inventaire requis | `docs/api/core/conditional_button_device.md` |
| spawn / respawn | `docs/api/core/player_spawner_device.md` |
| failure / decides | `docs/language/failure-and-effects.md` |
| async / race / spawn | `docs/language/concurrency.md`, `docs/architecture/async-lifetime.md` |
| bug compilation | `errors/compiler-errors.md` |
| runtime error | `errors/runtime-errors.md`, `docs/uefn/debugging.md` |
| API supprimée | `errors/deprecations.md` |
| persistence | `docs/uefn/persistence.md` |

Après ces fichiers, consulter la documentation officielle Epic si une signature ou version reste incertaine.


## Live UEFN / MCP routing

| Demande | Ouvrir |
|---|---|
| connecter IA à UEFN | `mcp/SETUP.md`, `mcp/CODEX.md` |
| modifier/compiler Verse automatiquement | `mcp/agent-workflow.md`, `prompts/UEFN_MCP_AGENT.md` |
| tester une session | `mcp/agent-workflow.md` |
| architecture IA + UEFN | `docs/architecture/RAG_PLUS_MCP.md` |


## V5 module routing

| Sujet | Ouvrir |
|---|---|
| Verse UI / widgets | `docs/ui/CURRENT_UI_API.md`, `docs/api/core/player_ui.md`, `docs/api/core/widget.md` |
| équipes | `docs/teams/fort_team_collection.md` |
| véhicules | `docs/vehicles/fort_vehicle.md` |
| SceneGraph | `docs/scenegraph/LIFECYCLE.md`, `docs/scenegraph/TRANSFORMS.md` |
| animation SceneGraph | `docs/api/core/keyframed_movement_component.md` |
| trouver un module | `knowledge/module_catalog.json` |


## V6 error-memory routing

| Situation | Ouvrir / exécuter |
|---|---|
| erreur compilation UEFN | `mcp/ERROR_FEEDBACK_LOOP.md`, `python tools/search_errors.py "..."` |
| nouvelle erreur réelle | `python tools/add_error.py --message "..."` |
| correction confirmée | `python tools/update_error.py ERR_ID ...` |
| log runtime | `tools/ingest_uefn_log.py` |
| promouvoir code | `verification/README.md`, `tools/check_verification.py` |
| architecture mémoire d'erreurs | `docs/architecture/ERROR_MEMORY.md` |


## V7 project-memory routing

| Besoin | Ouvrir / exécuter |
|---|---|
| comprendre un projet existant | `docs/architecture/PROJECT_MEMORY.md`, `mcp/PROJECT_SYNC.md` |
| retrouver un système | `python tools/search_projects.py "..."` |
| scanner un projet Verse | `tools/scan_verse_project.py` |
| créer un profil découvert | `tools/create_project_profile.py` |
| architecture RP | `projects/rp-framework/project.json` |
| véhicule RP | `projects/rp-framework/systems/vehicle-manager/system.json` |
| téléphone RP | `projects/rp-framework/systems/phone-system/system.json` |
| inventaire RP | `projects/rp-framework/systems/inventory-system/system.json` |
| staff panel | `projects/rp-framework/systems/staff-panel/system.json` |


## V8 quality routing

| Besoin | Ouvrir / exécuter |
|---|---|
| mesurer l'agent | `benchmark/README.md`, `benchmark/tasks.json` |
| promotion draft → verified | `mcp/QUALITY_GATE.md`, `tools/promote_artifact.py` |
| vérifier API suspectes | `tools/check_api_references.py` |
| orchestrer une feature | `prompts/VERSE_ENGINEERING_ORCHESTRATOR.md` |
| rapport benchmark | `tools/benchmark_report.py` |


## V9 maintenance routing

| Besoin | Ouvrir / exécuter |
|---|---|
| surveiller Epic | `maintenance/README.md`, `tools/watch_epic_sources.py` |
| comparer version/docs | `tools/compare_epic_snapshot.py` |
| voir les impacts | `tools/build_revalidation_queue.py`, `tools/revalidation_report.py` |
| revalider après update | `prompts/MAINTENANCE_AGENT.md` |
| accepter nouveau baseline | `tools/accept_maintenance_baseline.py` |
| architecture de veille | `docs/architecture/AUTO_MAINTENANCE.md` |


## V10 RAG routing

| Besoin | Exécuter |
|---|---|
| rechercher intelligemment | `python tools/rag_query.py "..."` |
| fabriquer contexte Codex | `python tools/rag_context_pack.py "..."` |
| préparer une tâche Codex | `python tools/prepare_codex_context.py "..."` |
| reconstruire index | `python tools/rag_build_index.py` |
| tester retrieval | `python tools/rag_benchmark.py` |
| comprendre scoring | `rag/README.md`, `rag/config.json` |


## V11 real-project routing

| Besoin | Ouvrir / exécuter |
|---|---|
| connecter vrai projet | `bridge/SETUP_WINDOWS.md` |
| bootstrap Windows | `bridge/bootstrap-project.ps1` |
| démarrer Codex | `bridge/CODEX_START_PROMPT.md` |
| boucle compilation | `bridge/COMPILE_LOOP.md` |
| vérifier sync | `bridge/PROJECT_SYNC_CHECKLIST.md` |
| contexte tâche projet | `python tools/project_context_query.py "..."` |


## V12 external-source routing

| Besoin | Ouvrir / exécuter |
|---|---|
| voir sources GitHub approuvées | `external/sources.json` |
| synchroniser corpus | `python tools/sync_external_sources.py` |
| rapport corpus | `python tools/external_corpus_report.py` |
| règle de confiance | `docs/architecture/EXTERNAL_CORPUS_TRUST.md` |
| review code externe | `prompts/EXTERNAL_CORPUS_REVIEWER.md` |
| plan de curation | `external/CURATION_PLAN.md` |



## V14 recompilation routing

| Besoin | Exécuter |
|---|---|
| classer les exemples GitHub | `tools/curate_external_examples.py` |
| créer file UEFN | `tools/build_compile_queue.py` |
| prochain candidat | `python tools/compile_queue.py next` |
| stage dans Verse Lab | `tools/stage_compile_candidate.py` |
| prompt MCP compile | `tools/generate_compile_prompt.py` |
| enregistrer résultat | `tools/record_uefn_compile.py` |
| promouvoir compiled | `tools/promote_compiled_candidate.py` |
| progression | `tools/compile_progress_report.py` |


## V15 VerseLab runner routing

| Besoin | Fichier / commande |
|---|---|
| installer VerseLab | `lab/SETUP_WINDOWS.md` |
| lancer setup | `lab/setup-verselab.ps1` |
| prochain candidat | `lab/next-candidate.ps1` |
| batches | `tools/build_compile_batches.py` |
| enregistrer compile | `tools/lab_result.py` |
| enregistrer playtest | `tools/record_playtest.py` |
| diagnostic | `tools/lab_doctor.py` |
| dashboard | `tools/lab_dashboard.py` |
| règles agent | `prompts/VERSELAB_RUNNER_AGENT.md` |


## V17 one-click routing

| Besoin | Ouvrir / exécuter |
|---|---|
| démarrer rapidement | `lab/START_VERSELAB.bat` |
| guide | `lab/ONE_CLICK_GUIDE.md` |
| détecter dossier Verse | `tools/detect_uefn_verse_dir.py` |
| instructions après build | `tools/generate_active_candidate_instructions.py` |
| état du lab | `python tools/verselab_status.py` |


## V18 evidence routing

| Besoin | Commande |
|---|---|
| couverture corpus | `python tools/corpus_coverage.py` |
| hydrater 395 examples | `python tools/ensure_full_corpus.py` |
| dépendances | `tools/analyze_verse_dependencies.py` |
| evidence graph | `tools/rag_build_evidence_graph.py` |
| Evidence Pack | `tools/rag_context_compiler.py` |
| benchmark | `tools/run_evidence_benchmark.py` |


## V19 hardening routing

| Besoin | Commande |
|---|---|
| préflight | `python tools/preflight.py` |
| validation globale | `python tools/validate_all.py` |
| intégrité | `python tools/validate_integrity.py` |
| contrats CLI | `python tests/test_cli_contracts.py` |
| claim ledger | `python tools/build_claim_ledger.py` |
| self-test statique | `python tools/self_test.py` |
