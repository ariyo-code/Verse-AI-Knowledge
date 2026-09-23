#!/usr/bin/env python3
"""Conservative static API-reference review. Unknowns are verification requests, not proof of hallucination."""
from pathlib import Path
import argparse,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from verse_ai_knowledge.api_index import load_symbols
symbols=load_symbols(ROOT); known={x.get('symbol_id') for x in symbols}|{x.get('name') for x in symbols}
modules=json.loads((ROOT/'knowledge/api/modules.json').read_text(encoding='utf-8')); known_modules={f'/{domain}/{module}' for domain,mods in modules.get('top_level',{}).items() for module in mods}
TYPE_RE=re.compile(r'\b([A-Za-z_][A-Za-z0-9_]*(?:_device|_component|_ui|_character|_vehicle|_collection))\b')
USING_RE=re.compile(r'using\s*\{\s*([^}]+)\s*\}')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('file'); a=ap.parse_args(); path=Path(a.file); text=path.read_text(encoding='utf-8',errors='ignore')
    candidates=sorted(set(TYPE_RE.findall(text))); unknown=[x for x in candidates if x not in known]
    imports=sorted(set(x.strip() for x in USING_RE.findall(text))); unknown_imports=[x for x in imports if x not in known_modules]
    print(f'API-like candidates: {len(candidates)}')
    if unknown:
        print('Needs API verification (not proof of hallucination):')
        for x in unknown: print('-',x,'-> TODO(API VERIFY)')
    if unknown_imports:
        print('Imports/modules needing verification:')
        for x in unknown_imports: print('-',x,'-> TODO(API VERIFY)')
    if not unknown and not unknown_imports: print('No catalog-missing API-like identifiers or module imports detected.')
if __name__=='__main__': main()
