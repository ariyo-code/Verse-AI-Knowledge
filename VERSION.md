# Knowledge Base Version

Release: **24.0.0**  
Schema: **24**  
Codename: **Claim Resolution, Evidence Graph & Continuous Verification**  
Verse API snapshot: **42.20**

## V24 focus

V24 builds on V23 without redesigning the repository.

Its main goals are:

- resolve API claims at field level instead of treating a whole symbol as equally verified;
- link signatures, parameters, return types, effects, events and members to explicit evidence IDs;
- generate an API evidence graph and deterministic claim decisions;
- lint generated Verse for unsupported API-looking claims before UEFN compilation;
- make Epic documentation fetching redirect-safe and hostname-strict;
- add version-aware revalidation and API coverage snapshots/diffs;
- provide a provider-optional end-to-end LLM evaluation harness;
- keep visible + hidden Markdown provenance for generated Verse;
- preserve strict UEFN compile/runtime/multiplayer evidence boundaries.

## Validation boundary

Repository CI, static analysis and policy evaluation do **not** prove that arbitrary generated Verse compiles in UEFN.

```text
UEFN compile status: NOT TESTED by release metadata
LLM end-to-end benchmark: SKIPPED unless a provider or saved outputs are explicitly configured
```
