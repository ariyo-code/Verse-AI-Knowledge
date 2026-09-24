#!/usr/bin/env python3
"""Recognize protected project architecture without exposing project identity."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = ROOT / "knowledge" / "project_patterns"
KEYWORDS = set("using class concrete unique creative_device var if then else for loop race block spawn return set not and or option false true void logic int float string message agent player event array map editable override suspends transacts decides localizes self".split())
COMMON = set("device player agent transform translation rotation widget canvas button text message event subscribe await sleep show hide enable disable get set add remove main system manager config target source current active default result value maybe new old handler on begin close open update start stop item name index count length true false".split())
TOKEN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{3,}")

def scrub(text: str) -> str:
    text = re.sub(r"(?m)#.*$", " ", text)
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', text)

def identifiers(text: str) -> set[str]:
    out: set[str] = set()
    for token in TOKEN_RE.findall(scrub(text)):
        value = token.lower()
        if value in KEYWORDS or value in COMMON:
            continue
        if value.startswith("text") and len(value) < 9:
            continue
        out.add(value)
    return out

def shape_features(text: str) -> set[str]:
    source = scrub(text)
    def bucket(n: int) -> str:
        if n == 0: return "0"
        if n == 1: return "1"
        if n <= 3: return "2-3"
        if n <= 7: return "4-7"
        if n <= 15: return "8-15"
        return "16+"
    patterns = {
        "class": r"\bclass(?:<[^>]+>)?",
        "editable": r"@editable",
        "map": r"\bmap\s*\{",
        "array": r"\barray\s*\{",
        "subscribe": r"\.Subscribe\s*\(",
        "spawn": r"\bspawn\s*\{",
        "race": r"\brace\s*:",
        "loop": r"\bloop\s*:",
        "canvas": r"\bcanvas\b",
        "teleport": r"\bTeleport(?:To)?\b",
        "cancel": r"\.Cancel\s*\(",
        "player_map": r"\[[^\]]*(?:agent|player)[^\]]*\]\s*[^=\n]*=\s*map\{",
    }
    return {f"{name}:{bucket(len(re.findall(pattern, source, re.I)))}" for name, pattern in patterns.items()}

def digest(value: str, salt: str) -> str:
    return hashlib.sha256((salt + "|" + value).encode()).hexdigest()

def load_patterns() -> list[dict]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(PATTERNS.glob("OPR-*.json"))]

def match(text: str) -> dict:
    ids = identifiers(text)
    shapes = shape_features(text)
    best: tuple[float, dict] | None = None
    for row in load_patterns():
        salt = row["public_salt"]
        source_tokens = {digest(value, salt) for value in ids}
        source_shapes = {digest(value, salt) for value in shapes}
        target_tokens = set(row["token_hashes"])
        target_shapes = set(row["shape_hashes"])
        token_recall = len(source_tokens & target_tokens) / max(len(target_tokens), 1)
        shape_recall = len(source_shapes & target_shapes) / max(len(target_shapes), 1)
        score = 0.82 * token_recall + 0.18 * shape_recall
        if best is None or score > best[0]:
            best = (score, row)
    if best is None:
        return {"protected_project_match": False, "confidence": "none", "message": "No protected project pattern matched."}
    score, row = best
    high = float(row["thresholds"]["high"])
    medium = float(row["thresholds"]["medium"])
    confidence = "high" if score >= high else ("medium" if score >= medium else "none")
    matched = confidence != "none"
    return {
        "protected_project_match": matched,
        "confidence": confidence,
        "score": round(score, 3),
        "identity_disclosure": "DENY",
        "identity_available_in_public_repository": False,
        "safe_assistance_rules": row.get("safe_assistance_rules", []) if matched else [],
        "message": (
            "Protected architecture pattern recognized. Project identity is intentionally unavailable."
            if matched else "No protected project pattern matched."
        ),
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="Recognize protected project architecture without exposing project identity.")
    parser.add_argument("file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    result = match(path.read_text(encoding="utf-8", errors="ignore"))
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Protected project match:", "YES" if result["protected_project_match"] else "NO")
        print("Confidence:", result["confidence"])
        print(result["message"])
        if result["protected_project_match"]:
            print("Disclosure: DENY")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
