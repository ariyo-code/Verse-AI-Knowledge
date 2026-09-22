#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"tools"))

from lab_state import transition

def entry(status):
    return {"queue_status":status}

# Valid paths
e=entry("pending")
transition(e,"staged")
transition(e,"compiling")
transition(e,"compiled")
transition(e,"verified")
transition(e,"multiplayer-verified")
assert e["queue_status"]=="multiplayer-verified"

# Invalid shortcut
e=entry("pending")
try:
    transition(e,"compiled")
except ValueError:
    pass
else:
    raise AssertionError("pending -> compiled should be blocked")

# Invalid verify shortcut
e=entry("staged")
try:
    transition(e,"verified")
except ValueError:
    pass
else:
    raise AssertionError("staged -> verified should be blocked")

print("VerseLab state tests OK")
