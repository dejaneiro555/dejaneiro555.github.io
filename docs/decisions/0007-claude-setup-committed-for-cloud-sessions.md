---
status: accepted
date: 2026-11-23
decision-makers: Rio Gonzales (owner)
---

# Commit the owner's Claude setup so cloud sessions load it

## Context and Problem Statement

The owner works with Claude in Claude Desktop cloud sessions, which run on a fresh clone of the repository. A cloud session loads only what the repository commits: not the owner's `~/.claude/CLAUDE.md`, user skills or user hooks [V: https://code.claude.com/docs/en/cloud-environments.md, read 2026-11-23 through a documentation agent]. Two tests on 2026-11-23 showed that a cloud environment's setup script cannot fetch the owner's private `claude-home` repository (`fatal: could not read Username for 'https://github.com'`), and a session with two repositories would not load a repository's hooks [V2, same doc] [V: the test sessions' reports].

## Considered Options

* Commit generated copies of the owner's setup into each repository.
* Start every cloud session with the project and `claude-home` both selected.
* Leave cloud sessions without the owner's rules and skills.

## Decision Outcome

Chosen option: "commit generated copies", because it is the only option that loads the same rules, skills and Stop hook in every session without weakening repository hooks.

* `.claude/rules/global.md`: the owner's `CLAUDE.md` from the private `dejaneiro555/claude-home` repository, word for word, except the "About me" section, which stays out of this public repository.
* `.claude/skills/`: `docs-system`, `fable-playbook`, `graphify` (Apache-2.0, license files included) and `task-observer` (CC-BY-4.0, license included), byte-identical to `claude-home`.
* `.claude/settings.json`: the docs-system Stop hook, so the docs check runs at the end of every turn in the cloud as on the Mac.
* `.claude/rules/repo.md`: hand-written notes for this repository, including which instruction wins.
* `claude-home/sync_to_repos.py` regenerates the copies; changes go through a pull request.

### Consequences

* Good: a cloud session and a session on the Mac load the same text and the same skills.
* Bad: task-observer observations and Claude's auto-memory written in a cloud session are lost when it ends.
* Bad: on the Mac the global rules load twice (from `~/.claude/CLAUDE.md` and `global.md`), costing context but not changing behaviour.
* Neutral: copies can fall behind `claude-home` until the sync script is run again.

### Confirmation

A cloud session on this repository lists `CLAUDE.md`, `.claude/rules/global.md`, `.claude/rules/repo.md` and the four skills, and its Stop hook runs.

Tested 2026-11-23 in a read-only cloud session at `e7abeac` (the session's report, pasted by the owner) [V]: `CLAUDE.md`, `.claude/rules/global.md` and `.claude/rules/repo.md` loaded, with no "About me" section; all four skills listed; the Stop hook is configured and exited 0; docs audit 0 errors; Node v22.23.5; `npm run build` built 9 pages. The file's "Generated from" comment did not reach the session, most likely because HTML comments are dropped when rules load [Inference]. Accepted by the owner on 2026-11-23.
