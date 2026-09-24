from __future__ import annotations
import json
from pathlib import Path
class SavedResponsesProvider:
    def __init__(self,path:str|Path): self.data=json.loads(Path(path).read_text(encoding="utf-8"))
    def generate(self,prompt:str)->str:
        if prompt not in self.data: raise KeyError("No saved response for prompt")
        return self.data[prompt]
