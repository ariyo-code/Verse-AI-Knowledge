# Project Context Agent

You are working inside an existing UEFN project.

Before implementing a substantial feature:

1. read `AGENTS.md`;
2. read `knowledge/ROUTING.md`;
3. search the project memory:
   `python tools/search_projects.py "relevant system"`;
4. inspect the current project's `project.json` if available;
5. inspect system manifests;
6. inspect the actual Verse project through UEFN MCP or filesystem;
7. compare planned architecture with real implementation;
8. never assume planned systems already exist.

## Status semantics

- `planned` = intended architecture only;
- `discovered` = found by static scan;
- `compiled` = actually compiled;
- `verified` = compiled and behavior tested.

Do not promote statuses without evidence.

## Reuse rule

Before writing a new system, search for:

- existing responsibility;
- public interface;
- state already owned elsewhere;
- reusable UI;
- existing persistence model;
- known edge cases.

Avoid creating two services that own the same state.

## Output expectations

When proposing a change, report:

- project/system affected;
- files expected to change;
- dependencies;
- state impact;
- persistence impact;
- lifecycle impact;
- verification required.
