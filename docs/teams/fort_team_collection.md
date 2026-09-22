# Teams — fort_team_collection

Source :
https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/teams/fort_team_collection

Module :

`/Fortnite.com/Teams`

Fonctions actuelles importantes :

- `GetTeams`
- `AddToTeam`
- `IsOnTeam`
- `GetAgents`
- `GetTeam`
- `GetTeamAttitude`

Exemples de signatures vérifiées :

```verse
GetTeams<public>()<transacts>:[]team

AddToTeam<public>(InAgent:agent, InTeam:team)<transacts><decides>:void

GetTeam<public>(InAgent:agent)<transacts><decides>:team
```

Les fonctions portant `<decides>` sont faillibles.
