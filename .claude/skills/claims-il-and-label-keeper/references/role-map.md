---
name: claims-il-and-label-keeper role map
description: Current role-holders for claims-il-and-label-keeper. Single source of truth for who holds each role. SKILL.md and other references stay role-based; names live here only.
last_updated: 2026-05-09
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
| QA Lead | Perrine | Technical QA/QC lead. Consult-only on quality-side overlaps (e.g., a label cross-check that surfaces a batch-affecting issue). Same holder as System B siblings (capa-coordinator, batch-lifecycle-tracker, quality-lab-coordinator). |
| Voice of Customer | Nicole Iturbe — Senior Director, Consumer Strategy & Operations | Consult-only on retailer attestation responses where customer-perceived attributes matter (e.g., Sephora Clean criteria interpretation). Same holder as System B siblings. |

## Update protocol

1. Confirm the change with the operator.
2. Update this file's table.
3. Update `last_updated`.
4. If the Reg Lead role splits at v6.3 (separate internal reg lead joins), update this file plus regulatory-manager and adverse-event-and-recall-reporter role maps at the same time.
5. If the QA Lead or Voice of Customer role-holder changes, update System B siblings (capa-coordinator, batch-lifecycle-tracker, quality-lab-coordinator, complaint-and-event-handler, quality-manager) at the same time — the role is shared.
6. If a Pedrero contact changes (Amy / Heather / Teona), update this file. The Outlook contacts are pulled from asana-pd-manager's contact catalog; cross-check that catalog stays in sync.

## Why this lives outside SKILL.md

Skills are portable. SKILL.md is the spec; role-holders are the runtime config. Mixing them couples the spec to the org chart and to the external partner roster, which makes the skill harder to lift across brands or hand off to another operator. Names in one file, role logic in the rest.
