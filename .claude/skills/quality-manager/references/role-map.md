---
name: quality-manager role map (canonical for System B)
description: Authoritative role-map for Sweet July Skin's System B (Quality Management). Sub-skill role-maps reference this file at runtime. SKILL.md, references, Asana writes, and Status/Gate field options stay role-based.
last_updated: 2026-07-31
---

# Role map — System B canonical

This is the canonical role-map for System B quality skills (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker, quality-manager). Sub-skill role-maps reference this file at runtime. When a role-holder changes, this is the source of truth.

| Role | Person | Holds gates on |
|---|---|---|
| Operator | Alvin Belt | All quality-side staging — drafts every decision before the Quality Gate approval. Also owns the quality **framework**: quality management system design, SOP framework, monthly quality-trend review cadence, and QoS threshold definitions. Retains the gate on SOP ratification and SOP annual review, and on SAE triage and recall kickoff (agency and legal exposure). |
| Quality Gate | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | **Primary quality control owner as of 2026-07-30.** Final quality check on anything related to quality of product or quality of documentation, across every function — each function still owns its own work, this gate sits on top of it. Holds gates on: complaint classification and first response, complaint trend calls, NCR review and NCR→CAPA conversion, root cause sign-off, CAPA verification / effectiveness / close, lab-finding classification and severity, vendor flags and vendor scorecard signals, batch holds and releases, near-expiry disposition, cross-cutting task creation, QoS threshold task creation, quality dashboard content. Calls out inconsistencies in product quality or documentation wherever they surface. |
| Technical Advisor | Perrine Calvet — Milinyc Beauty contractor | Provides technical guidance on R&D, Quality, Production and Regulatory **requirements for product**. Retains the gate on genuinely technical judgment: formula stage-gate technical sign-off, compatibility / stability / RIPT / PET decisions, in-market stability testing decisions, packaging development, and reformulation direction. **Consult-only** on every process-shaped gate above — she advises, the Quality Gate decides. Leadership can override a Perrine approval. |
| QA Manager | Covered internally by the Quality Gate | SOP §7 references a QA Manager who approves SOP revisions. As of 2026-07-30 that sits with Nicole as Quality Gate for review outcomes, and with the Operator for ratification of the SOP itself. No longer a vacant seat. |
| Department Manager | Varies by source | Vendor-driven CAPAs → Purchasing lead. Lab-driven → quality-lab-coordinator owner. Process-driven → Ops lead. Customer-driven → Quality Gate. Resolved at intake based on Source. |
| Quality execution (incoming) | PD Specialist — **open seat, phased in after the Ops Specialist** | Reports to Nicole. Its job description names running the quality system: CAPA, non-conformances, complaint intake and trend monitoring, lab results, supplier quality flags, batch lifecycle including stability and hold-release, and the quality dashboard. Until filled, the Operator executes and the Quality Gate approves. Do not assign to this seat — route to the Operator and note the intended transfer. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. Update sub-skill `references/role-map.md` files to match (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker). All five System B role-maps stay in sync.
5. If the change affects an in-flight CAPA, lab finding, batch hold, or complaint, comment on the affected task with the role-change rationale.

## Reading this against older skill text

Sub-skill SKILL.md files and SOP references still say "QA Lead approves" on process gates. Resolve **QA Lead → Quality Gate (Nicole)** for every process-shaped gate, and **QA Lead → Technical Advisor (Perrine)** only where the judgment is formula or testing. Where a file says "Voice of Customer," resolve to the Quality Gate — the customer-quality intake role folded into it. Skill bodies were deliberately left alone; this file is the runtime config and it wins.

## History

- **2026-07-31** — Quality function redesigned per the 2026-07-30 leadership review. Nicole Iturbe becomes the Quality Gate, holding the final check on product and documentation quality across every function, and takes the process-shaped gates that were QA Lead's. Perrine Calvet becomes Technical Advisor, retaining formula and testing gates and moving to consult-only on process. The Operator picks up explicit framework ownership. The QA Manager seat is no longer vacant — it is covered internally. Added the incoming PD Specialist row as the future quality-execution holder. Rationale in `decisions/log.md` 2026-07-30. Job title changes: none — this is gate ownership, not a retitle.
- **2026-05-09** — Corrected: Perrine is QA Lead (technical gates); Nicole Iturbe is Voice of Customer (customer-quality role). Earlier role-maps (v5.1 through v5.4 build) had Nicole as QA Lead in error.
- **2026-05-08** — quality-lab-coordinator (v5.3) and batch-lifecycle-tracker (v5.4) shipped with Nicole as QA Lead.
- **2026-04-29** — capa-coordinator (v5.2) shipped with Nicole as QA Lead.

## Why this lives in quality-manager

Sub-skills are portable; the role-map is org-specific runtime config. Centralizing in quality-manager means a role change lands in one file and propagates via sub-skill reference rather than five parallel updates.
