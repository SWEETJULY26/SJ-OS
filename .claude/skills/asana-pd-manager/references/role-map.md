---
name: asana-pd-manager role map (canonical for PD system)
description: Authoritative role-map for Sweet July Skin's PD system (the 7-skill PD intelligence cluster routed via sjs-pd-system). Sibling PD skills reference this file at runtime. SKILL.md, references, and Asana writes stay role-based.
last_updated: 2026-07-31
---

# Role map — PD system canonical

This is the canonical role-map for the PD system skills (asana-pd-manager, fireflies-asana-bridge, outlook-asana-bridge, asana-plm-bridge, outlook-plm-bridge, sjs-status-reporter, plus the asana-find-replace utility). When a role-holder changes, this is the source of truth. Quality (System B) and Regulatory (System C) role-maps live separately in their own umbrellas.

## Roles

| Role | Person | Holds gates on |
|---|---|---|
| Operator | Alvin Belt — VP of Operations, AC Brands | All PD-side staging. Every write confirms with the operator before commit per `references/confirmation-protocol.md`. |
| Technical Advisor | Perrine Calvet — Milinyc Beauty contractor | Technical guidance on R&D, Quality, Production and Regulatory **requirements for product**. Technical sign-off on formula stage moves, packaging dev calls, compatibility / stability / RIPT / PET decisions, in-market stability testing. Cross-flagged for any PD-side reformulation triggered by Quality or Regulatory reverse-handoffs. Consult-only on process-shaped quality and regulatory gates — see `quality-manager/references/role-map.md`. Was "PD Lead" through 2026-07-30; the label changed, the technical scope did not. |
| PD Consult + Quality Gate | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Strategy and consumer-side consult on PD decisions. Final-line approver alongside the President on direction-changing PD calls. **As of 2026-07-30 also holds the Quality Gate** — the final check on quality of product and quality of documentation across every function, including PD document control (specifications, dielines, artwork versions, BOMs, landed cost). Canonical definition lives in `quality-manager/references/role-map.md`. |
| Approver — President | Danielle | Approves direction-changing PD decisions (launch scope, supplier change, kill calls). |
| Approver — Founder | Ayesha Curry | Founder approval on brand-line moves. Receives weekly PD signal via `ayesha-weekly-briefing`. |
| Operations Specialist | **Open seat — recruiting now.** Reports to Nicole. | Prioritized first per the 2026-07-30 leadership review; target in place before Q4. Per its job description: daily order operations and the OC3PL relationship, channel operations across DTC / UBM / Amazon including promo setup, inventory reconciliation and FEFO and OOS signals, receiving, purchase-to-pay, freight and customs and brokers, routing-guide and ASN compliance, S&OP support, production scheduling, and label / PR seeding / sampling projects. Until filled, route by the interim split below. **Never assign to this seat** — it has no workspace account. |
| PD Specialist | **Open seat — phased in after the Operations Specialist.** Reports to Nicole. | Per its job description: PD portfolio across 20+ SKUs, document control (specifications, drawings, dielines, artwork versions, BOMs, landed-cost integrity), running the quality system, and product regulatory work (pre-launch IL and label review, claim substantiation, retailer compliance responses, registration tracker, external regulatory partner coordination). Scoped in the review as project management and accountability, not strategy or ideation. Until filled, route to the Operator. **Never assign to this seat.** |
| Interim coverage — retired Ops Coordinator seat | Alvin (inventory, logistics), Nicole Iturbe (order management, OC3PL) | The 2026-07-17 decision retired the Operations Coordinator role rather than backfilling it. This interim split is live until the two seats above are filled. Day-to-day Asana stewardship, follow-ups and status pulls route by it. |
| Marketing | Soraya — Marketing Manager | Marketing-side coordination on launch readiness and brand-facing comms. |
| Creative — Director | Erin Hover — **contractor** | Creative Director and **lead technical authority on packaging and artwork**. Holds the gate on packaging development, artwork execution, and the label artwork archive (the artwork itself — the Reg Lead still gates the regulatory archive entry, so those are two people). Perrine consults where formula contact or compatibility is in play. Danielle and Ayesha both consult on creative direction. |
| Creative — Contractor | Jan Haeck — contractor | Packaging Engineer, executes under Erin — packaging / artwork production. Titled "Packaging Engineer" in `sjs-comp-intel/references/team-ownership.md:79`; both framings refer to the same scope. |
| Creative — Coordinator | Ivy | Supports Erin and Jan. Owns Creative Requests intake and design coordination (`sjs-status-reporter/SKILL.md:352`). |
| Brand custody | Danielle — President | Holds the gate on brand guideline custody and on campaign direction. Erin maintains the guidelines; Soraya runs campaigns. Ayesha consults on both. |
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

## Departed role-holders

When someone leaves, the role row is marked vacant here **in the same pass** as the departure — a stale row is worse than a blank one, because every skill resolving followers off this map will keep trying to add a user who no longer has an account, and `asana_task_contract.md` Phase 3 will surface an unresolved-role-holder question on every write until it's fixed.

Checklist when a role-holder departs:

1. Mark the role vacant here with the interim coverage, and note the decision that set it.
2. Remove the person from any people list in a skill body (`outlook-asana-bridge` internal-ask row, `fireflies-asana-bridge` meeting-type table).
3. Remove their address from any automation recipient list — `ac-brands-holiday-comms` BCC is the live one.
4. Update their `contact/<slug>` wiki page to departed so the bridges' run-time lexicon stops resolving them as internal.
5. Sweep Asana for tasks assigned to them and reassign — an unassigned task has no owner and drops out of every per-person sweep, so it goes stale silently.

- **2026-07-31 (second pass)** — Role corrections from Alvin. Erin Hover marked as a **contractor** and named **lead technical authority on packaging and artwork**; packaging development moved from Perrine's gate to Erin's, with Perrine consulting on formula contact. Jan's row reconciled with the "Packaging Engineer" title used in comp-intel. Danielle added as the brand-custody and campaign-direction gate; Ayesha added as consult on brand and creative work rather than informed-only. Three of the four Creative-chain holders are contractors — flagged on the RACI Gaps sheet.
- **2026-07-31** — Quality function redesigned per the 2026-07-30 leadership review. "PD Lead" relabelled Technical Advisor (Perrine — technical scope unchanged, consult-only on process gates). Nicole added the Quality Gate alongside PD Consult. The vacant Operations Coordinator row was replaced by the two open specialist seats with their JD scopes and reporting line, and the interim split moved to its own row. Canonical quality definitions live in `quality-manager/references/role-map.md`. Rationale in `decisions/log.md` 2026-07-30. No job titles changed.
- **2026-07** — Ciarra Robinson (Operations Coordinator) departed. Role retired rather than backfilled, per the 2026-07-17 decision. Her Asana tasks were moved into a holding project (`Ciarra Robinson's previously assigned tasks`, gid `1216923783441065`) and reassigned to Alvin under the interim split on 2026-07-30; the holding project was archived in the same pass. Her Asana account is deprovisioned — she is not a workspace user, so she cannot be assigned or added as a follower.

## History

- **2026-07-29** — Operations Coordinator marked vacant; Ciarra Robinson departed. Added the departed-role-holder checklist above after the stale row surfaced during the `asana_task_contract.md` build (Phase 3 collaborator resolution found a mapped role-holder with no workspace account).
- **2026-05-17** — Externalized from inline asana-pd-manager v1 SKILL.md table. Adopted PD Lead (Perrine) / PD Consult (Nicole) framing to match `quality-manager/references/role-map.md` System B canonical (Perrine = QA Lead; Nicole = Voice of Customer). Earlier inline table did not separate the roles.
