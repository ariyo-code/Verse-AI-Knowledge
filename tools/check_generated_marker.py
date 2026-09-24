#!/usr/bin/env python3
from pathlib import Path
import argparse,re
PAT=re.compile(r'<!--\s*verse-ai-provenance:v25;([^>]*)-->'); STATUS={'draft','static-checked','compiled','verified','multiplayer-verified'}
FORBIDDEN=('\u200b','\u200c','\u200d','\u2060','\ufeff','\u202a','\u202b','\u202c','\u202d','\u202e','\u2066','\u2067','\u2068','\u2069')
as_bool=lambda v:str(v).lower()=='true'
ap=argparse.ArgumentParser(); ap.add_argument('file',nargs='?'); args=ap.parse_args(); files=[Path(args.file)] if args.file else list(Path('.').rglob('*.md')); errors=[]; found=0
for path in files:
 text=path.read_text(encoding='utf-8',errors='ignore')
 for ch in FORBIDDEN:
  if ch in text: errors.append(f'{path}: forbidden invisible/bidi Unicode U+{ord(ch):04X}')
 for i,m in enumerate(PAT.finditer(text),1):
  found+=1; before=text[max(0,m.start()-4000):m.start()]
  if 'Verse AI Knowledge · V25' not in before: errors.append(f'{path}: marker {i}: visible V25 provenance block missing')
  d={}
  for tok in m.group(1).split(';'):
   if '=' in tok:
    k,v=tok.split('=',1); d[k.strip()]=v.strip()
  status=d.get('status'); comp=as_bool(d.get('compiled')); run=as_bool(d.get('runtime')); multi=as_bool(d.get('multiplayer'))
  try: uncertain=int(d.get('uncertain_api_count','0') or 0)
  except ValueError: errors.append(f'{path}: marker {i}: invalid uncertain_api_count'); uncertain=0
  if status not in STATUS: errors.append(f'{path}: marker {i}: invalid status {status}')
  if status in {'compiled','verified','multiplayer-verified'} and not comp: errors.append(f'{path}: marker {i}: {status} requires compiled=true')
  if status in {'verified','multiplayer-verified'} and not run: errors.append(f'{path}: marker {i}: {status} requires runtime=true')
  if status=='multiplayer-verified' and not multi: errors.append(f'{path}: marker {i}: multiplayer requires multiplayer=true')
  if run and not comp: errors.append(f'{path}: marker {i}: runtime=true requires compiled=true')
  if multi and not run: errors.append(f'{path}: marker {i}: multiplayer=true requires runtime=true')
  if uncertain>0 and d.get('api_verify_required')!='true': errors.append(f'{path}: marker {i}: unresolved APIs require warning')
  if d.get('claim_resolution')!='field-level': errors.append(f'{path}: marker {i}: claim_resolution must be field-level')
if errors:
 print('Generated marker validation FAILED'); [print('-',e) for e in errors]; raise SystemExit(1)
print(f'Generated marker validation OK ({found} V25 marker(s) inspected)')
