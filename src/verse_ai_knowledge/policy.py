from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SOURCE_TRUST = ('official-current', 'official-stale', 'signature-verified', 'api-page-verified', 'community-verified', 'community-unverified', 'external-compiler-claimed', 'reference-only', 'deprecated', 'unknown')
VALIDATION = ('draft', 'static-checked', 'compiled', 'verified', 'multiplayer-verified')
LEGACY_TRUST_ALIASES = {'module-index-verified': 'official-current', 'official-guide-presence-verified': 'official-current', 'external-community': 'community-unverified', 'unspecified': 'unknown', 'official': 'official-current', 'verified': 'community-verified'}

def repo_root(start: Path | None=None) -> Path:
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / 'manifest.json').exists() and (candidate / 'AGENTS.md').exists():
            return candidate
    packaged = Path(__file__).resolve().parents[2]
    if (packaged / 'manifest.json').exists():
        return packaged
    raise RuntimeError('Verse AI Knowledge repository root not found.')

def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))

def canonical_source_trust(value: str | None) -> str:
    if not value:
        return 'unknown'
    v = str(value).strip().lower()
    if v in SOURCE_TRUST:
        return v
    return LEGACY_TRUST_ALIASES.get(v, 'unknown')

def canonical_validation(value: str | None) -> str:
    if not value:
        return 'draft'
    v = str(value).strip().lower()
    return v if v in VALIDATION else 'draft'

def validation_from_checks(checks: dict[str, Any] | None, fallback: str | None=None) -> str:
    checks = checks or {}
    compiled = bool(checks.get('compiled'))
    runtime = bool(checks.get('runtime_tested'))
    multiplayer = bool(checks.get('multiplayer_tested'))
    if compiled and runtime and multiplayer:
        return 'multiplayer-verified'
    if compiled and runtime:
        return 'verified'
    if compiled:
        return 'compiled'
    if fallback == 'discovered':
        return 'static-checked'
    return canonical_validation(fallback)

def exact_signature_allowed(symbol: dict[str, Any]) -> bool:
    return bool(symbol.get('signature') and symbol.get('exact_signature_claim_allowed') and (canonical_source_trust(symbol.get('source_trust')) in {'signature-verified', 'api-page-verified'}))
