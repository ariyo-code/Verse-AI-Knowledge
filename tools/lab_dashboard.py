#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter,defaultdict

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"

q=json.loads(QUEUE.read_text(encoding="utf-8"))
entries=q.get("entries",[])
counts=Counter(x.get("queue_status","unknown") for x in entries)

order=[
    "pending","staged","compiling","compile-failed","blocked-environment",
    "compiled","runtime-pending","verified","multiplayer-verified","skipped"
]

done=sum(counts[x] for x in ["compiled","verified","multiplayer-verified"])
attempted=len(entries)-counts["pending"]

lines=[
    "# VerseLab Progress",
    "",
    f"Total candidates: **{len(entries)}**",
    f"Attempted: **{attempted}**",
    f"Locally compiled or better: **{done}**",
    "",
    "## Status",
    ""
]
for status in order:
    lines.append(f"- `{status}`: **{counts[status]}**")

lines += ["","## Compiled / verified",""]
for e in entries:
    if e.get("queue_status") in {"compiled","runtime-pending","verified","multiplayer-verified"}:
        lines += [
            f"### `{e['candidate_id']}` — {e['queue_status']}",
            f"- `{e['source_path']}`",
            f"- Compile attempts: {len(e.get('compile_attempts',[]))}",
            ""
        ]

lines += ["","## Failures requiring review",""]
for e in entries:
    if e.get("queue_status") in {"compile-failed","blocked-environment"}:
        lines += [
            f"### `{e['candidate_id']}` — {e['queue_status']}",
            f"- `{e['source_path']}`",
            f"- Classification: `{e.get('failure_classification')}`",
            ""
        ]

out=ROOT/"lab/PROGRESS.md"
out.write_text("\n".join(lines),encoding="utf-8")
print(out)
print(dict(counts))
