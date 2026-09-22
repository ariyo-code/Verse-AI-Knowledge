using { /Fortnite.com/Characters }
using { /Fortnite.com/Vehicles }

TryGetAgentVehicle(Agent:agent):void=
    if:
        Character := Agent.GetFortCharacter[]
        Vehicle := Character.GetVehicle[]
    then:
        Drivers := Vehicle.GetDrivers()
