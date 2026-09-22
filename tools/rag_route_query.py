#!/usr/bin/env python3
import json,re,sys

ROUTES={
    "api":[
        "api","device","function","class","interface","module","signature",
        "effect","decides","transacts","using","import"
    ],
    "project":[
        "system","project","architecture","vehicle manager","inventory","phone",
        "staff","economy","whitelist","session","hud","rp"
    ],
    "error":[
        "error","erreur","compiler","runtime","failed","failure","exception",
        "does not compile","ne compile"
    ],
    "ui":[
        "ui","widget","hud","canvas","overlay","button","text_block","player_ui"
    ],
    "vehicle":[
        "vehicle","vehicule","véhicule","driver","seat","fort_vehicle","car"
    ],
    "persistence":[
        "persistence","persist","weak_map","save","load","migration","persistent"
    ],
    "async":[
        "race","spawn","suspends","async","concurrency","concurrent","task","await"
    ],
    "mcp":[
        "mcp","uefn","compile","playtest","session","logs","editor"
    ],
    "maintenance":[
        "release","version","deprecated","deprecation","update","42.","maintenance",
        "revalidate","revalidation"
    ]
}

def route(query):
    q=query.lower()
    scores={}
    for name,terms in ROUTES.items():
        score=0
        for term in terms:
            if term in q:
                score+=3 if " " in term else 1
        if score:
            scores[name]=score
    return [x[0] for x in sorted(scores.items(),key=lambda x:(-x[1],x[0]))]

if __name__=="__main__":
    q=" ".join(sys.argv[1:])
    print(json.dumps({"query":q,"routes":route(q)},ensure_ascii=False))
