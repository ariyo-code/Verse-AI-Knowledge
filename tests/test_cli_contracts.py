#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]

checks={
    "tools/scan_verse_project.py":["--output"],
    "tools/corpus_coverage.py":["--json"],
    "tools/analyze_verse_dependencies.py":["--output"],
    "tools/rag_context_compiler.py":["--output"],
    "tools/build_claim_ledger.py":["--evidence","--output"],
}

errors=[]
for rel,flags in checks.items():
    p=ROOT/rel
    if not p.exists():
        errors.append(f"missing: {rel}")
        continue
    text=p.read_text(encoding="utf-8",errors="ignore")
    for flag in flags:
        if flag not in text:
            errors.append(f"{rel}: missing CLI flag {flag}")

if errors:
    print("CLI contract tests FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)

print("CLI contract tests OK")
