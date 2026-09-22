# Creative devices

Sources :

- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/devices/creative_device
- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/devices/creative_device_base
- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/devices/creative_object

Dernière vérification : 2026-09-22.

## `creative_device`

Un device Verse personnalisé dérive généralement de `creative_device`.

Module documenté :

`/Fortnite.com/Devices`

## Lifecycle

`OnBegin` sert à lancer la logique lorsque l'expérience démarre.

`OnEnd` existe également, mais la documentation actuelle avertit que des coroutines lancées depuis `OnEnd` peuvent ne jamais s'exécuter.

Conclusion : ne pas compter sur `OnEnd` pour une opération asynchrone critique.

## Transform

Les objets créatifs exposent notamment des opérations de transformation comme :

- lecture du transform ;
- téléportation ;
- déplacement.

La documentation de `creative_object` indique qu'il faut vérifier la validité d'un objet avant certaines opérations lorsqu'il peut avoir été détruit ou supprimé pendant le gameplay.

## Règles IA

Avant d'appeler une fonction sur un objet créatif potentiellement détruit :

- vérifier si l'objet peut être invalidé ;
- consulter la documentation de la méthode ;
- ajouter la validation nécessaire.

Ne pas supposer qu'une référence placée au début de la partie restera valide éternellement.
