from __future__ import annotations
import re
MARKER_RE=re.compile(r'<!--\s*verse-ai-provenance:v25;([^>]*)-->')
def parse_markers(text:str)->list[dict[str,str]]:
    out=[]
    for match in MARKER_RE.finditer(text):
        row={'version':'v25'}
        for token in match.group(1).split(';'):
            if '=' in token:
                k,v=token.split('=',1); row[k.strip()]=v.strip()
        out.append(row)
    return out
