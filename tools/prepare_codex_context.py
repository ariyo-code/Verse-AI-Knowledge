#!/usr/bin/env python3
from pathlib import Path
import argparse,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(); p.add_argument('task'); p.add_argument('--budget',type=int,default=18000); a=p.parse_args()
    out=ROOT/'rag/generated/CODEX_CONTEXT.md'; out.parent.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run([sys.executable,str(ROOT/'tools/rag_context_pack.py'),a.task,'--budget',str(a.budget),'--output',str(out)],capture_output=True,text=True)
    if proc.returncode!=0: print(proc.stdout); print(proc.stderr,file=sys.stderr); raise SystemExit(proc.returncode)
    prompt=ROOT/'rag/generated/CODEX_TASK.md'; prompt.write_text('# Codex Task — V22\n\nRead `AI_BOOTSTRAP.md`, then `AGENTS.md`, then `rag/generated/CODEX_CONTEXT.md`.\n\n## Requested task\n\n'+a.task+'\n\n## Required workflow\n\n1. Route and retrieve before assuming.\n2. Keep source trust separate from local validation.\n3. Make the smallest coherent change.\n4. Use `TODO(API VERIFY)` for unsupported exact API claims.\n5. Compile with UEFN only when actually available.\n6. Never claim compile/runtime/multiplayer validation without evidence.\n',encoding='utf-8'); print(prompt); print(out)
if __name__=='__main__': main()
