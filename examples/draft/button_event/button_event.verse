using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

button_event_example := class(creative_device):

    @editable
    Button:button_device = button_device{}

    OnBegin<override>()<suspends>:void=
        Button.InteractedWithEvent.Subscribe(OnInteracted)

    OnInteracted(Agent:agent):void=
        Print("Button interaction received")
