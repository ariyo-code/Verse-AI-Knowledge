# Pattern — subscription à un événement

Statut : `draft` (pattern documenté, snippet non certifié compilé dans ce repo)

Une subscription Verse doit avoir un propriétaire et une durée de vie.

Pattern conceptuel :

```verse
var MaybeSubscription:?cancelable = false

StartListening():void=
    Subscription := SomeDevice.SomeEvent.Subscribe(OnSomeEvent)
    set MaybeSubscription = option{Subscription}

StopListening():void=
    if (Subscription := MaybeSubscription?):
        Subscription.Cancel()
        set MaybeSubscription = false
```

Points à vérifier selon le cas :

- type exact du payload de l'événement ;
- signature exacte du handler ;
- possibilité de souscrire plusieurs fois ;
- moment où l'abonnement doit être annulé.

Epic documente explicitement que `Subscribe()` renvoie un `cancelable`.
