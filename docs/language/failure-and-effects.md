# Failure contexts et effets

Sources :

- https://dev.epicgames.com/documentation/fortnite/basics-of-writing-code-9-failure-and-control-flow-in-verse
- https://dev.epicgames.com/documentation/fortnite/verse-glossary
- https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/characters/getfortcharacter

Dernière vérification : 2026-09-22.

## Principe

Verse utilise l'échec comme mécanisme de contrôle de flux.

Certaines expressions peuvent échouer au lieu de renvoyer simplement une valeur classique.

Elles doivent être exécutées dans un contexte qui autorise cet échec.

## Exemples de choses faillibles

Selon l'API ou l'opération :

- accès potentiellement invalide à un élément ;
- conversion / récupération conditionnelle ;
- fonction portant l'effet `<decides>`;
- certaines comparaisons ou opérations dépendant d'une condition.

## `<decides>`

Une fonction marquée `<decides>` peut échouer.

Un appel à cette fonction est donc une expression faillible.

L'appel doit apparaître dans un contexte approprié.

## `<transacts>`

`<transacts>` indique que les actions effectuées par une fonction peuvent participer à une opération qui peut être annulée si le contexte échoue.

L'écriture dans une variable mutable implique souvent cet effet.

## Exemple important : GetFortCharacter

L'extension `GetFortCharacter` de `agent` est actuellement documentée avec les effets :

- `<transacts>`
- `<decides>`

L'IA ne doit donc pas la traiter comme une conversion toujours réussie.

## Règle IA

Avant d'utiliser une fonction de l'API :

1. vérifier sa signature actuelle ;
2. relever ses effets ;
3. vérifier si son appel est faillible ;
4. écrire le contexte de failure adapté ;
5. ne jamais retirer `<decides>` ou `<transacts>` "pour faire compiler".
