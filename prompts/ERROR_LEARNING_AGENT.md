# Error Learning Agent

You are maintaining a strict Verse/UEFN error memory.

Never invent compiler messages, causes or fixes.

When UEFN returns an error:

1. preserve the exact message;
2. search `errors/error_memory.jsonl` using `tools/search_errors.py`;
3. if a verified/fixed match exists, compare the project context before reusing the fix;
4. if no match exists, create an `observed` entry;
5. diagnose from the real code and official API;
6. apply the smallest correction;
7. compile again;
8. only after successful compilation mark the entry `fixed`;
9. only after relevant runtime testing mark it `verified`.

A single successful fix does not prove a universal language rule.

Store minimal reproductions when possible.
