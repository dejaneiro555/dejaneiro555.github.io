# Architecture

How the system is built: system context (who and what talks to it), the main components, the data model, and where trust boundaries are. No diagram notation is in use yet.

## System context

A static personal website. Visitors' browsers fetch prebuilt HTML, CSS, fonts and images from GitHub Pages at https://dejaneiro555.github.io. There is no server-side code, no database, no forms and no client-side scripts in `src/` [V: `grep -rnE '<form|<script|fetch\(' src` found nothing, 2026-11-21]. Outbound links go to LinkedIn and GitHub only.

## Components (as of `main` at `8f7c15b`)

| Part | Path | What it does |
|---|---|---|
| Astro build | `astro.config.mjs`, `package.json` | Turns `src/` into static files in `dist/` (`npm run build`; 9 pages on 2026-11-21 [V]) |
| Layout | `src/layouts/Base.astro` | Shared page shell: title, canonical URL, link-preview image, navigation, footer links |
| Pages | `src/pages/` | `index`, `about`, `contact`, `journey`, `404`, `projects/index`, `projects/[id]` |
| Content collection | `src/content.config.ts`, `src/content/projects/*.md` | One Markdown file per project case study, checked against a schema (title, summary, status, stack, repo, order) |
| Styles and font | `src/styles/global.css`, `@fontsource-variable/jost` | Design tokens; the Jost font is bundled, not loaded from a font CDN |
| Static assets | `public/` | `favicon.svg`, `og.png` |
| Deploy | `.github/workflows/deploy.yml` | Builds and publishes on every push to `main` |
| Docs check | `.github/workflows/docs-check.yml`, `scripts/docs_audit.py` | Fails pull requests whose code changes skip the changelog or an ADR |

## Trust boundaries

1. The owner's GitHub account and the repository: whoever can push to `main` changes the live site.
2. GitHub Actions and the third-party actions it runs (`withastro/action`, `actions/*`), and npm packages installed during the build.
3. GitHub Pages serving the result to the public.

See [the threat model](../security/threat-model.md).

## Planned

- A dev container so the site can be developed in GitHub Codespaces (not started).
