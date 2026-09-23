# Optional MCP Knowledge Server — V24 contract

This is a knowledge/retrieval MCP concept, not the MCP connection that controls UEFN.

Suggested read-oriented tools:

- `search_verse_knowledge`
- `lookup_verse_api`
- `lookup_verse_module`
- `resolve_verse_api_claim`
- `lint_verse_api_claims`
- `get_api_coverage`
- `get_api_evidence_graph`
- `get_api_revalidation_state`
- `get_api_verification_queue`
- `find_verified_example`
- `search_verse_errors`
- `get_project_context`
- `build_evidence_pack`
- `read_generated_provenance`

Each API result should expose, when relevant:

```text
source_url
source_trust
api_version
claim_state
validation
field_evidence
revalidation
signature_state
exact_signature_claim_allowed
```

## Claim resolution

The server should resolve exact claims per field:

```text
presence
module
kind
signature
parameters
return_type
effects
event_names
event_payloads
member_names
```

A missing field returns the equivalent of:

```text
TODO(API VERIFY)
```

It must not synthesize a missing signature.

## Safety

The MCP surface must not silently promote harvested API candidates.

UEFN compile/runtime truth remains outside this knowledge MCP and requires real editor evidence.
