---
name: regulatory-manager role map
description: Canonical System C role-map. Source of truth for who holds each role across regulatory-manager, claims-il-and-label-keeper, and adverse-event-and-recall-reporter. SKILL.md and other references stay role-based; names live here only. Sub-skill role-maps reference this file.
last_updated: 2026-05-09
---

# Role map

The skill reads role-holders from this file at runtime. SKILL.md, references, Asana writes, and Gate field options all stay role-based. When a role-holder changes, only this file updates — sub-skill role-maps point here.

| Role | Person | Notes |
|---|---|---|
| Operator | Alvin Belt | VP of Operations, AC Brands. Holds the Operator gate. Approves intake scope, fan-out routing, registration drafts, Pedrero engagement drafts. Submits agency filings and Pedrero sends manually after Reg Lead approval. |
| Reg Lead (internal) | Alvin Belt | Same person as Operator at v6.3. May split if a dedicated internal reg lead joins. Approves cross-skill task creation, registration writes, attestation reminder edits, fan-out routing decisions, every Pedrero send for engagement work. |
| External Reg Partner | Pedrero Regulatory | All substantive regulatory review across System C. No internal authority, no Asana access. Consult by Outlook only. Pedrero-specific contact details in `references/pedrero-contacts.md`. |
| QA Lead | Perrine | Technical QA/QC lead. Consult-only on cross-cutting overlaps (e.g., a regulatory inspection that surfaces a quality-system question). Same holder as System B siblings (capa-coordinator, batch-lifecycle-tracker, quality-lab-coordinator, quality-manager) and System C siblings (claims-il-and-label-keeper, adverse-event-and-recall-reporter). |
| Voice of Customer | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Consult-only on retailer attestation responses and SAE classification where customer-perceived attributes matter. Same holder as System B/C siblings. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. **System C role propagation.** This file is the canonical home of the System C role definition. When a role changes here, sub-skill role-maps automatically reflect it (claims-il-and-label-keeper and adverse-event-and-recall-reporter point to this file as source of truth). No need to update sub-skill role-maps separately.
5. **System B role coordination.** If the QA Lead or Voice of Customer role-holder changes, update System B siblings (capa-coordinator, batch-lifecycle-tracker, quality-lab-coordinator, complaint-and-event-handler, quality-manager) at the same time — the role is shared across both systems.
6. **Pedrero contact change.** Pedrero contact details live in `references/pedrero-contacts.md`. Update there; this role-map references the partner relationship abstractly. asana-pd-manager's contact catalog should also stay in sync.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart and to the external partner roster, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
