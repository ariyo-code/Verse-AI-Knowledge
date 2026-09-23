#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.claims import resolve_claim  # noqa: E402

verified = resolve_claim("GetFortCharacter", "signature", root=ROOT)
assert verified["decision"] == "ALLOW"
assert verified["supported"] is True
assert verified["evidence_ids"]

presence = resolve_claim("MakeCanvasSlot", "presence", root=ROOT)
assert presence["decision"] == "ALLOW"

unverified = resolve_claim("button_device", "signature", root=ROOT)
assert unverified["decision"] == "TODO(API VERIFY)"
assert unverified["supported"] is False

unknown = resolve_claim("definitely_fake_api", "signature", root=ROOT)
assert unknown["decision"] == "TODO(API VERIFY)"

print("V24 claim resolution tests OK")
