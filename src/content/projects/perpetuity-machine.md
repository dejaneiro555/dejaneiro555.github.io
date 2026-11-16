---
title: Perpetuity Machine
summary: A persistent, permission-aware memory layer for organizations, designed to sit beneath AI models and agents.
status: In design
stack: [Python, Shell]
order: 1
---

## What it is

Perpetuity Machine is a memory layer for organizations. It sits beneath AI models and agents and records what an organization knows and what it has done, keeping the evidence, history, permissions and provenance behind every memory.

The idea at its center: models are interchangeable, and the memory is the part that should last.

## Why I'm building it

I've worked in HR at four organizations and talked with people at many more. One problem followed me through every role and every conversation: people want to understand their role and how to do their best work, and organizations rarely have a reliable way to give them that.

Compensation is the comparatively simple part. It comes down to allocation and budgeting. Training and development is harder. It involves every person, function, department and manager, and it differs for each organization and industry. In my experience it gets left to managers and teams to figure out, and they end up feeling lost, overloaded and unsupported.

That thought is what led me here. An organization that reliably remembers what it knows and what it has done, with the evidence behind it, can support its people far better. And when someone turns out not to be the right fit, it can show that they were given the best support possible.

## Where it stands

The project is in its foundations phase. The repository currently holds governance documents and project configuration, and no product code yet. The rules come before the software: how decisions are recorded, how changes are reviewed, and what data is allowed.

## Ground rules

- **Synthetic data only.** Nothing derived from real people is used until a later, explicitly gated phase.
- **Governed by a written guide.** One governing document wins over any conflicting instruction.
- **Reviewed changes.** Short-lived branches, conventional commit messages, and pull requests into the main branch, with no direct pushes.

## Related

[mini-perpetuity](/projects/mini-perpetuity/) is the small-scale, single-user sandbox where these ideas are being tried in working code.
