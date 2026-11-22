---
status: accepted
date: 2026-11-21
decision-makers: Rio Gonzales (owner)
---

# Bundle the Jost font with @fontsource-variable/jost

## Context and Problem Statement

*Recorded after the fact on 2026-11-21: the decision was made on 2026-11-15, as the code and commits show. The reasons below are what the commits state; anything else is marked.*

The design uses the Jost typeface, which must render the same for every visitor.

## Considered Options

* Bundle the font with `@fontsource-variable/jost`
* Load it from a font CDN such as Google Fonts
* Rely on system fonts

## Decision Outcome

Chosen option: "Bundle with @fontsource-variable/jost", added in `8188ac4` (2026-11-15), whose message gives the reason: "consistent rendering".

### Consequences

* Good: the font is served from the site itself, so no third-party font request is made [Inference from how Fontsource packages work; not checked in the built output].
* Bad: one more npm dependency to keep updated.

### Confirmation

`src/layouts/Base.astro` imports `@fontsource-variable/jost` [V].

## Pros and Cons of the Options

### Bundle with Fontsource

* Good, because rendering does not depend on a CDN.
* Bad, because the font files add to the site's size.

## Threat-model impact

No new data flow to a third party at runtime [Inference]; the package is part of T3 (dependencies).

## Sources

* `package.json`, `src/layouts/Base.astro`, commit `8188ac4` [V]
