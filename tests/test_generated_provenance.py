#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'x.verse'; p.write_text('test := class:\n    # TODO(API VERIFY)\n',encoding='utf-8')
 out=subprocess.check_output([sys.executable,str(ROOT/'tools/stamp_generated_code.py'),str(p)],text=True)
 assert 'Verse AI Knowledge · V23' in out; assert 'verse-ai-generated:v23' in out; assert 'api_verify_required=true' in out; assert 'uncertain_api_count=1' in out
 md=Path(td)/'x.md'; md.write_text(out,encoding='utf-8'); rc=subprocess.run([sys.executable,str(ROOT/'tools/check_generated_marker.py'),str(md)]).returncode; assert rc==0
print('V23 generated provenance tests OK')
