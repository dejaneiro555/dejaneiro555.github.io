# Verification backlog

Claims the project relies on that are not yet checked against a primary source. Labels: **[V]** verified against the primary source, **[V2]** secondary source only, **[U]** unverified.

| ID | Claim | Status | Where to check | Needed by |
|---|---|---|---|---|
| VB-01 | The owner's GitHub account has two-factor authentication on (threat T1) | [U] | GitHub → Settings → Password and authentication | threat model |
| VB-02 | Why Astro and GitHub Pages were chosen over alternatives (ADR 0001, 0002) | [U] | the owner | ADR 0001, 0002 |
| VB-03 | Astro's dev server is reachable through Codespaces port forwarding without `--host` | [U] | a Codespace running `npm run dev` | dev container step |

## How to close an item

Open the primary source, record the URL and the date read, change the label where the claim is made, and move the row to "Verified" below.

## Verified
