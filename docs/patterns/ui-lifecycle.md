# Pattern — UI par joueur

L'UI Verse est attachée à un `player_ui`.

`GetPlayerUI(Player)` est faillible dans l'API actuelle.

## Architecture recommandée

Conserver séparément :

- le widget racine par joueur ;
- l'état métier affiché ;
- les subscriptions aux boutons/widgets ;
- la logique de création ;
- la logique de suppression.

## Cleanup

Lorsqu'un joueur quitte :

- retirer le widget si l'UI est encore accessible ;
- supprimer les références runtime ;
- annuler les subscriptions liées au widget.

Ne pas partager une instance mutable de widget entre tous les joueurs sans avoir vérifié que c'est réellement le comportement souhaité.
