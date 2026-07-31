---
name: regulatory-status-reporter role map
description: Pointer to the canonical System C role-map at regulatory-manager/references/role-map.md. This skill renders the rollup; role-holders are inherited from the umbrella.
last_updated: 2026-07-31
---

# Role map

regulatory-status-reporter is the rendering layer. Role-holders for System C are defined canonically in `regulatory-manager/references/role-map.md`. This file points there rather than duplicating.

## Roles relevant to this skill

| Role | Person | Why it matters here |
|---|---|---|
| Operator | Alvin Belt | Approves every commit and push to acb-thelanding; approves every Asana attachment. |
| Reg Lead | Alvin Belt | Same person as Operator at v6.4. Approves layout changes, dashboard section adds, KPI tile redefinitions. |
| External Reg Partner | Pedrero Regulatory | Read-only on the dashboard. No write authority. |
| Technical Advisor | Perrine Calvet — Milinyc Beauty contractor | Technical guidance on R&D, Quality, Production and Regulatory requirements for product. Consult-only here. Was "QA Lead" through 2026-07-30. |
| Quality Gate | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Primary quality control owner as of 2026-07-30. Consult-only here, including where documentation quality is the question. Replaces the former "Voice of Customer" row. |

## Update protocol

1. Role-holder changes flow through `regulatory-manager/references/role-map.md` — update there.
2. This file's table refreshes from the canonical source on next read.

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

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart, which makes the skill harder to lift across brands or hand off to another operator.
