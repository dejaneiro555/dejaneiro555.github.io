# Governance

The rules of the project: what wins when goals conflict, how work is done, who decides. The owner, Rio Gonzales, decides; this is a one-person project.

## Priority order

Not decided yet. Question for the owner (see the docs audit of 2026-11-21).

## Evidence standard

Claims carry a source or a label: **[V]** checked against a primary source, **[V2]** secondary source only, **[U]** not verified, **[Inference]** reasoned judgment. If something cannot be verified, write "I cannot confirm this" and add it to [the verification backlog](../verification-backlog.md).

## Invariants

Not decided yet. Question for the owner. A likely candidate, not adopted: nothing private (contact details beyond LinkedIn and GitHub, employer-internal material) is published on the site [Inference].

## Process

- Work happens on a branch and reaches `main` through a pull request; a push to `main` deploys the site ([ADR 0002](../decisions/0002-host-on-github-pages-via-actions.md)). The "Protect main" ruleset enforces this ([ADR 0006](../decisions/0006-protect-main-with-a-ruleset.md)).
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`) [V: `git log`, 2026-11-21].
- Every change with code includes a `CHANGELOG.md` entry, and every new dependency or hosting/CI choice an ADR; the docs check in CI enforces both ([ADR 0004](../decisions/0004-docs-check-in-ci.md)).
- A finished step gets a Learning Note in [learning/](../learning/README.md) and a row in [progress/](../progress/README.md).
