---
name: regulatory-status-reporter role map
description: Pointer to the canonical System C role-map at regulatory-manager/references/role-map.md. This skill renders the rollup; role-holders are inherited from the umbrella.
last_updated: 2026-05-09
---

# Role map

regulatory-status-reporter is the rendering layer. Role-holders for System C are defined canonically in `regulatory-manager/references/role-map.md`. This file points there rather than duplicating.

## Roles relevant to this skill

| Role | Person | Why it matters here |
|---|---|---|
| Operator | Alvin Belt | Approves every commit and push to acb-thelanding; approves every Asana attachment. |
| Reg Lead | Alvin Belt | Same person as Operator at v6.4. Approves layout changes, dashboard section adds, KPI tile redefinitions. |
| External Reg Partner | Pedrero Regulatory | Read-only on the dashboard. No write authority. |
| QA Lead | Perrine | Consult-only on cross-cutting overlaps surfaced in the rollup. |
| Voice of Customer | Nicole Iturbe | Consult-only on retailer attestation visualizations where customer-perceived attributes matter. |

## Update protocol

1. Role-holder changes flow through `regulatory-manager/references/role-map.md` — update there.
2. This file's table refreshes from the canonical source on next read.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart, which makes the skill harder to lift across brands or hand off to another operator.
