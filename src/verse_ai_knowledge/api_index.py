from __future__ import annotations

import difflib
import json
from pathlib import Path
from typing import Any

from .policy import repo_root


def symbols_path(root: Path | None = None) -> Path:
    return (root or repo_root()) / "knowledge" / "api" / "symbols.jsonl"


def load_symbols(root: Path | None = None) -> list[dict[str, Any]]:
    path = symbols_path(root)
    if not path.exists():
        raise FileNotFoundError(f"Missing generated API symbol index: {path}. Run tools/migrate_api_catalog_v24.py")
    rows: list[dict[str, Any]] = []
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{n}: {exc}") from exc
    return rows


def lookup(name: str, root: Path | None = None) -> tuple[dict[str, Any] | None, list[str]]:
    rows = load_symbols(root)
    by_key: dict[str, dict[str, Any]] = {}
    for row in rows:
        for key in {str(row.get("name", "")), str(row.get("symbol_id", "")), str(row.get("qualified_name") or "")}:
            if key:
                by_key.setdefault(key.casefold(), row)
    exact = by_key.get(name.casefold())
    if exact:
        return exact, []
    names = sorted({str(x.get("name")) for x in rows if x.get("name")})
    return None, difflib.get_close_matches(name, names, n=8, cutoff=0.35)
