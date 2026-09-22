# Codex Start Prompt — Real UEFN Project

Use this after running the bridge bootstrap.

```text
Read AGENTS.md.

Read:
- bridge/generated/PROJECT_CONTEXT.md
- bridge/generated/BRIDGE_STATUS.json
- the generated discovered project profile

Then discover the UEFN MCP toolsets available to you.

Inspect the actual Verse files in the project before suggesting edits.

Do not assume the static scan proves compilation.

For any requested feature:

1. identify the existing system owner;
2. identify the files to change;
3. identify exact Verse/UEFN APIs;
4. check known error memory;
5. make the smallest coherent change;
6. compile through UEFN;
7. preserve exact compiler errors;
8. fix only confirmed issues;
9. run a playtest when behavior needs verification;
10. update project/error memory only after evidence.
```
