---
title: Care Navigator
summary: Referral coordination for patients, caregivers, navigators and organization admins, built as a runnable MVP on synthetic data.
status: Synthetic-data MVP
stack: [React, TypeScript, Django REST, PostgreSQL]
order: 4
---

## What it is

Care Navigator helps people follow through on referrals they already have. It coordinates the administrative side of care among four roles: patients, caregivers, navigators and organization admins. It does not provide clinical care and has no external integrations.

## How it works

- **Intake.** A patient records an administrative goal, existing referral instructions, providers, coverage, barriers and communication needs, then confirms a summary or asks a navigator for help.
- **Navigation.** A navigator accepts the request, creates tasks with an owner and due date, and records provider checks. Unknown, pending, verified, conflicting and stale evidence are all visible.
- **Referral tracking.** Each referral moves through defined stages from review to closed. Closing requires evidence; a booking alone cannot complete a referral.
- **Access control.** Patients grant or revoke a caregiver's read and communication permissions. Internal staff notes stay hidden from patients.
- **Organization isolation.** The two seeded demo organizations cannot see each other's data.

## Typing and speech

Typing works throughout. Speech input and spoken responses are optional, need explicit permission, and raw audio is not retained.

## Verification

The project has Django tests, frontend tests, end-to-end browser tests, and a backup-restore check.

## Where it stands

A runnable MVP on fictional data. It is not for live patients. The README lists what launch would require first, including staff multi-factor authentication, secure hosting, clinical escalation review, and independent accessibility testing. It makes no HIPAA-compliance, clinical-benefit or cost-savings claim.
