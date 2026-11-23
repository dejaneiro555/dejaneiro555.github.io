# Threat model

**Draft, not reviewed by anyone else.** Written 2026-11-21 during the docs-system setup, for `main` at `8f7c15b`.

## Q1. What are we working on?

A static website (see [architecture](../architecture/README.md)). Data: only what the site deliberately publishes (name, career history, project write-ups, LinkedIn and GitHub links). No user input, accounts, cookies, forms or server code. Data flow: owner → GitHub repository → GitHub Actions build (npm packages, third-party actions) → GitHub Pages → public visitors. Development (added 2026-11-21, [ADR 0005](../decisions/0005-dev-container-for-codespaces.md)): GitHub Codespaces builds a container from Microsoft's image `mcr.microsoft.com/devcontainers/javascript-node:26`, runs `npm ci`, and holds a clone of the repository with the owner's GitHub access.

## Q2. What can go wrong?

| ID | Component | Threat (STRIDE) | Mitigation | Status |
|---|---|---|---|---|
| T1 | GitHub account | Spoofing / Tampering: someone with the owner's GitHub access pushes to `main` and defaces or replaces the site | Two-factor authentication (authenticator app and a security key, recovery codes saved) on the GitHub account [V, owner-reported 2026-11-22, VB-01]; ruleset "Protect main" requires a pull request and the `docs` check, and blocks force pushes and deletion ([ADR 0006](../decisions/0006-protect-main-with-a-ruleset.md)) | ok |
| T2 | Build pipeline | Tampering: a compromised third-party action (`withastro/action@v6`, `actions/checkout@v7`, `actions/deploy-pages@v5`, `actions/checkout@v4`) runs in the build. They are pinned to major-version tags, not commit SHAs | Workflows request minimal permissions (`contents: read`; `pages: write` and `id-token: write` only in deploy) [V] | accepted risk |
| T3 | Dependencies | Tampering: a malicious npm package version is installed during the build | `package-lock.json` is committed [V]; two direct dependencies only (`astro`, `@fontsource-variable/jost`) | partly |
| T4 | Content | Information disclosure: private details (contact data, employer-internal material) are published by mistake | Owner review before merge; no email address on the site [V: `contact.astro` links LinkedIn and GitHub only] | partly |
| T5 | Repository | Information disclosure: a secret is committed. The site needs none today | `.gitignore` excludes `.env` and `.env.production` [V] | ok |
| T6 | Dev container | Tampering: a compromised base image or tag update runs code in the codespace, which can push to the repository with the owner's access | Image from Microsoft's registry, pinned to major tag `26` (not `latest`) [V: `.devcontainer/devcontainer.json`]; no secrets stored in Codespaces for this repository | accepted risk |
| T7 | Codespaces | Information disclosure: a forwarded port is made public, exposing the dev server | Port 4321 showed as Private in the codespace tested on 2026-11-22 [V, VB-04]; the dev server serves only the public site's content | ok |
| T8 | Claude cloud sessions | Tampering / Information disclosure: Claude runs in Anthropic's cloud on a clone of this public repository, with GitHub access through Anthropic's proxy; committed rules and skills steer what it does | No secrets in this repository's cloud environment; the committed Claude setup is reviewed in pull requests like code ([ADR 0007](../decisions/0007-claude-setup-committed-for-cloud-sessions.md)); personal details left out of the public copy | partly |

## Q3. What are we going to do about it?

Done: two-factor on GitHub and Vercel, and the `main` ruleset (2026-11-22). Open questions for the owner, not decisions: consider pinning actions to commit SHAs. Private vulnerability reporting is on (2026-11-23, `SECURITY.md`).

## Q4. Did we do a good enough job?

Not reviewed. Not covered: GitHub Pages' own security, the browser side of the published HTML, the owner's local machine.

## Sources

* `.github/workflows/deploy.yml`, `.github/workflows/docs-check.yml`, `package.json`, `.gitignore`, `src/pages/contact.astro` [V, opened 2026-11-21]
