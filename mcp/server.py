#!/usr/bin/env python3
"""Official MCP Python SDK server for Verse AI Knowledge.

Install the optional dependency with ``pip install -e '.[mcp]'`` and run with
``python mcp/server.py`` (stdio) or ``mcp run mcp/server.py:mcp``.

The server is read-only. Exact Verse API claims are delegated to the same
field-level claim resolver used by the CLI and SDK; unsupported exact claims
remain ``TODO(API VERIFY)``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    from mcp.server import MCPServer
except ImportError as exc:  # pragma: no cover - optional dependency
    raise SystemExit("MCP SDK not installed. Run: python -m pip install -e '.[mcp]'") from exc

from verse_ai_knowledge import KnowledgeBase

kb = KnowledgeBase(ROOT)
mcp = MCPServer("Verse AI Knowledge")


@mcp.tool()
def search_knowledge(query: str, limit: int = 12) -> list[dict[str, Any]]:
    """Retrieve relevant repository knowledge. Retrieval score is not proof."""
    return kb.search(query, limit)


@mcp.tool()
def get_api_symbol(symbol: str) -> dict[str, Any]:
    """Return one known structured API symbol, or an explicit unresolved result."""
    row = kb.lookup_api(symbol)
    return row or {"symbol": symbol, "decision": "TODO(API VERIFY)"}


@mcp.tool()
def resolve_api_claim(symbol: str, field: str = "presence") -> dict[str, Any]:
    """Resolve one field-level Verse API claim against recorded evidence."""
    return kb.resolve_claim(symbol, field)


@mcp.tool()
def get_evidence(symbol: str) -> dict[str, Any]:
    """Return evidence recorded for a symbol without inferring missing fields."""
    row = kb.get_evidence(symbol)
    return row or {"symbol": symbol, "decision": "TODO(API VERIFY)"}


@mcp.tool()
def get_api_coverage() -> dict[str, Any]:
    """Return measured coverage for repository-known structured symbols."""
    return kb.get_coverage()


@mcp.tool()
def get_verification_queue(limit: int = 30) -> dict[str, Any]:
    """Return API fields waiting for review/verification."""
    return kb.get_verification_queue(limit)


@mcp.tool()
def search_errors(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search only real recorded error-memory entries."""
    return kb.search_errors(query, limit)


@mcp.tool()
def get_project_context(query: str, limit: int = 10) -> list[dict[str, Any]]:
    """Search project-memory records; actual project files remain authoritative."""
    return kb.get_project_context(query, limit)


@mcp.tool()
def get_routing() -> str:
    """Return the repository routing rules."""
    return kb.get_routing()


@mcp.tool()
def validate_generated_claims(claims_json: str) -> dict[str, Any]:
    """Validate explicit API claims encoded as a JSON array of symbol/field objects."""
    data = json.loads(claims_json)
    if not isinstance(data, list):
        raise ValueError("claims_json must decode to a JSON array")
    return kb.validate_generated_claims(data)


if __name__ == "__main__":
    mcp.run()
