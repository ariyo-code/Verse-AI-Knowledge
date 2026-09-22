# Pattern — validité d'un creative_object

La référence officielle avertit que `GetTransform()` peut provoquer une runtime error si un `creative_object` a été détruit/disposé et que sa validité n'est pas vérifiée.

## Règle

Dès qu'un objet peut être supprimé pendant le gameplay :

1. considérer sa référence comme potentiellement invalide ;
2. consulter l'API du type ;
3. vérifier `IsValid` lorsque requis ;
4. ne pas exécuter aveuglément `GetTransform`/déplacement après destruction.
