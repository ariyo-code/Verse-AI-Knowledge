#!/usr/bin/env python3
from pathlib import Path
import argparse,json

def main():
    p=argparse.ArgumentParser()
    p.add_argument("run_json")
    args=p.parse_args()

    data=json.loads(Path(args.run_json).read_text(encoding="utf-8"))
    rows=[]
    total=0
    max_total=0
    for t in data.get("tasks",[]):
        score=sum([
            t.get("static_score",0),
            t.get("compile_score",0),
            t.get("runtime_score",0),
            t.get("multiplayer_score",0)
        ])
        rows.append((t.get("task_id"),score))
        total+=score
        max_total+=100

    print("Run:",data.get("run_id"))
    print("Agent:",data.get("model_or_agent"))
    for tid,score in rows:
        print(f"- {tid}: {score}/100")
    if rows:
        print(f"Average: {total/len(rows):.1f}/100")
    else:
        print("No task results.")

if __name__=="__main__":
    main()
