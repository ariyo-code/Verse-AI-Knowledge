#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EXT = {".md", ".txt", ".json", ".jsonl", ".py", ".yml", ".yaml", ".toml", ".ps1", ".bat", ".verse"}
SKIP_DIRS = {".git", "__pycache__"}
SKIP_FILES = {"tools/scan_secrets.py"}

PATTERNS = [
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-pat", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("openai-style-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{28,}\b")),
    ("discord-token", re.compile(r"\b[A-Za-z0-9_-]{24,}\.[A-Za-z0-9_-]{6}\.[A-Za-z0-9_-]{25,}\b")),
    ("credentialed-db-url", re.compile(r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?)://[^/\s:@]+:[^@\s/]+@")),
    ("auth-bearer", re.compile(r"(?i)\bAuthorization\s*[:=]\s*[\"']?Bearer\s+[A-Za-z0-9._~-]{24,}")),
]

findings = []
for path in ROOT.rglob("*"):
    if not path.is_file() or path.suffix.lower() not in ALLOWED_EXT:
        continue
    rel = str(path.relative_to(ROOT)).replace("\\", "/")
    if rel in SKIP_FILES or any(part in SKIP_DIRS for part in path.parts):
        continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    for label, pattern in PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            findings.append((rel, line, label))

if findings:
    print("Secret scan FAILED")
    for rel, line, label in findings:
        print(f"- {rel}:{line}: possible {label} (value redacted)")
    print("Rotate/revoke any real exposed credential. Removing it from the latest commit does not erase Git history.")
    raise SystemExit(1)

print("Secret scan OK — no high-confidence credential pattern detected")
print("This scan does not prove that Git history never contained a secret.")
