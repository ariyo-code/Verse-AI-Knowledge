# MCP Knowledge Server — V25

V25 exposes the repository through an actual **Model Context Protocol** server using the official Python SDK when the optional `mcp` dependency is installed.

```bash
python -m pip install -e ".[mcp]"
python mcp/server.py
```

The default transport is stdio. The server is read-only and exposes:

- `search_knowledge`
- `get_api_symbol`
- `resolve_api_claim`
- `get_evidence`
- `get_api_coverage`
- `get_verification_queue`
- `search_errors`
- `get_project_context`
- `get_routing`
- `validate_generated_claims`

`resolve_api_claim` uses the canonical field-level resolver. An absent or unsupported exact API claim returns `TODO(API VERIFY)` rather than being inferred.

## Validation boundary

Installing/running the MCP server does not constitute UEFN compilation, runtime testing, or multiplayer verification.
