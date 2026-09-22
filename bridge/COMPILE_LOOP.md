# Compile Loop

## Standard loop

```text
edit Verse
↓
UEFN compile
↓
success?
├─ yes → continue
└─ no
   ↓
capture exact error
   ↓
search error memory
   ↓
fix smallest cause
   ↓
compile again
```

## Commands

Search:

```bash
python tools/search_errors.py "exact compiler message"
```

Store:

```bash
python tools/add_error.py   --message "EXACT ERROR"   --category compiler   --file path/to/file.verse
```

After real successful compilation:

```bash
python tools/update_error.py ERR_ID   --status fixed   --compiled   --evidence "UEFN compile succeeded"
```
