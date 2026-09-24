from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def test_data_instruction_boundary_documented():
    text=(ROOT/"docs/security/PROMPT_INJECTION.md").read_text(encoding="utf-8").lower()
    assert "data" in text and "not instructions" in text
    assert "epic documentation" in text
