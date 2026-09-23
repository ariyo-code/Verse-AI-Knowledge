#!/usr/bin/env python3
from pathlib import Path
import contextlib
import io
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verse_ai_knowledge.cli import build_parser, cmd_api, cmd_claim, cmd_doctor  # noqa: E402

parser = build_parser()
cases = [
    ["search", "vehicle ownership"],
    ["context", "phone ui"],
    ["api", "GetFortCharacter"],
    ["claim", "GetFortCharacter", "--field", "signature"],
    ["lint", "README.md"],
    ["coverage"],
    ["api-queue"],
    ["coverage-snapshot"],
    ["coverage-diff", "a.json", "b.json"],
    ["api-revalidation"],
    ["provenance", "stamp", "README.md"],
    ["provenance", "read", "README.md"],
    ["provenance", "check", "README.md"],
    ["llm-eval"],
    ["errors", "x"],
    ["project", "scan", "."],
    ["verify", "README.md"],
    ["lab", "next"],
    ["lab", "status"],
    ["maintenance", "check"],
    ["doctor"],
    ["validate"],
]
for args in cases:
    ns = parser.parse_args(args)
    assert ns.cmd

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = cmd_api(ROOT, "definitely_not_a_real_verse_api_symbol")
assert rc == 2
assert "TODO(API VERIFY)" in buf.getvalue()

with contextlib.redirect_stdout(io.StringIO()):
    assert cmd_claim(ROOT, "GetFortCharacter", "signature", False) == 0
    assert cmd_claim(ROOT, "button_device", "signature", False) == 2
    assert cmd_doctor(ROOT) == 0

print("V24 CLI tests OK")
