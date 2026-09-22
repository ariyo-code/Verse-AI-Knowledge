#!/usr/bin/env python3
from maintenance_lib import load_json

def main():
    q=load_json("maintenance/revalidation_queue.json")
    print("Revalidation queue")
    print("Baseline:",q.get("baseline_version"))
    print("Detected:",q.get("detected_version"))
    print("Items:",len(q.get("items",[])))
    print()
    for i,item in enumerate(q.get("items",[]),start=1):
        print(f"{i}. [{item.get('priority')}] {item.get('reason')}")
        print("   source:",item.get("source_url"))
        files=item.get("impacted_files",[])
        if files:
            print("   impacted:")
            for f in files[:12]:
                print("    -",f)
            if len(files)>12:
                print(f"    ... +{len(files)-12}")
        print()

if __name__=="__main__":
    main()
