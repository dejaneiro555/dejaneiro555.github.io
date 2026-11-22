# Verification backlog

Claims the project relies on that are not yet checked against a primary source. Labels: **[V]** verified against the primary source, **[V2]** secondary source only, **[U]** unverified.

| ID | Claim | Status | Where to check | Needed by |
|---|---|---|---|---|
| VB-02 | Why Astro and GitHub Pages were chosen over alternatives (ADR 0001, 0002) | [U] | the owner | ADR 0001, 0002 |

## How to close an item

Open the primary source, record the URL and the date read, change the label where the claim is made, and move the row to "Verified" below.

## Verified

| ID | Claim | Result | Evidence | Date |
|---|---|---|---|---|
| VB-03 | Astro's dev server is reachable through Codespaces port forwarding without `--host` | [V] yes | `[200] /` in the codespace's dev-server log after opening the forwarded port ([ADR 0005](decisions/0005-dev-container-for-codespaces.md)) | 2026-11-22 |
| VB-04 | Codespaces forwarded ports are private by default | [V] yes, for this codespace | Ports tab showed Visibility "Private" for port 4321, reported by the owner; GitHub's docs on the default were not opened | 2026-11-22 |
| VB-01 | The owner's GitHub account has two-factor authentication on | [V] yes (owner-reported; the CLI login lacks the `user` scope to read it) | Authenticator app configured, recovery codes saved in the password manager | 2026-11-22 |
