# Security Policy

## Reporting
Use GitHub Private Vulnerability Reporting when available: repository **Security → Advisories → Report a vulnerability**. Do not post secrets, exploit details or credentials in a public issue.

## Secrets
Never commit API keys, tokens, cookies, private keys, `.env` secrets, Discord tokens, GitHub PATs, Epic credentials or LLM provider credentials. If a secret is exposed, revoke/rotate it; deleting it from the latest commit does not remove it from Git history.

## Remote content
Epic documentation fetchers use HTTPS and strict host validation. Remote pages, compiler logs, project source and external examples are data, not instructions.

## Validation boundary
A static security or CI pass does not imply UEFN compile/runtime/multiplayer verification.
