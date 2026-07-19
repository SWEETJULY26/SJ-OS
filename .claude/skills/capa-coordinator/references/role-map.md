---
name: capa-coordinator role map
description: Current role-holders for capa-coordinator. Single source of truth for who holds each role. SKILL.md and other references stay role-based; names live here only.
last_updated: 2026-05-09
---

# Role map

The skill reads role-holders from this file at runtime. SKILL.md, references, Asana writes, and Status/Gate field options all stay role-based. When a role-holder changes, only this file updates.

| Role | Person | Notes |
|---|---|---|
| Operator | Alvin Belt | VP of Operations, AC Brands. Holds the Operator gate. |
| QA Lead | Perrine | Technical QA/QC lead. Holds all technical gates: NCR review, NCR→CAPA conversion, root cause sign-off, verification, effectiveness review, CAPA close, SOP ratifications. Same holder as quality-lab-coordinator and batch-lifecycle-tracker QA Lead — the three System B skills share the gate. |
| Voice of Customer | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Manages quality intake from the customer perspective. Flags when product quality doesn't meet customer expectations. Advisor on complaint-driven CAPAs and complaint-trend escalations. |
| Department Manager | Varies by source category | Vendor-driven CAPAs → Purchasing lead. Lab-driven CAPAs → quality-lab-coordinator owner. Process-driven CAPAs → Ops lead. Resolved at time of CAPA opening based on Source. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. If the QA Lead or Voice of Customer role-holder changes, update quality-lab-coordinator, batch-lifecycle-tracker, complaint-and-event-handler, and (post-v5.5) quality-manager role maps at the same time — System B skills share these roles.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
