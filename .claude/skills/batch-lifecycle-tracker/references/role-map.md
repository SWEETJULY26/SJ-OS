---
name: batch-lifecycle-tracker role map
description: Current role-holders for batch-lifecycle-tracker. Single source of truth for who holds each role. SKILL.md and other references stay role-based; names live here only.
last_updated: 2026-07-31
---

# Role map

The skill reads role-holders from this file at runtime. SKILL.md, references, Asana writes, and Status/Gate field options all stay role-based. When a role-holder changes, only this file updates.

| Role | Person | Notes |
|---|---|---|
| Operator | Alvin Belt | VP of Operations, AC Brands. Holds the Operator gate. |
| Technical Advisor | Perrine Calvet — Milinyc Beauty contractor | Technical guidance on R&D, Quality, Production and Regulatory requirements for product. Retains formula, stability, RIPT, PET and packaging judgment. **Consult-only** on the process gates above. Was "QA Lead" through 2026-07-30. |
| Quality Gate | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | **Primary quality control owner as of 2026-07-30.** Final quality check on quality of product and quality of documentation. Holds every process-shaped gate in this skill — the gates this table previously assigned to QA Lead. Canonical definition in `quality-manager/references/role-map.md`. |
| Department Manager | Varies by Hold Reason | Lab fail → Quality Gate. Vendor signal → Purchasing lead. Process-driven → Ops lead. Resolved at hold opening. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. If the Quality Gate or Technical Advisor role-holder changes, update capa-coordinator, quality-lab-coordinator, complaint-and-event-handler, and (post-v5.5) quality-manager role maps at the same time — System B skills share these roles.

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

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
