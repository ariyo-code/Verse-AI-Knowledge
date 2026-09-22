#!/usr/bin/env python3
from pathlib import Path
import argparse, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--budget",type=int,default=16000)
    args=p.parse_args()

    cmd=[
        sys.executable,
        str(ROOT/"tools/rag_context_pack.py"),
        args.query,
        "--budget",str(args.budget),
        "--output",str(ROOT/"bridge/generated/PROJECT_TASK_CONTEXT.md")
    ]

    proc=subprocess.run(cmd,capture_output=True,text=True)

    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr,file=sys.stderr)

    raise SystemExit(proc.returncode)

if __name__=="__main__":
    main()
