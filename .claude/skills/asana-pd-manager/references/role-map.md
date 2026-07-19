---
name: asana-pd-manager role map (canonical for PD system)
description: Authoritative role-map for Sweet July Skin's PD system (the 7-skill PD intelligence cluster routed via sjs-pd-system). Sibling PD skills reference this file at runtime. SKILL.md, references, and Asana writes stay role-based.
last_updated: 2026-05-17
---

# Role map — PD system canonical

This is the canonical role-map for the PD system skills (asana-pd-manager, fireflies-asana-bridge, outlook-asana-bridge, asana-plm-bridge, outlook-plm-bridge, sjs-status-reporter, plus the asana-find-replace utility). When a role-holder changes, this is the source of truth. Quality (System B) and Regulatory (System C) role-maps live separately in their own umbrellas.

## Roles

| Role | Person | Holds gates on |
|---|---|---|
| Operator | Alvin Belt — VP of Operations, AC Brands | All PD-side staging. Every write confirms with the operator before commit per `references/confirmation-protocol.md`. |
| PD Lead | Perrine Calvet — Milinyc Beauty contractor | Owns PD / R&D / Quality / Regulatory work. Technical sign-off on formula stage moves, packaging dev calls, compatibility / stability / RIPT / PET decisions. Cross-flagged for any PD-side reformulation triggered by Quality or Regulatory reverse-handoffs. |
| PD Consult | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Strategy and consumer-side consult on PD decisions. Final-line approver alongside the President on direction-changing PD calls. |
| Approver — President | Danielle | Approves direction-changing PD decisions (launch scope, supplier change, kill calls). |
| Approver — Founder | Ayesha Curry | Founder approval on brand-line moves. Receives weekly PD signal via `ayesha-weekly-briefing`. |
| Operations Coordinator | Ciarra Robinson | Day-to-day Asana stewardship, follow-ups, status pulls. |
| Marketing | Soraya — Marketing Manager | Marketing-side coordination on launch readiness and brand-facing comms. |
| Creative — Director | Erin | Creative Director — packaging, artwork, brand visuals. |
| Creative — Contractor | Jan Haeck | Creative contractor under Erin — packaging / artwork execution. |
| Creative — Coordinator | Ivy | Supports Erin and Jan. |
| Social | Kate | Social Media Coordinator. Cross-flagged for launch comms. |

## Contact lookup

Contact emails live in Supabase wiki — `public.wiki_pages WHERE page_type='contact'`. Look up by `slug = 'contact/' || public.wiki_slugify(name)` or by content match. The four bridges load all contacts at run time.

When Alvin refers to a person by first name, map to the workspace user via `asana_get_workspace_users` before assigning. Never guess a user GID.

## Update protocol

1. Confirm the change with Alvin (Operator).
2. Update this file's tables.
3. Update `last_updated`.
4. Propagate to sibling PD skills that name a role-holder directly (fireflies-asana-bridge, outlook-asana-bridge, sjs-status-reporter) — keep the workspace-context tables in sync.
5. Cross-reference: if the change touches Quality or Regulatory roles, also update `quality-manager/references/role-map.md` and `regulatory-manager/references/role-map.md` per their update protocols.
6. If the change affects an in-flight PD task or stage move, comment on the affected task with the role-change rationale.

## Why this lives in asana-pd-manager

asana-pd-manager is the core engine of the PD system. Centralizing the PD role-map here means a role change lands in one file and propagates via sibling reference rather than parallel updates in every PD skill. Same pattern as `quality-manager/references/role-map.md` for System B.

## History

- **2026-05-17** — Externalized from inline asana-pd-manager v1 SKILL.md table. Adopted PD Lead (Perrine) / PD Consult (Nicole) framing to match `quality-manager/references/role-map.md` System B canonical (Perrine = QA Lead; Nicole = Voice of Customer). Earlier inline table did not separate the roles.
