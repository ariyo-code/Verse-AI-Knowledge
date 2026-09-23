from __future__ import annotations

import urllib.parse
import urllib.request
from typing import Iterable

ALLOWED_HOST = "dev.epicgames.com"
ALLOWED_SCHEME = "https"
DEFAULT_MAX_BYTES = 2_000_000
DEFAULT_CONTENT_TYPES = ("text/html", "application/json", "text/plain")


def validate_epic_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() != ALLOWED_SCHEME:
        raise ValueError("Epic documentation URL must use HTTPS.")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Credentials are not allowed in Epic documentation URLs.")
    if (parsed.hostname or "").lower() != ALLOWED_HOST:
        raise ValueError("Epic documentation hostname is not allowlisted.")
    if parsed.port not in (None, 443):
        raise ValueError("Unexpected port in Epic documentation URL.")
    if not parsed.path.startswith("/documentation/"):
        raise ValueError("Only Epic documentation paths are allowed.")
    return urllib.parse.urlunsplit(parsed)


class StrictEpicRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_epic_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_epic(
    url: str,
    *,
    timeout: int = 20,
    max_bytes: int = DEFAULT_MAX_BYTES,
    allowed_content_types: Iterable[str] = DEFAULT_CONTENT_TYPES,
    user_agent: str = "Verse-AI-Knowledge-V24/1.0",
) -> tuple[bytes, str, str | None]:
    url = validate_epic_url(url)
    opener = urllib.request.build_opener(StrictEpicRedirectHandler())
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    with opener.open(req, timeout=timeout) as resp:
        final_url = validate_epic_url(resp.geturl())
        content_type = (resp.headers.get_content_type() if getattr(resp, "headers", None) else None)
        if content_type and content_type not in set(allowed_content_types):
            raise ValueError(f"Unexpected content type from Epic documentation: {content_type}")
        raw = resp.read(max_bytes + 1)
        if len(raw) > max_bytes:
            raise ValueError("Epic documentation response exceeded configured size limit.")
        return raw, final_url, content_type
