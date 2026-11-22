---
status: accepted
date: 2026-11-21
decision-makers: Rio Gonzales (owner)
---

# Build the personal site as a static site with Astro

## Context and Problem Statement

*Recorded after the fact on 2026-11-21: the decision was made on 2026-11-15, as the code and commits show. The reasons below are what the commits state; anything else is marked.*

The owner needs a personal portfolio site with a few pages and a set of project case studies, hosted for free and simple to change.

## Considered Options

* Astro (static output)
* Other static site generators or hand-written HTML: I cannot confirm whether any were considered

## Decision Outcome

Chosen option: "Astro", set up in `febaf3d` (2026-11-15). Why Astro over the alternatives is not recorded in the repository: I cannot confirm this.

### Consequences

* Good: pages are prebuilt HTML with no client-side JavaScript in `src/` today, which keeps the attack surface small [V].
* Good: project case studies are Markdown files checked against a schema (`src/content.config.ts`).
* Bad: a Node toolchain is needed to build (`engines.node >=22.23.4` in `package.json`).

### Confirmation

`npm run build` succeeds (9 pages on 2026-11-21 [V]).

## Pros and Cons of the Options

### Astro

* Good, because it outputs static files, which GitHub Pages can serve.
* Bad, because it adds a build step and npm dependencies.

## Threat-model impact

Defines the build pipeline in the [threat model](../security/threat-model.md) (T2, T3). No change made by this record.

## Sources

* `package.json`, `astro.config.mjs`, `src/content.config.ts`, commit `febaf3d` [V]
* https://docs.astro.build/ [U: not opened in this session]
