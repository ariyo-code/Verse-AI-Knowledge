# Upload Verse AI Knowledge to GitHub — PC Guide

## Folder to upload

After extracting the archive, open:

```text
Verse-AI-Knowledge/
```

Inside it you should directly see:

```text
README.md
README_FR.md
README_EN.md
AGENTS.md
AI_GUIDE.md
portable/
knowledge/
docs/
projects/
rag/
tools/
lab/
.github/
...
```

**Upload the contents of this folder to the root of your GitHub repository.**

Do not end up with:

```text
Verse-AI-Knowledge/
└── Verse-AI-Knowledge/
    └── README.md
```

## Recommended method: GitHub Desktop

1. Install GitHub Desktop.
2. Sign in to GitHub.
3. Clone your `Verse-AI-Knowledge` repository.
4. Open the cloned local folder.
5. Copy **all contents** of the provided `Verse-AI-Knowledge/` folder into the cloned repository folder.
6. Review the changes in GitHub Desktop.
7. Recommended commit message:

```text
Initial release - Verse AI Knowledge v21
```

8. Click `Commit to main`.
9. Click `Push origin`.

## Suggested branches

Keep `main` stable.

Suggested long-lived branches:

```text
main
dev
ui-creator
rag
verselab
external-corpus
examples
experimental
```

For short-lived work:

```text
feature/phone-system
feature/ui-preview
fix/api-catalog
fix/ui-cleanup
```

## After upload

Check that GitHub renders `README.md` and that `portable`, `knowledge`, `docs`, `.github`, and `tools` are visible directly at repository root.

## Never publish secrets

Do not commit:

```text
.env
tokens
passwords
API keys
Epic credentials
private DATABASE_URL
Discord bot tokens
```

The project's `.gitignore` already excludes several common sensitive files.
