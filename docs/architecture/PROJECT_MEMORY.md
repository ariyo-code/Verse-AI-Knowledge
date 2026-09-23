# Project Memory Architecture

## Why

General Verse knowledge is not enough.

An expert coding agent also needs to know:

- what this project already contains;
- who owns which state;
- how systems communicate;
- what is persistent;
- what is only runtime;
- what has already been tested;
- what architectural decisions were made.

## Layers

```text
API Knowledge
↓
Patterns
↓
Project
↓
Systems
↓
Files / Devices / State
↓
Real UEFN project
```

## Planned vs discovered

A planned manifest describes intent.

A discovered profile comes from scanning actual files.

They are deliberately separate because architecture documents can become stale.

## Conflict rule

If planned memory disagrees with actual project files:

```text
actual project > planned memory
```

If actual project compiles differently from API assumptions:

```text
UEFN compiler/runtime > everything else
```
