using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

teleport_agent_example := class(creative_device):

    @editable
    Button:button_device = button_device{}

    @editable
    Teleporter:teleporter_device = teleporter_device{}

    OnBegin<override>()<suspends>:void=
        Button.InteractedWithEvent.Subscribe(OnInteracted)

    OnInteracted(Agent:agent):void=
        Teleporter.Teleport(Agent)
