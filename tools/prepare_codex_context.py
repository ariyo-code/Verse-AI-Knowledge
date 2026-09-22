#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("task")
    p.add_argument("--budget",type=int,default=18000)
    args=p.parse_args()

    out=ROOT/"rag/generated/CODEX_CONTEXT.md"
    out.parent.mkdir(parents=True,exist_ok=True)

    cmd=[
        sys.executable,
        str(ROOT/"tools/rag_context_pack.py"),
        args.task,
        "--budget",str(args.budget),
        "--output",str(out)
    ]
    proc=subprocess.run(cmd,capture_output=True,text=True)
    if proc.returncode!=0:
        print(proc.stdout)
        print(proc.stderr,file=sys.stderr)
        raise SystemExit(proc.returncode)

    prompt=ROOT/"rag/generated/CODEX_TASK.md"
    prompt.write_text(
        "# Codex Task\n\n"
        "Read `AGENTS.md` first.\n"
        "Then read `rag/generated/CODEX_CONTEXT.md`.\n\n"
        "## Requested task\n\n"
        f"{args.task}\n\n"
        "## Required workflow\n\n"
        "1. Retrieve/inspect actual project files before assuming project state.\n"
        "2. Produce a short plan.\n"
        "3. Make the smallest coherent change.\n"
        "4. Compile with UEFN MCP when available.\n"
        "5. Use exact compiler feedback to fix issues.\n"
        "6. Runtime-test when behavior cannot be proven statically.\n"
        "7. Do not mark anything verified without evidence.\n",
        encoding="utf-8"
    )

    print(prompt)
    print(out)

if __name__=="__main__":
    main()
