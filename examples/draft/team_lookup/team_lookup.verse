using { /Fortnite.com/Playspaces }
using { /Fortnite.com/Teams }

TryGetAgentTeam(Playspace:fort_playspace, Agent:agent):void=
    Teams := Playspace.GetTeamCollection()
    if (AgentTeam := Teams.GetTeam[Agent]):
        AllTeams := Teams.GetTeams()
