---
name: claims-il-and-label-keeper role map
description: Current role-holders for claims-il-and-label-keeper. Single source of truth for who holds each role. SKILL.md and other references stay role-based; names live here only.
last_updated: 2026-07-31
---

# Role map

The skill reads role-holders from this file at runtime. SKILL.md, references, Asana writes, and Gate field options all stay role-based. When a role-holder changes, only this file updates.

| Role | Person | Notes |
|---|---|---|
| Operator | Alvin Belt | VP of Operations, AC Brands. Holds the Operator gate. Approves intake, classification, IL packet contents, claim sub writes, label archive entries, attestation drafts. |
| Reg Lead (internal) | Alvin Belt | Same person as Operator at v6.1. v6.3 may split if a dedicated internal reg lead joins (regulatory-manager build). Approves every Pedrero send, every retailer submission, every IL archive write. The Reg Lead gate fires as a separate confirmation step from Operator gate so the audit trail captures both decisions. |
| External Reg Partner | Pedrero Regulatory | All substantive regulatory review. No internal authority, no Asana access. Consult by Outlook only. |
| External Reg Partner — Principal | Amy Pedrero (amy@pedreroregulatory.com) | Primary contact on every Pedrero send |
| External Reg Partner — Secondary | Heather Folkes (heather@pedreroregulatory.com) | Cc on every send |
| External Reg Partner — Secondary | Teona Bebia (teona@pedreroregulatory.com) | Cc on every send |
| Technical Advisor | Perrine Calvet — Milinyc Beauty contractor | Technical guidance on R&D, Quality, Production and Regulatory requirements for product. Consult-only here. Was "QA Lead" through 2026-07-30. |
| Quality Gate | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Primary quality control owner as of 2026-07-30. Consult-only here, including where documentation quality is the question. Replaces the former "Voice of Customer" row. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. If the Reg Lead role splits at v6.3 (separate internal reg lead joins), update this file plus regulatory-manager and adverse-event-and-recall-reporter role maps at the same time.
5. If the Quality Gate or Technical Advisor role-holder changes, update System B siblings (capa-coordinator, batch-lifecycle-tracker, quality-lab-coordinator, complaint-and-event-handler, quality-manager) at the same time — the role is shared.
6. If a Pedrero contact changes (Amy / Heather / Teona), update this file. The Outlook contacts are pulled from asana-pd-manager's contact catalog; cross-check that catalog stays in sync.

| Artwork technical authority | Erin Hover — contractor | Lead technical authority on packaging and artwork as of 2026-07-31. Answers for the artwork being correct on the label archive and cross-check work; the **Reg Lead still gates the archive entry itself**, so the artwork authority and the regulatory approval are deliberately two different people. Jan Haeck executes under her. Canonical definition in `asana-pd-manager/references/role-map.md`. |

## Reading this against older skill text

This file mirrors the canonical role-map. SKILL.md and SOP references in this skill still say
"QA Lead" and "Voice of Customer." Resolve **QA Lead → Quality Gate (Nicole)** for process-shaped
gates, **QA Lead → Technical Advisor (Perrine)** only where the judgment is formula or testing, and
**Voice of Customer → Quality Gate (Nicole)**. Skill bodies were deliberately left alone; the
role-map is the runtime config and it wins.
## History

- **2026-07-31** — Quality function redesigned per the 2026-07-30 leadership review. Nicole Iturbe
  is the Quality Gate and holds the process-shaped gates formerly labelled QA Lead. Perrine Calvet
  is the Technical Advisor, retaining formula and testing judgment and consult-only on process. See
  the canonical role-map and `decisions/log.md` 2026-07-30. No job titles changed.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart and to the external partner roster, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
