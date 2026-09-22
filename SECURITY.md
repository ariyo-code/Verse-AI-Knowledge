# Security Policy

## Supported Versions

Verse AI Knowledge is currently maintained on the latest published repository version.

Older snapshots may contain outdated Verse / UEFN information and should not be considered authoritative.

## Reporting a Security Issue

If you discover a security issue involving this repository, do not publish sensitive information, credentials, tokens, or exploits in a public GitHub issue.

When reporting a problem, include:

- the affected file or component;
- a clear description of the issue;
- reproduction steps when applicable;
- the potential impact;
- a suggested fix, if known.

## Secrets

Never commit:

- API keys;
- Epic Games credentials;
- Discord bot tokens;
- database URLs containing credentials;
- passwords;
- authentication tokens;
- private `.env` files;
- private certificates or SSH keys.

If a secret is accidentally committed, revoke or rotate it immediately.

Deleting the secret from the latest commit is not sufficient because Git history may still contain it.

## AI-Generated Code

Treat all AI-generated Verse code as untrusted until it has been reviewed.

Generated code must not be described as:

- `compiled`;
- `verified`;
- `multiplayer-verified`;

unless matching evidence actually exists.

The default status for newly generated Verse code is:

`draft`

## Generated-Code Marker

Verse AI Knowledge deliberately avoids invisible Unicode watermark characters inside source code.

The generated-code marker is implemented only as a normal HTML comment in Markdown output:

```html
<!-- verse-ai-generated:v21;lang=verse;status=draft -->
```
