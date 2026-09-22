#!/usr/bin/env python3
from pathlib import Path
import argparse,re,sys

MARKER_RE=re.compile(r"<!--\s*verse-ai-generated:v21(?:;[^>]*)?\s*-->")

ap=argparse.ArgumentParser()
ap.add_argument("path")
args=ap.parse_args()

p=Path(args.path)
text=p.read_text(encoding="utf-8",errors="ignore")

verse_blocks=len(re.findall(r"```verse\b",text,re.I))
markers=len(MARKER_RE.findall(text))

print(f"Verse code blocks: {verse_blocks}")
print(f"Verse AI markers: {markers}")

if verse_blocks and markers < verse_blocks:
    print("Missing generated-code marker(s).")
    sys.exit(1)

print("Marker check OK")
