from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(ROOT/"src"))
from verse_ai_knowledge import KnowledgeBase
def test_sdk_claim_boundary():
    kb=KnowledgeBase(ROOT); assert kb.resolve_claim("definitely_fake_api","signature")["decision"]=="TODO(API VERIFY)"
def test_sdk_coverage():
    kb=KnowledgeBase(ROOT); assert kb.get_coverage()["symbol_count"]>=1
