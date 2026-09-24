from pathlib import Path
import contextlib,io,sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from verse_ai_knowledge.cli import parser,cmd_api,cmd_claim,cmd_doctor,version_data
def test_parser_commands():
    p=parser()
    for argv in [["version"],["explain","GetFortCharacter"],["evidence","GetFortCharacter"],["status"],["api-diff","a.json","b.json"],["snapshot"],["doctor"]]: assert p.parse_args(argv).cmd
def test_unknown_api_is_todo():
    b=io.StringIO()
    with contextlib.redirect_stdout(b): rc=cmd_api(ROOT,"definitely_fake_api")
    assert rc==2 and "TODO(API VERIFY)" in b.getvalue()
def test_known_claim_and_doctor():
    with contextlib.redirect_stdout(io.StringIO()):
        assert cmd_claim(ROOT,"GetFortCharacter","signature",False)==0; assert cmd_doctor(ROOT,False)==0
def test_version():
    assert version_data(ROOT)["knowledge_release"]=="25.0.0"
