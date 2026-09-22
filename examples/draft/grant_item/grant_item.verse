using { /Fortnite.com/Devices }
using { /Verse.org/Simulation }

grant_item_example := class(creative_device):

    @editable
    Button:button_device = button_device{}

    @editable
    Granter:item_granter_device = item_granter_device{}

    OnBegin<override>()<suspends>:void=
        Button.InteractedWithEvent.Subscribe(OnInteracted)

    OnInteracted(Agent:agent):void=
        Granter.GrantItem(Agent)
