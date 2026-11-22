---
status: accepted
date: 2026-11-21
decision-makers: Rio Gonzales (owner)
---

# Check in CI that code changes come with their docs

## Context and Problem Statement

The repository had no documentation system. The owner's documentation standard requires a changelog entry with code changes and an ADR for each new dependency or hosting/CI choice; a check that runs only on request lets docs drift.

## Considered Options

* A GitHub Actions workflow running `scripts/docs_audit.py --changed` on every pull request
* A local pre-commit hook only
* No automated check

## Decision Outcome

Chosen option: "a CI workflow", because CI runs for every pull request on any machine, including Codespaces, while a local hook exists only in one clone. The setup also installs a local pre-commit hook that keeps `docs/MAP.md` current.

### Consequences

* Good: a pull request that changes code without a changelog entry fails.
* Bad: a genuinely docs-free change needs a `Docs: none needed - <reason>` line in a commit message.
* Bad: `scripts/docs_audit.py` is a copy of the docs-system skill's script and must be re-copied when the skill changes (the audit warns when it falls behind).

### Confirmation

The `Docs check` workflow runs on the pull request that adds it.

## Pros and Cons of the Options

### CI workflow

* Good, because it cannot be skipped by forgetting.
* Bad, because it adds a third-party action (`actions/checkout@v4`) with `contents: read` only.

## Threat-model impact

Adds one workflow with read-only permissions; covered by T2 in the [threat model](../security/threat-model.md).

## Sources

* `.github/workflows/docs-check.yml`, `scripts/docs_audit.py` [V]
