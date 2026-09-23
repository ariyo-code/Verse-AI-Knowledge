# Error Memory

Cette section transforme les vrais échecs Verse/UEFN en connaissance réutilisable.

## Principe

Une erreur n'est utile au repo que si elle contient suffisamment de contexte pour être retrouvée et réutilisée.

Chaque entrée doit idéalement contenir :

- message exact ;
- type d'erreur ;
- fichier / contexte ;
- snippet minimal fautif ;
- cause ;
- correction ;
- version UEFN / Verse ;
- statut de confirmation ;
- preuve de compilation ou de test.

## Statuts

- `observed` : erreur réelle capturée, cause pas encore confirmée ;
- `diagnosed` : cause plausible/confirmée, correction pas encore validée ;
- `fixed` : correction compilée ;
- `verified` : correction compilée + comportement testé ;
- `deprecated` : erreur historique liée à une ancienne version.

## Règle

Ne jamais inventer une erreur pour "remplir" la base.

La mémoire d'erreurs doit venir de vrais messages UEFN/compiler/runtime.
