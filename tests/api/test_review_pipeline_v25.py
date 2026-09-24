from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
def test_review_requires_explicit_values_for_claimed_fields():
    p=subprocess.run([sys.executable,str(ROOT/'tools/review_api_candidate.py'),'GetFortCharacter','--source-url','https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/characters/getfortcharacter','--fields','parameters'],cwd=ROOT,capture_output=True,text=True)
    assert p.returncode != 0
    assert 'explicit value' in (p.stdout+p.stderr)
