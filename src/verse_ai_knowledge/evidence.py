from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_evidence_graph(root: Path) -> dict[str, Any]:
    return json.loads((root / 'knowledge/api/evidence_graph.json').read_text(encoding='utf-8'))

def get_symbol_evidence(symbol: str, root: Path) -> dict[str, Any] | None:
    graph = load_evidence_graph(root)
    symbols = graph.get('symbols') or {}
    if symbol in symbols:
        return symbols[symbol]
    for key, value in symbols.items():
        if key.casefold() == symbol.casefold():
            return value
    return None
