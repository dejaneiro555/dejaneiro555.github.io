# Security Policy

## Reporting a vulnerability

**Do not open a public issue or pull request for a security problem.**

Report it privately through GitHub: open the repository's **Security** tab and choose **Report a vulnerability**, or go straight to <https://github.com/dejaneiro555/dejaneiro555.github.io/security/advisories/new>. The report is not public [U: GitHub's docs on who can see it were not opened].

Private vulnerability reporting was turned on 2026-11-23 [V: `gh api repos/dejaneiro555/dejaneiro555.github.io/private-vulnerability-reporting` returned `{"enabled":true}`]. A test report has not been sent, so delivery is not confirmed end to end [U] (VB-05).

No response-time targets are promised yet.

## What not to include in a report

Do not send real personal data, credentials, keys, or tokens. If you found a live secret or real personal data in this repository, report where it is without copying the value.

## Supported versions

There are no releases. The only supported version is the live site, built from `main` (see [ADR 0002](docs/decisions/0002-host-on-github-pages-via-actions.md)).
