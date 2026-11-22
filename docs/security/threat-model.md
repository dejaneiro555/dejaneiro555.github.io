# Threat model

**Draft, not reviewed by anyone else.** Written 2026-11-21 during the docs-system setup, for `main` at `8f7c15b`.

## Q1. What are we working on?

A static website (see [architecture](../architecture/README.md)). Data: only what the site deliberately publishes (name, career history, project write-ups, LinkedIn and GitHub links). No user input, accounts, cookies, forms or server code. Data flow: owner → GitHub repository → GitHub Actions build (npm packages, third-party actions) → GitHub Pages → public visitors.

## Q2. What can go wrong?

| ID | Component | Threat (STRIDE) | Mitigation | Status |
|---|---|---|---|---|
| T1 | GitHub account | Spoofing / Tampering: someone with the owner's GitHub access pushes to `main` and defaces or replaces the site | Two-factor authentication on the GitHub account [U]; pull requests before `main` (process, not enforced) | partly |
| T2 | Build pipeline | Tampering: a compromised third-party action (`withastro/action@v6`, `actions/checkout@v7`, `actions/deploy-pages@v5`, `actions/checkout@v4`) runs in the build. They are pinned to major-version tags, not commit SHAs | Workflows request minimal permissions (`contents: read`; `pages: write` and `id-token: write` only in deploy) [V] | accepted risk |
| T3 | Dependencies | Tampering: a malicious npm package version is installed during the build | `package-lock.json` is committed [V]; two direct dependencies only (`astro`, `@fontsource-variable/jost`) | partly |
| T4 | Content | Information disclosure: private details (contact data, employer-internal material) are published by mistake | Owner review before merge; no email address on the site [V: `contact.astro` links LinkedIn and GitHub only] | partly |
| T5 | Repository | Information disclosure: a secret is committed. The site needs none today | `.gitignore` excludes `.env` and `.env.production` [V] | ok |

## Q3. What are we going to do about it?

Open questions for the owner, not decisions: enable branch protection on `main`; consider pinning actions to commit SHAs; enable private vulnerability reporting (see `SECURITY.md`).

## Q4. Did we do a good enough job?

Not reviewed. Not covered: GitHub Pages' own security, the browser side of the published HTML, the owner's local machine.

## Sources

* `.github/workflows/deploy.yml`, `.github/workflows/docs-check.yml`, `package.json`, `.gitignore`, `src/pages/contact.astro` [V, opened 2026-11-21]
