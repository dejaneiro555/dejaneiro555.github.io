---
status: accepted
date: 2026-11-21
decision-makers: Rio Gonzales (owner)
---

# Host on GitHub Pages, deployed by GitHub Actions on every push to main

## Context and Problem Statement

*Recorded after the fact on 2026-11-21: the decision was made on 2026-11-15, as the code and commits show. The reasons below are what the commits state; anything else is marked.*

The built site needs free hosting at a stable address that updates when the content changes.

## Considered Options

* GitHub Pages, built by GitHub Actions
* Other hosts (Netlify, Vercel, Cloudflare Pages): I cannot confirm whether any were considered

## Decision Outcome

Chosen option: "GitHub Pages via GitHub Actions", added in `1e49c04` (2026-11-15). The workflow follows Astro's GitHub Pages guide, as its first line says.

### Consequences

* Good: no cost, and the address is the GitHub user site `dejaneiro555.github.io`.
* Good: every push to `main` deploys, so `main` is always what is live.
* Bad: anyone who can push to `main` changes the live site (threat T1).

### Confirmation

The live site at https://dejaneiro555.github.io matches `main` after each deploy run in the Actions tab.

## Pros and Cons of the Options

### GitHub Pages via Actions

* Good, because the code and the hosting live in one place.
* Bad, because it relies on third-party actions pinned to major-version tags (threat T2).

## Threat-model impact

Adds the GitHub Actions and Pages trust boundaries (T1, T2 in the [threat model](../security/threat-model.md)).

## Sources

* `.github/workflows/deploy.yml`, commit `1e49c04` [V]
* https://docs.astro.build/en/guides/deploy/github/ [U: cited in the workflow, not opened in this session]
