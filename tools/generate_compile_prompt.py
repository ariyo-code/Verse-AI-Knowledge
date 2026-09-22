#!/usr/bin/env python3
from pathlib import Path
import argparse,json

ROOT=Path(__file__).resolve().parents[1]
QUEUE=ROOT/"lab/compile_queue.json"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("candidate_id")
    ap.add_argument("--output",default="lab/generated/COMPILE_CANDIDATE.md")
    args=ap.parse_args()

    q=json.loads(QUEUE.read_text(encoding="utf-8"))
    e=next((x for x in q["entries"] if x["candidate_id"]==args.candidate_id),None)
    if not e:
        raise SystemExit("Candidate not found.")

    text=f"""# UEFN MCP Compile Candidate

Candidate: `{e['candidate_id']}`

Source: `{e['source_id']} / {e['source_path']}`

Upstream status: `{e['upstream_status']}`

## Objective

Determine whether this exact candidate compiles in the current local UEFN environment.

## Rules

1. Read the staged candidate without rewriting it first.
2. Discover the available UEFN MCP compile tools.
3. Attempt a real Verse build.
4. Preserve exact compiler output.
5. Do not call an environment/dependency problem a language/API failure.
6. Classify the result as one of:
   - compile success
   - syntax/language failure
   - API/version failure
   - missing dependency
   - project/environment block
   - unknown failure
7. Record the result with `tools/record_uefn_compile.py`.
8. Do not silently fix the source before the first result is recorded.

If compilation succeeds, it may be promoted locally to `compiled`.
Runtime behavior remains unverified until playtested.
"""
    out=ROOT/args.output
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(text,encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
