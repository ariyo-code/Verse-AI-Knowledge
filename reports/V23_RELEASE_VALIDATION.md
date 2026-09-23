# V23 Release Validation

Release: **23.0.0 — API Coverage, Generation Reliability & Provenance**  
Date: **2026-09-23**  
Verse API snapshot: **42.20**

## Static validation performed

- V23 integrity: PASS
- legacy/local integrity guard: PASS
- verification evidence guard: PASS
- generated-file drift: PASS
- CLI contracts: PASS
- VerseLab state transitions: PASS
- V23 schema/integrity tests: PASS
- generated provenance tests: PASS
- V23 CLI tests: PASS
- repository validation: PASS
- RAG retrieval benchmark: **8/8 PASS**
- Evidence composition benchmark: **3/3 PASS**
- anti-hallucination policy eval: **11/11 PASS**
- static self-test: PASS
- preflight: PASS
- consolidated validation suite: PASS

## V23 API coverage seed

- structured symbols: **164**
- presence recorded: **164 / 164 (100%)**
- exact signatures verified: **11 / 164 (6.71%)**
- parameters structured from verified signatures: **11 / 164 (6.71%)**
- return types structured from verified signatures: **11 / 164 (6.71%)**
- effects structured from verified signatures: **11 / 164 (6.71%)**
- symbols with named events: **24 / 164 (14.63%)**
- verified event payload details: **0 / 164 (0%)**
- exact-evidence queue remaining: **153**

Three previously stored but insufficiently classified signature strings were reviewed against current official Epic pages during V23 preparation: `GetFortCharacter`, `GetPlayerUI`, and `GetPlayspace`.

## Generated-code provenance

V23 supports both:

- a visible Markdown status block before generated Verse;
- a hidden ordinary HTML comment after generated Verse.

The implementation explicitly forbids zero-width characters, bidi controls, Unicode tags, and other invisible Unicode mechanisms.

## UEFN boundary

```text
UEFN compile status for the repository release: NOT TESTED
Generation benchmark against a live model: NOT RUN
V22 vs V23 UEFN first-pass compile comparison: NOT YET MEASURED
```

No compile/runtime metric is fabricated by this release.
