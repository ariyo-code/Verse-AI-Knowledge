#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import re

PAT = re.compile(r"<!--\s*verse-ai-generated:v24;([^>]*)-->")
ap = argparse.ArgumentParser()
ap.add_argument("file")
args = ap.parse_args()

text = Path(args.file).read_text(encoding="utf-8")
out = []
for match in PAT.finditer(text):
    data = {"version": "v24"}
    for token in match.group(1).split(";"):
        if "=" in token:
            k, v = token.split("=", 1)
            data[k.strip()] = v.strip()
    out.append(data)

print(json.dumps(out, indent=2, ensure_ascii=False))
raise SystemExit(0 if out else 2)
