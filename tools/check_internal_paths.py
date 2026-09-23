#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []

manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
PATH_EXT = re.compile(r"\.(?:md|json|jsonl|py|yml|yaml|txt|toml|ps1|bat)$", re.I)

def walk(value):
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)
    elif isinstance(value, str):
        yield value

for value in walk(manifest):
    if "://" in value or value.startswith("verse-ai") or "\n" in value or "{" in value:
        continue
    if value.endswith("/") or PATH_EXT.search(value):
        # Do not interpret human sentences as paths.
        if " " in value and "/" not in value:
            continue
        target = ROOT / value
        if not target.exists():
            errors.append(f"manifest path does not exist: {value}")

LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    if any(part in {".git", "external"} for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for dest in LINK_RE.findall(text):
        dest = dest.strip().split("#", 1)[0]
        if not dest or "://" in dest or dest.startswith("mailto:") or dest.startswith("#"):
            continue
        # GitHub-style links can carry optional titles; use the first token unless quoted path.
        dest = dest.strip("<>")
        candidate = (path.parent / dest).resolve()
        try:
            candidate.relative_to(ROOT.resolve())
        except ValueError:
            continue
        if not candidate.exists():
            errors.append(f"{path.relative_to(ROOT)}: dead relative link -> {dest}")

if errors:
    print("Internal path validation FAILED")
    for error in sorted(set(errors)):
        print("-", error)
    raise SystemExit(1)

print("Internal path validation OK")
