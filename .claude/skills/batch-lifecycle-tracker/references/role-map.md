---
name: batch-lifecycle-tracker role map
description: Current role-holders for batch-lifecycle-tracker. Single source of truth for who holds each role. SKILL.md and other references stay role-based; names live here only.
last_updated: 2026-05-09
---

# Role map

The skill reads role-holders from this file at runtime. SKILL.md, references, Asana writes, and Status/Gate field options all stay role-based. When a role-holder changes, only this file updates.

| Role | Person | Notes |
|---|---|---|
| Operator | Alvin Belt | VP of Operations, AC Brands. Holds the Operator gate. |
| QA Lead | Perrine | Technical QA/QC lead. Holds all technical gates across System B: CAPA closes, vendor flags, batch holds and releases, lab-finding escalations, SOP ratifications. Same holder as capa-coordinator and quality-lab-coordinator QA Lead — the three System B skills share the gate. |
| Voice of Customer | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Manages quality intake from the customer perspective. Flags when product quality doesn't meet customer expectations. Holds gates on complaint classification and complaint-driven escalations (in complaint-and-event-handler). For batch lifecycle, advisor on customer-driven holds (complaint-trend hold path per Job 4). |
| Department Manager | Varies by Hold Reason | Lab fail → QA Lead. Vendor signal → Purchasing lead. Process-driven → Ops lead. Resolved at hold opening. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. If the QA Lead or Voice of Customer role-holder changes, update capa-coordinator, quality-lab-coordinator, complaint-and-event-handler, and (post-v5.5) quality-manager role maps at the same time — System B skills share these roles.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
