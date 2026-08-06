---
sop_id: SKN-OPS-012
title: PD Readiness → PO Request Handoff Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# PD Readiness → PO Request Handoff Procedure

## 1. Why this exists

Every SKU project carries a task asking for a purchase order — artwork approved, formula signed off, quantities settled, supplier confirmed. That task is a request, not the order, and treating it as one has caused real damage: PD milestones ended up sitting inside the purchasing queue carrying no purchase-to-pay state, where nothing could ever move them. This procedure keeps the two work items distinct with a clean, three-part handoff between them.

## 2. Scope

Applies to every purchase order that traces back to a PD readiness milestone — packaging, formula fill, or any component tied to a specific SKU launch or reformulation. Does not apply to a routine reorder against an already-launched SKU with no PD gate in play — that starts directly at PO placement.

## 3. Definitions

- **PD request** — the task representing PD's own readiness: artwork approved, formula signed off, quantities settled, supplier confirmed. No PO number exists yet. Closes when the PO is created.
- **Purchasing order** — the task representing the purchase-to-pay lifecycle from the moment a PO number exists: Draft → Sent → Acknowledged → In Transit → Received → Closed. Closes when the invoice matches.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **PD** | Owns the PD request — gates it on readiness, never on purchase-to-pay state. |
| **Operations** | Owns the Purchasing order from the moment a PO number exists through invoice close. |

## 5. Procedure

### 5.1 The two-task rule

The PD request and the Purchasing order are different work items with a handoff, and both stay open independently. A one-person test settles which task closes when: "create the PO" closes when the PO exists; the PO task closes on invoice match. Two closes, two tasks — never one task carrying both.

### 5.2 Naming

- PD side: `[PO Request] <SKU> — <what is being bought>`.
- Purchasing side: `PO <number> — <vendor>`.

The prefix is what makes the chain legible on sight — a request reads as a request, an order reads as an order.

### 5.3 Never multi-home the PD request into Purchasing

A PD milestone dropped into a purchase-to-pay queue carries no purchase-to-pay state, so nothing can ever move it along that queue's workflow — it sits in Receiving forever. The two tasks stay in their own projects, linked, never sharing a home.

### 5.4 One request, several orders

One PD readiness gate routinely spawns more than one PO — primary packaging, secondary carton, and formula fill are commonly three separate purchase orders against one readiness milestone. Several Purchasing tasks depending on one PD request is the expected, correct shape, not a data error.

### 5.5 The three-way link

When the PO is placed against a PD request, all three of the following are set in the same action, not staggered across separate writes:

1. **Dependency.** The Purchasing order task is set to depend on the PD request task. This expresses the actual gate — a PO should not go out against artwork that isn't approved yet — and is visible from both sides without either project owning the other's task.
2. **Link fields.** The Purchasing task's linked-project, linked-SKU, and PLM product fields are filled so the PO is self-describing without anyone needing to open the PD side to know which SKU it serves. Where no PD project exists (an in-market SKU reordering components with no active PD gate), this is marked explicitly as not applicable rather than left blank.
3. **The PO number flowing back.** On creation, the PO number and vendor are commented onto the PD request task, so PD sees the placement without leaving its own project.

### 5.6 Readiness gate at placement

A PO traces its trigger to one of: an approved reorder review, an NPI ramp, a manual request, or a PD request task reaching readiness. In every PD-linked case, the dependency link in §5.5 is what actually enforces the gate — a PO should not be placed against unapproved artwork or an unsigned formula, and the dependency makes that visible and checkable on both sides.

## 6. Records

| Record | Where it lives |
|---|---|
| PD request state | PD SKU project, one task per readiness gate |
| Purchase order state | Purchasing queue, one task per PO, Draft through Closed |
| Link between the two | Task dependency plus the four linked-project/SKU/PLM fields on the Purchasing task |
| PO number sync-back | Comment on the PD request task |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from the working handoff rule already governing asana-pd-manager and purchasing-manager. | Alvin Belt |
