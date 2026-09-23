#!/usr/bin/env python3
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.epic_http import validate_epic_url, StrictEpicRedirectHandler  # noqa: E402

good = "https://dev.epicgames.com/documentation/fortnite/verse-api"
assert validate_epic_url(good) == good

bad = [
    "http://dev.epicgames.com/documentation/fortnite/verse-api",
    "https://dev.epicgames.com.attacker.example/documentation/fortnite/verse-api",
    "https://user:pass@dev.epicgames.com/documentation/fortnite/verse-api",
    "https://evil.example/?next=https://dev.epicgames.com/documentation/fortnite/verse-api",
    "https://dev.epicgames.com:444/documentation/fortnite/verse-api",
    "https://dev.epicgames.com/not-documentation/fortnite/verse-api",
]
for url in bad:
    try:
        validate_epic_url(url)
    except ValueError:
        pass
    else:
        raise AssertionError(f"unsafe URL accepted: {url}")

handler = StrictEpicRedirectHandler()
request = urllib.request.Request(good)
try:
    handler.redirect_request(
        request, None, 302, "Found", {},
        "https://attacker.example/documentation/fortnite/verse-api",
    )
except ValueError:
    pass
else:
    raise AssertionError("redirect to non-allowlisted host was accepted")

print("V24 Epic URL security tests OK")
