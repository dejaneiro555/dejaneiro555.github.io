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

Humans became as capable as we are because we learned to pass knowledge on. Organizations are still bad at it. When someone leaves, what they knew usually leaves with them, because nobody had time to write it down.

I've worked in HR at four organizations and saw the same thing in every one. People want to understand their role and how to do their best work. Training and development gets left to managers and teams, and they end up feeling lost, overloaded and unsupported.

Perpetuity Machine is meant to preserve that knowledge for the team: record work as it happens, remember it, and return it to a shared knowledge base. Procedures can be drafted from that record and approved by people. New hires and AI agents can then learn from the real work, so they get up to speed faster and the pressure on managers and teammates drops.

This is about preserving knowledge, not monitoring people. Security and permissions come first, and people decide what becomes official.

## Where it stands

The project is in its foundations phase. The repository currently holds governance documents and project configuration, and no product code yet. The rules come before the software: how decisions are recorded, how changes are reviewed, and what data is allowed.

## Ground rules

- **Synthetic data only.** Nothing derived from real people is used until a later, explicitly gated phase.
- **Governed by a written guide.** One governing document wins over any conflicting instruction.
- **Reviewed changes.** Short-lived branches, conventional commit messages, and pull requests into the main branch, with no direct pushes.

## Related

[mini-perpetuity](/projects/mini-perpetuity/) is the small-scale, single-user sandbox where these ideas are being tried in working code.
