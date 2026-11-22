---
status: accepted
date: 2026-11-22
decision-makers: Rio Gonzales (owner)
---

# Protect main with a ruleset: pull request and docs check required

## Context and Problem Statement

A push to `main` deploys the live site ([ADR 0002](0002-host-on-github-pages-via-actions.md)). Until 2026-11-22 nothing stopped a direct push, a force push or a deletion of `main` [V: `gh api .../branches/main` returned `protected: false`, 0 rulesets]. That was threat T1 in the [threat model](../security/threat-model.md).

## Considered Options

* A repository ruleset on the default branch
* Classic branch protection
* No protection (process only)

## Decision Outcome

Chosen option: "a repository ruleset", ruleset `Protect main` (id 27824802), active, with no bypass actors:

* require a pull request before merging, with **0** approvals (a sole owner cannot approve their own pull request);
* require the `docs` status check ([ADR 0004](0004-docs-check-in-ci.md));
* block force pushes and deletion.

### Consequences

* Good: every change to the live site goes through a pull request that passed the docs check.
* Bad: a typo fix also needs a branch and a pull request.
* Bad: with no bypass actors, if the `docs` check breaks, nothing can merge until it is fixed or the ruleset is edited in Settings → Rules.

### Confirmation

`gh api repos/dejaneiro555/dejaneiro555.github.io/rules/branches/main` lists `deletion`, `non_fast_forward`, `pull_request`, `required_status_checks` [V, 2026-11-22]. The pull request that adds this ADR is the first to merge under the ruleset.

## Pros and Cons of the Options

### Ruleset

* Good, because it is GitHub's newer mechanism and can be read and changed through the API.

### Classic branch protection

* Good, because it is widely documented.
* Bad, because it does the same job here with no extra benefit [Inference].

### No protection

* Bad, because it leaves T1 open.

## Threat-model impact

Reduces T1; recorded in the [threat model](../security/threat-model.md) in the same change.

## Sources

* `gh api` responses for the ruleset and branch rules [V, 2026-11-22]
* https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets [U: not opened in this session]
