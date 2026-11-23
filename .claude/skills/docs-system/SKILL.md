---
name: docs-system
description: "Set up, audit and keep current a repository's documentation system: the standard docs/ layout (architecture, ADRs, explanation, governance, how-to, learning notes, progress, reference, security/threat model, tutorials, glossary, verification backlog), CHANGELOG and SECURITY.md, a generated knowledge map (docs/MAP.md: every doc, its title, ADR status and backlinks), a short landing-page README, and automation that keeps them current (a CI check that fails pull requests whose code changes skip the changelog or an ADR, a git pre-commit hook and a Claude Code Stop hook that regenerate the map). Use when the user asks to set up, scaffold, organise, audit, review or check a project's docs, docs/ folder, README or knowledge map, asks \"are my docs complete / up to date\" or how to keep them up to date, starts a new repository, or finishes a milestone and wants the docs checked. Run as /docs-system audit (default, changes nothing) or /docs-system setup."
argument-hint: "[audit|setup]"
---

# Docs system: set up and audit

Mode: `$ARGUMENTS` (empty means `audit`).

- **audit** changes nothing and ends with a report.
- **setup** creates what is missing, fills it from what the repository already shows, then audits.

The goal is a repository where a newcomer, a reviewer and a future AI session can each find *how it is built, why, what the rules are, where it stands, and what is not yet verified* without asking anyone.

## The standard layout

```
README.md  CHANGELOG.md  SECURITY.md  CLAUDE.md
docs/
  README.md                 index: one line per folder
  MAP.md                    knowledge map: every Markdown file, title, ADR status, backlinks (generated)
  architecture/             how it is built: context, components, data model, trust boundaries
  decisions/                ADRs, one per significant decision; README.md is the index
  explanation/              background and concepts: the "why"           (Diátaxis)
  how-to/                   steps for one specific task                  (Diátaxis)
  reference/                API, schema, config, commands: facts only    (Diátaxis)
  tutorials/                guided lessons for a newcomer                (Diátaxis)
  governance/               priorities, invariants, process, who decides
  learning/                 one Learning Note per finished step
  progress/                 plan, current phase, status with evidence
  security/                 threat-model.md, reviews; data-classification.md if personal data
  verification-backlog.md   claims not yet verified
  glossary.md
```

Every folder exists and has a README saying what belongs there and what is in it today. An honest "nothing yet" README is correct; a missing folder is not, because nobody can tell whether it was forgotten or never needed.

**The repository's own rules win.** Read its `CLAUDE.md` and governance file first. If it already keeps a section somewhere else (a root `GOVERNANCE.md`, `docs/plan/`, its own ADR numbering), keep that and do not duplicate it. If it deliberately left a section out and recorded why, report that as a recorded deviation, not a gap.

## Step 1: run the structure check

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/docs_audit.py" --root .
```

(`${CLAUDE_SKILL_DIR}` is the folder this file is in.) It reports missing sections and root files, a missing index, broken relative links, orphan files, ADRs with no status or not in the index, a changelog with no Unreleased section, unfilled `TODO(docs)` placeholders, a missing or stale `docs/MAP.md`, and a repository copy `scripts/docs_audit.py` that differs from this skill's (copy it again). `ERROR` means a required piece is missing or a link is broken; exit code 1.

For **setup**, add `--init`. It copies each missing file from `templates/` and never overwrites or edits an existing file. It also installs the CI check: `scripts/docs_audit.py` (a copy of this script) and `.github/workflows/docs-check.yml`, the workflow skipped when an existing workflow already runs `docs_audit.py`. Last, it generates `docs/MAP.md`. It does not create the root `README.md` or `CLAUDE.md`: those are project-specific, so write them yourself.

**Knowledge map.** `--map` regenerates `docs/MAP.md`: every Markdown file in the root and `docs/`, its first `#` title, the status of each ADR (`docs/decisions/` or `docs/adr/`), and a "Linked from" list of the files that link to it. Titles are escaped, and links inside code are ignored. Nobody runs `--map` by hand: `--init` (or `--install-hook` in an existing repository) installs a git pre-commit hook that regenerates the map and adds it to every commit that changes a Markdown file, and the Stop hook regenerates a stale map at the end of each Claude turn. The audit still reports `ERROR` while the map is missing or stale, so CI catches a clone without the hook (`.git/hooks` is not part of the repository). An existing pre-commit hook that is not ours is never overwritten; the install reports it instead. A `docs/MAP.md` without the generated marker belongs to the repository's own generator (for example `tools/build_map.py`): it is reported as INFO, never checked or overwritten, and `--map` refuses to replace it.

Add `--changed <base>` (for example `--changed origin/main`, or `--changed HEAD` for uncommitted work) to also check that docs moved with the code changed since the merge-base with `<base>`, including untracked files:

| Changed | Required | Level |
|---|---|---|
| any code file (not `docs/`, root `*.md`, or dot-paths) | `CHANGELOG.md` | ERROR |
| a dependency manifest (`pyproject.toml`, `requirements.txt`, `package.json`, …) | a non-README file in `docs/decisions/` or `docs/adr/` | ERROR |
| a new code file | something in `docs/architecture/` | WARN |
| a path matching auth/login/secur/crypt/secret/token/session/permission/migration/storage | `docs/security/threat-model.md` | WARN |

A line `Docs: none needed - <reason>` in any commit message in the range turns these ERRORs into INFO. A `<base>` that is not a commit exits 2, never a pass.

## Keeping docs current automatically

An audit that runs only on request lets docs drift. Wire `--changed` into the change itself. **setup** installs the CI check; the other two are opt-in: set them up only when the user asks.

- **Claude Code Stop hook** (all repos; regenerates a stale `docs/MAP.md`; silent in any repo without `docs/README.md` or `docs/MAP.md`). Add to `~/.claude/settings.json`:
  ```json
  {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "~/.claude/skills/docs-system/scripts/stop_hook.sh"}]}]}}
  ```
  When the turn leaves uncommitted code changes without the docs they need, it blocks the stop once and shows Claude the findings. It never blocks twice in a row (`stop_hook_active`), and only change-related findings block it, never old structure errors.
- **Local git hook** (per repo): `.git/hooks/pre-commit` containing `exec python3 ~/.claude/skills/docs-system/scripts/docs_audit.py --root . --changed HEAD`, then `chmod +x` it. It sees unstaged changes too, and cannot read the commit message, so skip a genuinely docs-free commit with `git commit --no-verify` and put the `Docs: none needed` line in the message for CI.
- **CI** (per repo, the check that cannot be forgotten; installed by `--init`): `templates/.github/workflows/docs-check.yml` runs the repository's copy `scripts/docs_audit.py --root . --changed origin/<base>` on every pull request, with full history. CI cannot see `~/.claude`, so the repository carries the copy, and the audit warns when it falls behind. The check also fails on structure errors, so commit the workflow only once the script reports no `ERROR`, or every pull request fails. A repository whose main CI file already runs it (a step calling `docs_audit.py`) gets no second workflow.

## Step 2: read, because the script only checks structure

A scaffold that passes the script can still be wrong. Check each of these by opening the files and the code, and record what you actually looked at:

1. **Architecture matches the code.** Components, data stores and entry points named in `architecture/` exist in the source tree, and the main ones in the source tree are named in `architecture/`. Planned parts are marked planned.
2. **Decisions are recorded.** Each dependency in the manifest, and each storage, auth, hosting or CI choice visible in the code, traces to an ADR. List the ones that do not. Superseded ADRs say what superseded them.
3. **The repository's own promises are kept.** If its governance or README lists a document, a check or a process, that thing exists. (Example found when this skill was written: a guide listing `security/data-classification.md` and `glossary.md` that had not been created.)
4. **The README is a landing page.** The root `README.md` says what the project is, how to start in a few steps, where it stands in one line, and links into `docs/` (index and map). The script warns past 150 lines. Steps for a task belong in `how-to/`, background in `explanation/`, facts (layout, commands, config) in `reference/`, status tables in the progress folder.
5. **Diátaxis kinds are not mixed.** A tutorial teaches a newcomer end to end; a how-to solves one task; reference states facts; explanation gives background. Flag files in the wrong folder (an install guide outside `how-to/` or `tutorials/`, for example).
6. **Commands work.** Every command in the README, how-to guides and tutorials either ran successfully in this session, or is listed as "not run" with the reason. Never report a command as working without running it.
7. **Progress is current.** The stated phase and status agree with the changelog and recent commits (`git log -15 --stat`). Status rows have evidence links.
8. **Security docs are current.** The threat model covers the data flows, storage and trust boundaries the code has today, and says who reviewed it. `SECURITY.md` names a reporting channel that is confirmed to work.
9. **Staleness.** Run Step 1 with `--changed <the last release tag or main>` for the mechanical part. Then, for docs that describe code, compare `git log -1 --format=%cs -- <doc>` with the last change to the code it describes. Flag docs that are older than a significant change.
10. **Claims are sourced.** Factual claims carry a URL or an evidence label; unverified ones are in the verification backlog.

## Step 3 (setup only): fill, do not invent

- Fill each `TODO(docs)` from the code, the existing docs and the git history. If the repository does not show the answer, leave the placeholder and list it as a question for the owner. A confident guess in an architecture or security doc is worse than a visible gap.
- Write retroactive ADRs only for decisions the code clearly shows, with status `accepted`, the date you wrote it, and a note that it was recorded after the fact. Reasons you cannot find evidence for go in as "I cannot confirm this".
- Add every new file to the index (`docs/README.md`, and `docs/decisions/README.md` for ADRs). Add a changelog entry under Unreleased.
- Follow the repository's process: its branch naming, commit style, protected paths, and any docs map it generates. Do not edit existing CI workflows, hooks or `.claude/` unless the user asks for that in this session; adding `docs-check.yml` is the one CI change setup makes.
- Adding the docs check is a CI decision: record it in an ADR (and the changelog) in the repository's ADR folder.
- A README over the limit is split, not rewritten: move each section word for word into the file its kind belongs in, fix its relative links, leave a short landing page with links, and keep the old section anchors reachable by linking the new files.
- Re-run the script until it reports no `ERROR`, then do Step 2. Do not commit `docs-check.yml` while an `ERROR` remains.

## Evidence labels

Use these in docs and in the report: **[V]** you opened the primary source (or ran it) in this session, **[V2]** secondary source only, **[U]** not verified, **[Inference]** reasoned judgment. When something cannot be verified, write "I cannot confirm this" and add it to `docs/verification-backlog.md` (in audit mode, list it in the report instead).

## Report

End with this, shortest useful form, most serious first:

```
## Docs audit: <repo> at <commit>
Result: <N errors, N warnings from the script> · <N content findings>

### Must fix
- <file or section>: <what is wrong> → <what to do>

### Should fix
- ...

### Recorded deviations (no action)
- ...

### Questions for the owner
- <what the repository could not answer>

### Not checked
- <commands not run, sources not opened, and why>
```

Paste the script's summary line as it printed. Do not round findings up to "docs look good": say what was checked and what was not.

## Sources

The layout and conventions come from the owner's Perpetuity Machine Governing Guide (§3 evidence standard, §10.6 Learning Notes, §11 documentation system), which cites:

- Diátaxis, the four kinds of documentation: https://diataxis.fr/
- MADR, the ADR template: https://adr.github.io/madr/
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- Threat modelling by four questions, with STRIDE: named in the Guide §5.8 and §11

The Guide labels the first three **[V]** as read on 2026-11-07. They were **not** re-opened when this skill was written (the hosts were unreachable from that session), so treat the templates as following the Guide, not as independently re-verified against those sites.
