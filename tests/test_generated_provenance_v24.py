#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
forbidden = ("\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\u202e", "\u2066", "\u2067", "\u2068", "\u2069")

with tempfile.TemporaryDirectory() as td:
    code = Path(td) / "x.verse"
    code.write_text("test := class:\n    # TODO(API VERIFY)\n", encoding="utf-8")
    output = subprocess.check_output(
        [sys.executable, str(ROOT / "tools/stamp_generated_code.py"), str(code)],
        text=True,
    )
    assert "Verse AI Knowledge · V24" in output
    assert "verse-ai-generated:v24" in output
    assert "claim_resolution=field-level" in output
    assert "api_verify_required=true" in output
    assert "uncertain_api_count=1" in output
    assert not any(ch in output for ch in forbidden)

    md = Path(td) / "x.md"
    md.write_text(output, encoding="utf-8")
    rc = subprocess.run([sys.executable, str(ROOT / "tools/check_generated_marker.py"), str(md)]).returncode
    assert rc == 0

print("V24 generated provenance tests OK")
