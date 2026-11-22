# CLAUDE.md

Rio Gonzales's personal portfolio site: Astro, static output, hosted on GitHub Pages. See [docs/README.md](docs/README.md).

## Commands

- `npm ci` installs dependencies from `package-lock.json` (not run in the 2026-11-21 session; `node_modules` already existed).
- `npm run dev` starts the dev server on http://localhost:4321 (ran 2026-11-21: HTTP 200). Started from a non-interactive shell (as in a Claude session) it ran in the background; stop it with `npx astro dev stop`, check it with `npx astro dev status`.
- `npm run build` builds into `dist/` (ran 2026-11-21: 9 pages).
- `python3 scripts/docs_audit.py --root . --changed origin/main` runs the docs check CI runs.

## Rules for this repository

- This is a learning project: explain the why, let the owner write key parts, then review.
- Pushing to `main` deploys the live site. Work on a branch and open a pull request.
- Code changes need a `CHANGELOG.md` entry; new dependencies, hosting or CI choices need an ADR in `docs/decisions/`.
- Do not commit `dist/`, `.astro/`, `node_modules/` or `graphify-out/`.
