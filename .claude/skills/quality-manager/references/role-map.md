---
name: quality-manager role map (canonical for System B)
description: Authoritative role-map for Sweet July Skin's System B (Quality Management). Sub-skill role-maps reference this file at runtime. SKILL.md, references, Asana writes, and Status/Gate field options stay role-based.
last_updated: 2026-05-09
---

# Role map — System B canonical

This is the canonical role-map for System B quality skills (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker, quality-manager). Sub-skill role-maps reference this file at runtime. When a role-holder changes, this is the source of truth.

| Role | Person | Holds gates on |
|---|---|---|
| Operator | Alvin Belt | All quality-side staging — drafts every decision before QA Lead approval. |
| QA Lead | Perrine | Technical QA/QC lead. All technical gates: NCR review, NCR→CAPA conversion, root cause sign-off, verification, effectiveness review, CAPA close, vendor flags, vendor scorecard signals, batch holds and releases, lab-finding severity overrides, retest authority, SOP ratifications, SOP annual reviews, cross-cutting task creation, QoS threshold task creation. |
| Voice of Customer | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Customer-quality intake. Manages quality intake from the customer perspective. Holds gates on complaint classification and complaint-driven escalations (in complaint-and-event-handler). Advisor on complaint-driven CAPAs and complaint-trend batch holds. |
| QA Manager | Currently overlaps with QA Lead | Separate role created if/when an in-house QA Manager is hired. SOP §7 references a QA Manager who approves SOP revisions; at v5.5 that responsibility sits with Perrine (QA Lead). |
| Department Manager | Varies by source | Vendor-driven CAPAs → Purchasing lead. Lab-driven → quality-lab-coordinator owner. Process-driven → Ops lead. Customer-driven → Voice of Customer. Resolved at intake based on Source. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. Update sub-skill `references/role-map.md` files to match (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker). All five System B role-maps stay in sync.
5. If the change affects an in-flight CAPA, lab finding, batch hold, or complaint, comment on the affected task with the role-change rationale.

## History

- **2026-05-09** — Corrected: Perrine is QA Lead (technical gates); Nicole Iturbe is Voice of Customer (customer-quality role). Earlier role-maps (v5.1 through v5.4 build) had Nicole as QA Lead in error.
- **2026-05-08** — quality-lab-coordinator (v5.3) and batch-lifecycle-tracker (v5.4) shipped with Nicole as QA Lead.
- **2026-04-29** — capa-coordinator (v5.2) shipped with Nicole as QA Lead.

## Why this lives in quality-manager

Sub-skills are portable; the role-map is org-specific runtime config. Centralizing in quality-manager means a role change lands in one file and propagates via sub-skill reference rather than five parallel updates.
