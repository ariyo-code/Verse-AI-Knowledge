# How it works

```text
Task → Routing → Retrieval → API claim resolution → Evidence Pack
→ Claim Ledger → Implementation → Provenance → Static validation
→ UEFN compile/runtime/multiplayer evidence when available
```

Retrieval score is never treated as proof. Exact API claims are allowed only when the corresponding field-level evidence is present. Otherwise the system returns `TODO(API VERIFY)`.
