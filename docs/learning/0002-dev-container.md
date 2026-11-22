# Learning Note 0002: a dev container for Codespaces

## What we did

The owner wrote `.devcontainer/devcontainer.json` (four properties), ADR 0005 recorded why, and a codespace built from the branch ran the site on 2026-11-22.

## How it works

- A **dev container** is a container described by a file in the repository. GitHub Codespaces reads `.devcontainer/devcontainer.json` and builds the environment from it.
- `image` picks the starting point: Microsoft's Node image, tag `26`. A **tag** names one version of an image; `26` follows Node 26 releases, `latest` follows whatever is newest, and a full version like `v26.13.1` is not a tag this registry publishes.
- `postCreateCommand` runs once after the container is built. `npm ci` installs exactly what `package-lock.json` lists, which `npm install` does not promise.
- `forwardPorts` connects a port inside the container to a URL your browser can open.

## What went wrong, and why it matters

- The tag went through `latest` and `v26.13.1` before `26`. `latest` would let the environment change without a commit; `v26.13.1` does not exist, so the build would fail.
- The official dev container CLI needs Docker even to read a config, and this Mac has none. The file was checked by parsing it, then by building a real codespace.
- A command meant for the codespace was first run on the Mac (`/Users/...` in the error gave it away). The prompt path tells you which machine you are on: `/workspaces/...` is the container.
- Giving the GitHub CLI the `codespace` permission would also have reached the owner's work organization, which does not restrict outside apps. The codespace was created from the browser instead.

## What is still open

- VB-04 is answered for this codespace (port 4321 was Private), but GitHub's documentation of the default was not opened.
- `npm ci` running was inferred from Astro starting; the creation log was not read.

## Exercise

In the codespace, run `cat /etc/os-release` and `which node`. Which Linux distribution does the image use, and where is Node installed?

## Sources

* https://containers.dev/implementors/json_reference/ [V, read 2026-11-21]
* https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers [V, read 2026-11-21]
* The codespace's terminal output, pasted by the owner on 2026-11-22 [V]
