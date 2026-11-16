---
title: mini-perpetuity
summary: A small, local memory layer for AI clients, where nothing becomes trusted memory until a human approves it.
status: Early build
stack: [Python, PostgreSQL, MCP]
repo: https://github.com/dejaneiro555/mini-perpetuity
order: 2
---

## What it is

mini-perpetuity is a single-user memory layer that runs on your own machine. AI clients connect to it to search and fetch what you have chosen to remember. It exists for two reasons: to be a working personal memory, and to serve as a small-scale sandbox for the larger [Perpetuity Machine](/projects/perpetuity-machine/) design.

It is an early build, not production software.

## Why I'm building it

mini-perpetuity is the same idea as Perpetuity Machine at the scale of one person. Before asking an organization to trust a system with what it knows, I wanted the smallest version that works, one I can use myself. It is where I test the parts that matter most: memory that persists, a human approving what becomes trusted, and a record of what happened.

## How it works

- **Memory lives in PostgreSQL**, one database per instance.
- **Instances behave like separate accounts.** You can run any number of named instances, such as `personal`, `work` and `test`. Each has its own database, login role, config file and audit trail, and one instance's role cannot connect to another's database.
- **AI clients connect through an MCP server**, the single way a client reads memory. Each client is registered by name and bound to one instance.

## Human approval is the gate

Everything starts as **pending**, whether you wrote it or an AI client proposed it. Pending items are invisible to search and to every client, including the one that wrote them.

- An AI client can search approved memory and propose new notes. It cannot approve anything.
- Approval takes a separate approver password, typed at a terminal and stored nowhere; the database keeps only a hash.
- Approved notes are never edited in place. Corrections are recorded as new versions, with the reason kept.

## Everything is recorded

Searches and approval decisions are recorded in an append-only ledger, including the text of each search. Text that looks like a secret or a Social Security number is refused on the way in.

## Honest limits

The README documents what the design does not protect against. For example, an AI client that can run shell commands as your own user can bypass the server entirely, and all instances share one local database cluster. Writing those limits down is part of the project.
