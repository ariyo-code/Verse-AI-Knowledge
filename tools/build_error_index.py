#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter
from error_memory_lib import read_entries

ROOT=Path(__file__).resolve().parents[1]
entries=read_entries()
summary={
    "count":len(entries),
    "by_status":dict(Counter(x.get("status","unknown") for x in entries)),
    "by_category":dict(Counter(x.get("category","unknown") for x in entries)),
    "ids":[x.get("id") for x in entries],
}
(ROOT/"errors/error_index.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(summary,indent=2,ensure_ascii=False))
