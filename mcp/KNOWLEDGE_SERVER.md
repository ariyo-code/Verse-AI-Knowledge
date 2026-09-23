# Optional MCP Knowledge Server — V22 design

This is a **knowledge/retrieval MCP**, not the MCP connection that controls UEFN. The responsibilities must remain separate.

Proposed read-oriented tools:

- `search_verse_knowledge`
- `lookup_verse_api`
- `lookup_verse_module`
- `find_verified_example`
- `search_verse_errors`
- `get_project_context`
- `build_evidence_pack`
- `check_api_claim`

Each result should expose, where relevant:

```text
source
source_trust
verse_api_version
validation
validation_evidence
```

V22 documents this contract but does not require an MCP server implementation for repository correctness.
