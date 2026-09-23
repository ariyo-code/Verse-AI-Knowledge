#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.policy import canonical_source_trust, canonical_validation  # noqa: E402

CONFIG = json.loads((ROOT / "rag/config.json").read_text(encoding="utf-8"))
ALLOWED = {".md", ".json", ".jsonl", ".verse", ".py", ".yml", ".yaml", ".toml"}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_./<>:-]+", text.lower())


def extract_title(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def first_match(text: str, patterns: list[str]) -> str | None:
    for pat in patterns:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1).strip().lower()
    return None


def detect_source_trust(text: str) -> tuple[str, str | None]:
    explicit = first_match(text, [r'"source_trust"\s*:\s*"([^"]+)"', r"\bsource_trust\s*:\s*`?([a-zA-Z0-9_-]+)"])
    if explicit:
        return canonical_source_trust(explicit), None
    legacy_verification = first_match(text, [r'"verification"\s*:\s*"([^"]+)"', r"\*\*Vérification\s*:\*\*\s*`?([^`\n]+)"])
    legacy_status = first_match(text, [r'"status"\s*:\s*"([^"]+)"', r"\bstatus\s*:\s*`?([a-zA-Z0-9_-]+)"])
    value = legacy_verification or legacy_status
    return canonical_source_trust(value), value


def detect_validation(text: str) -> str:
    explicit = first_match(text, [r'"validation"\s*:\s*"([^"]+)"', r"\bvalidation\s*:\s*`?([a-zA-Z0-9_-]+)"])
    if explicit:
        return canonical_validation(explicit)
    legacy_status = first_match(text, [r'"status"\s*:\s*"([^"]+)"', r"\bstatus\s*:\s*`?([a-zA-Z0-9_-]+)"])
    return canonical_validation(legacy_status)


def detect_version(text: str) -> str | None:
    m = re.search(r"\b(?:verse_api|Verse API(?: version)?|verse api snapshot|api_version)\b[^0-9]{0,20}([0-9]{2}\.[0-9]{2})", text, re.I)
    return m.group(1) if m else None


def external_trust_for_path(path: Path) -> str | None:
    parts = path.parts
    try:
        idx = parts.index("corpus")
    except ValueError:
        return None
    if len(parts) <= idx + 2:
        return None
    provenance = ROOT.joinpath(*parts[: idx + 3]) / "PROVENANCE.json"
    if not provenance.exists():
        return "community-unverified"
    try:
        return canonical_source_trust(json.loads(provenance.read_text(encoding="utf-8")).get("trust"))
    except Exception:
        return "community-unverified"


def detect_api_symbols(text: str) -> list[str]:
    vals = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_.]*)`", text))
    vals.update(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*(?:_device|_component|_ui|_character|_vehicle|_collection))\b", text))
    return sorted(vals)


def main() -> None:
    catalog_path = ROOT / "knowledge/api_catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8")).get("entries", {}) if catalog_path.exists() else {}
    docs = []
    df: Counter[str] = Counter()

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in ALLOWED:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel.startswith("rag/index"):
            continue
        if any(rel.startswith(x) for x in CONFIG.get("excluded_paths", [])):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        tokens = tokenize(text)
        tf = Counter(tokens)
        for token in tf:
            df[token] += 1
        symbols = set(detect_api_symbols(text))
        for name in catalog:
            if name in text:
                symbols.add(name)

        trust, evidence_basis = detect_source_trust(text)
        external = external_trust_for_path(path.relative_to(ROOT))
        if external:
            trust = external
        doc = {
            "id": hashlib.sha1(rel.encode()).hexdigest()[:16],
            "path": rel,
            "title": extract_title(text, path),
            "extension": path.suffix.lower(),
            "size_chars": len(text),
            "token_count": len(tokens),
            "term_freq": dict(tf),
            "source_trust": trust,
            "validation": detect_validation(text),
            "evidence_basis": evidence_basis,
            "verse_api": detect_version(text),
            "api_symbols": sorted(symbols),
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        }
        docs.append(doc)

    avgdl = sum(x["token_count"] for x in docs) / max(len(docs), 1)
    index = {
        "schema_version": 2,
        "document_count": len(docs),
        "avg_document_length": avgdl,
        "document_frequency": dict(df),
        "documents": docs,
    }
    out = ROOT / "rag/index.json"
    out.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Indexed {len(docs)} document(s) with V24 source-trust, validation and claim-evidence metadata.")


if __name__ == "__main__":
    main()
