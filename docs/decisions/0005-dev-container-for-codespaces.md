---
status: proposed
date: 2026-11-21
decision-makers: Rio Gonzales (owner)
---

# Develop the site in a dev container, Codespaces first

## Context and Problem Statement

The owner plans to do most development in a cloud environment connected to GitHub, so that the laptop holds nothing that exists only there. Today the site can only be developed on a machine that already has a suitable Node installed (`engines.node >=22.23.4` in `package.json`; the owner's Mac runs Node 26.13.1 [V]). Nothing in the repository describes that environment, so a fresh machine or a GitHub Codespace has to guess it.

## Decision Drivers

* The environment is written down as code and reviewed like code.
* It works the same in GitHub Codespaces and on a local machine.
* It stays inside the free Codespaces allowance.
* The owner's Mac is still needed for hardware and coursework that a cloud container cannot reach (for example a board on USB) [Inference].

## Considered Options

* A dev container (`.devcontainer/devcontainer.json`) using Microsoft's Node image
* No configuration: let Codespaces use its default image
* Local development only, documented in `CLAUDE.md`

## Decision Outcome

Chosen option: "a dev container using Microsoft's Node image", because it is the only option that records the environment in the repository and works both in Codespaces and locally.

* Image: `mcr.microsoft.com/devcontainers/javascript-node`, tag `26`, matching the owner's Mac. Tags `22`, `24` and `26` exist [V: the registry's tag list, read 2026-11-21].
* Forward port 4321, the Astro dev server's port.
* Install dependencies once, after the container is created, with `npm ci`.
* Codespaces first; local use with Docker is possible but not planned.

### Consequences

* Good: any Codespace or local container gets the same Node and the same dependencies.
* Good: the laptop holds no environment that exists only there.
* Bad: Codespaces use counts against the free allowance: 120 compute hours and 15 GB-month of storage a month on GitHub Free [V]. A 2-core machine uses 2 of those hours per hour [V], so about 60 hours of real use a month (120 ÷ 2) [Inference from that table].
* Bad: storage is counted while a codespace exists, not only while it runs [V], so unused codespaces should be deleted.
* Neutral: a codespace stops after 30 minutes idle by default (configurable from 5 to 240) [V].
* Neutral: the git hook that keeps `docs/MAP.md` current lives in `.git/hooks/`, so it is missing in a fresh codespace; the docs check in CI still catches a stale map ([ADR 0004](0004-docs-check-in-ci.md)).

### Confirmation

Accept this ADR once a codespace built from `.devcontainer/devcontainer.json` runs `npm run dev` and the site opens on forwarded port 4321. Until then it stays `proposed`. Open: whether Astro's dev server is reachable through port forwarding without `--host` (VB-03).

## Pros and Cons of the Options

### Dev container with Microsoft's Node image

* Good, because the Node version and setup steps are pinned in the repository.
* Good, because the same file works in Codespaces and in VS Code locally.
* Bad, because the image tag `26` follows Node 26 updates, so the exact Node version can change between rebuilds [Inference].

### Codespaces default image

* Good, because nothing needs writing.
* Bad, because the Node version is whatever the default image ships; I cannot confirm that it meets `>=22.23.4`.
* Bad, because nothing in the repository records the environment.

### Local development only

* Good, because there is no allowance to watch.
* Bad, because it keeps development tied to one laptop, which is the problem this ADR solves.

## Threat-model impact

Adds two trust boundaries: GitHub Codespaces runs the code, and Microsoft's container registry supplies the base image. The site needs no secrets, so no secrets go into Codespaces. Update `docs/security/threat-model.md` in the change that adds `.devcontainer/`.

## Sources

* https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-codespaces/about-billing-for-github-codespaces (allowance, multiplier, storage) [V, read 2026-11-21]
* https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers (`.devcontainer/devcontainer.json` location; default image when there is none) [V, read 2026-11-21]
* https://docs.github.com/en/codespaces/customizing-your-codespace/setting-your-timeout-period-for-github-codespaces (30-minute default timeout) [V, read 2026-11-21]
* https://containers.dev/implementors/json_reference/ (`image`, `forwardPorts`, `postCreateCommand`) [V, read 2026-11-21]
* https://mcr.microsoft.com/v2/devcontainers/javascript-node/tags/list (tags `22`, `24`, `26`) [V, read 2026-11-21]
