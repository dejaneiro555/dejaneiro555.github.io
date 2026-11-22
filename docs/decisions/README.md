# Architecture Decision Records

One ADR per significant decision (a new dependency, a storage or security choice, a change of direction), reviewed like code.

- Template: [adr-template.md](adr-template.md) (MADR, https://adr.github.io/madr/).
- File names: `NNNN-title-with-dashes.md`, numbered in order.
- Statuses: `proposed`, `accepted`, `superseded by ADR-NNNN`.
- After acceptance an ADR is edited only to change its status. A changed decision is a new ADR that supersedes the old one.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-build-the-site-with-astro.md) | Build the personal site as a static site with Astro | accepted |
| [0002](0002-host-on-github-pages-via-actions.md) | Host on GitHub Pages, deployed by GitHub Actions on every push to main | accepted |
| [0003](0003-bundle-the-jost-font.md) | Bundle the Jost font with @fontsource-variable/jost | accepted |
| [0004](0004-docs-check-in-ci.md) | Check in CI that code changes come with their docs | accepted |
| [0005](0005-dev-container-for-codespaces.md) | Develop the site in a dev container, Codespaces first | accepted |
| [0006](0006-protect-main-with-a-ruleset.md) | Protect main with a ruleset: pull request and docs check required | accepted |
