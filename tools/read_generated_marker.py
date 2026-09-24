#!/usr/bin/env python3
from pathlib import Path
import argparse,json,re
PAT=re.compile(r'<!--\s*verse-ai-provenance:v25;([^>]*)-->')
ap=argparse.ArgumentParser(); ap.add_argument('file'); args=ap.parse_args(); text=Path(args.file).read_text(encoding='utf-8'); out=[]
for m in PAT.finditer(text):
 d={'version':'v25'}
 for token in m.group(1).split(';'):
  if '=' in token:
   k,v=token.split('=',1); d[k.strip()]=v.strip()
 out.append(d)
print(json.dumps(out,indent=2,ensure_ascii=False)); raise SystemExit(0 if out else 2)
