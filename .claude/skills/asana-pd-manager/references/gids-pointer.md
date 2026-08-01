---
name: Asana field GIDs pointer
description: Pointer to the canonical Asana section, field, and option GID reference, shared by every skill that writes to SJS Asana projects.
last_updated: 2026-08-01
---

# Asana field GIDs — canonical pointer

The canonical reference is **`references/architecture/queue_registry.md`** in this repo, pulled live from Asana. It records, per queue: project GID, every section GID, the state field and its option GIDs, the state → section map, and which field is authoritative.

Cross-cutting identifiers that are not per-queue — workspace, teams, portfolios, the PLM project, M365 — live in `references/architecture/gids.md`.

**This pointer used to name a file on Alvin's Mac** — `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md` — and told consumers not to move it. Nothing running in a remote session or a scheduled Routine could ever read that path, so every consumer skill cached its own copy of the GIDs instead. That is how the SJS Quality Management section GIDs came to exist in four separate, silently diverging copies. The registry is in the repo precisely so there is one copy every consumer can actually open.

Consumers: `asana-pd-manager`, `claims-il-and-label-keeper`, `quality-manager`, `quality-lab-coordinator`, `batch-lifecycle-tracker`, `regulatory-manager`, `adverse-event-and-recall-reporter`, `quality-status-reporter`.

## What this skill uses from it

`SJ SKIN – Formula Development Tracker` — project `1213280384100264`, `IL Status` field `1214676606090922` and its options. Plus `SJS Regulatory Management` — project `1214660807386611`, Inbound Staging section `1214661463988658`, and the `Artifact Type` and `Linked SKU` field GIDs.

The Formula Development Tracker is a PD project and is **not yet in the registry**, which covers the eleven Ops/Quality/Regulatory queues named in `bridge_queue_contract.md`. Its GIDs stay cached here until the registry is extended to the PD projects. For the SJ SKIN product projects, look up by name on first use and cache in the conversation.

## When Asana changes

Re-pull the affected project with `get_project` (`include_sections`, `custom_field_settings`) and update the registry. Do not update a skill body's private copy instead — that is the failure this file exists to prevent.
