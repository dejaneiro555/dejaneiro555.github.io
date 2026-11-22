# Learning Note 0001: setting up the documentation system

## What we did

Ran `/docs-system setup` on 2026-11-21. It created the `docs/` folders, `CHANGELOG.md`, `SECURITY.md`, a knowledge map (`docs/MAP.md`), a CI check and a local pre-commit hook. Then filled the placeholders from the code and git history: architecture, threat model, progress, governance process, and four ADRs (three recorded after the fact).

## How it works

- An **ADR** (Architecture Decision Record) is a short file recording one decision, the options and why. A *retroactive* ADR records a decision already made; it says so, and marks reasons the repository does not show as "I cannot confirm this".
- The **docs check** (`scripts/docs_audit.py --changed origin/main`) compares a branch with `main`: changed code needs a `CHANGELOG.md` entry, a changed `package.json` needs an ADR.
- The **pre-commit hook** regenerates `docs/MAP.md` on each commit that touches Markdown. It lives in `.git/hooks/`, which is not part of the repository, so a fresh clone (or a Codespace) does not have it; CI still catches a stale map.

## What went wrong, and why it matters

Nothing failed. One choice to note: the reasons for choosing Astro and GitHub Pages were never written down at the time, so the ADRs cannot give them. Writing the ADR when deciding is cheaper than reconstructing it.

## What is still open

- A private vulnerability-reporting channel (`SECURITY.md`).
- The priority order and invariants in governance.
- VB-01 and VB-02 in the [verification backlog](../verification-backlog.md).

## Exercise

Change one line in `src/pages/about.astro` on a branch without touching `CHANGELOG.md`, then run `python3 scripts/docs_audit.py --root . --changed origin/main`. Predict the result before you run it.

## Sources

* `scripts/docs_audit.py` docstring and the docs-system skill [V]
* https://adr.github.io/madr/ [U: not opened in this session]
