#!/usr/bin/env python3
from pathlib import Path
import contextlib,io,sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.cli import build_parser,cmd_api,cmd_doctor
p=build_parser()
for args in [['search','vehicle ownership'],['context','phone ui'],['api','GetFortCharacter'],['coverage'],['api-queue'],['provenance','stamp','README.md'],['provenance','read','README.md'],['provenance','check','README.md'],['errors','x'],['project','scan','.'],['verify','README.md'],['lab','next'],['lab','status'],['maintenance','check'],['doctor'],['validate']]:
 ns=p.parse_args(args); assert ns.cmd
buf=io.StringIO()
with contextlib.redirect_stdout(buf): rc=cmd_api(ROOT,'definitely_not_a_real_verse_api_symbol')
assert rc==2 and 'TODO(API VERIFY)' in buf.getvalue()
with contextlib.redirect_stdout(io.StringIO()): assert cmd_doctor(ROOT)==0
print('V23 CLI tests OK')
