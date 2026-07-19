---
name: Asana field GIDs pointer
description: Pointer to the canonical Asana custom field GID cache, which is shared by every skill that writes to SJS Asana projects.
last_updated: 2026-05-17
---

# Asana field GIDs — canonical pointer

The canonical Asana custom field GID cache lives at:

`/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`

This file is org-level canonical. It is shared by every skill that touches Asana custom fields — currently at least:

- `asana-pd-manager` (this skill)
- `claims-il-and-label-keeper`
- `quality-manager`
- `quality-lab-coordinator`
- `batch-lifecycle-tracker`
- `regulatory-manager`
- `adverse-event-and-recall-reporter`
- `quality-status-reporter`

Do not move or rename it. Moving it would force every consumer skill to update its path references and would create an artificial PD-system dependency for Quality and Regulatory skills.

If the canonical location ever changes, update this pointer first, then update every consuming skill in a single coordinated sweep.

## What lives in the canonical file

- Project GIDs for every SJS Asana project
- Section GIDs per project
- Custom field GIDs (single-select, text, date, multi-enum) per project
- Option GIDs for every single-select field used by skills

## What this skill uses from it

Most heavily: `SJ SKIN – Formula Development Tracker` (project GID `1213280384100264`) — specifically `IL Status` field GID `1214676606090922` and its option GIDs, plus the `SJS Regulatory Management` project (GID `1214660807386611`) Inbound Staging section GID `1214661463988658` and the `Artifact Type` and `Linked SKU` field GIDs.

For every other PD project (the 13 SJ SKIN product projects), look up by name on first use and cache in the conversation.
