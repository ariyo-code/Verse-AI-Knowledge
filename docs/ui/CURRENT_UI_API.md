# Current Verse UI API — 42.20

Sources officielles :

- https://dev.epicgames.com/documentation/fortnite/verse-api/unrealenginedotcom/temporary/ui
- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/ui

Dernière vérification : 2026-09-22.

## Deux modules importants

### `/UnrealEngine.com/Temporary/UI`

Contient notamment :

- `player_ui`
- `widget`
- `button`
- `canvas`
- `overlay`
- `stack_box`
- `color_block`
- `texture_block`
- `material_block`
- slots / anchors / margin
- `GetPlayerUI`
- `MakeCanvasSlot`

### `/Fortnite.com/UI`

Contient notamment :

- `text_button_base`
- `button_loud`
- `button_regular`
- `button_quiet`
- `slider_regular`
- `text_block`
- `fort_hud_controller`
- identifiants HUD Fortnite/Creative

## Important

Les UI Verse sont par joueur.

`GetPlayerUI` est faillible et doit être utilisé dans un failure context.

Ne pas mélanger arbitrairement les deux modules UI : certains noms peuvent être ambigus selon les imports du projet.
