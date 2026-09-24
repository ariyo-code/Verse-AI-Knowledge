from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from verse_ai_knowledge.claims import resolve_claim
def test_plausible_fake_api_not_allowed():
    for name in ["GetFortniteCharacter","TeleportAllPlayersNative","PlayerUIManager","VehicleCard"]:
        assert resolve_claim(name,"signature",root=ROOT)["decision"]=="TODO(API VERIFY)"
