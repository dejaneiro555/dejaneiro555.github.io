# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/). Written by hand for people: do not paste commit logs here.

## [Unreleased]

### Added

- The owner's Claude setup is committed in `.claude/` (ADR 0007, accepted 2026-11-23 after a cloud-session test); `.gitignore` now covers `__pycache__/` and `.claude/settings.local.json`: global rules (without personal details), the docs-system, fable-playbook, graphify and task-observer skills, and the docs-system Stop hook, so Claude Desktop cloud sessions load the same setup as the Mac.
- Private vulnerability reporting is on; `SECURITY.md` says how to use it.
- `main` is protected by a ruleset (ADR 0006): changes need a pull request that passes the docs check; force pushes and deletion are blocked.
- A dev container for GitHub Codespaces (`.devcontainer/devcontainer.json`, ADR 0005): Node 26, port 4321 forwarded, dependencies installed with `npm ci`. Tested in a codespace on 2026-11-22.
- Documentation system: `docs/` with architecture, threat model (draft), progress, governance, a knowledge map and four ADRs; `SECURITY.md`; a project `CLAUDE.md`.
- A docs check on every pull request (ADR 0004): code changes need a changelog entry, dependency changes an ADR.
