# This repository's notes for Claude

Hand-written for this repository; `global.md` beside it is generated from the owner's `claude-home` and must not be edited here ([ADR 0007](../../docs/decisions/0007-claude-setup-committed-for-cloud-sessions.md)).

## Which instruction wins

1. The owner's direct instructions in the conversation.
2. This repository's `CLAUDE.md` and this file.
3. `global.md` (the owner's personal rules).
4. The skills in `.claude/skills/`; they add method and never override the above.

## Where the work runs

- Claude works in Claude Desktop cloud sessions (Linux, bash, a fresh clone, the Default environment with no secrets) or on the owner's Mac. Give commands for the shell the session runs in.
- Cloud sessions run Node 22; `package.json` asks for `>=22.23.4`, and the dev container uses 26.
- A cloud session has no git pre-commit hook: before committing a change to any Markdown file, run `python3 scripts/docs_audit.py --root . --map`.
- This repository is public. Never commit personal details, contact data or anything from the owner's employer; `global.md` here leaves out the owner's "About me" section for that reason.
- No Graphify graph exists in a cloud session; read the code instead.
