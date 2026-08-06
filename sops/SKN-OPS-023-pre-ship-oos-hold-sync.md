---
sop_id: SKN-OPS-023
title: Pre-Ship OOS Hold Sync Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Pre-Ship OOS Hold Sync Procedure

## 1. Purpose

Define the daily, unattended sync that turns the fulfillment warehouse's order-level out-of-stock signal into tracked pre-ship hold tasks — so an order blocked by a short SKU is visible and tracked to resolution every day, without requiring someone to remember to check for it.

## 2. Purpose boundary

This procedure owns order-level pre-ship holds only — which specific orders are blocked, and their triage or substitution decision. The SKU-level shortage signal (which SKUs are OOS, and by how much) belongs to inventory management's own procedure and is never duplicated here, even though both procedures read from the same source sheet.

## 3. Scope

Applies to the daily order-level OOS and short-SKU signal for DTC orders at the fulfillment warehouse. Runs alongside the daily fulfillment report parse, or independently on request. Does not cover the SKU-level shortage signal, which inventory management owns, and does not cover the substantive decision on an open hold beyond what this sync itself surfaces.

## 4. Definitions

- **Canonical row** — one order's current shortage state, merged from two source tabs into a single row per order number. Where an order appears in both source tabs, the more decision-advanced one wins.
- **Auto-close** — a hold task closing itself once its order is absent from both source tabs for two consecutive runs, rather than requiring a manual close.

## 5. Procedure

### 5.1 Fetch

The two order-level tabs from the fulfillment source sheet are pulled fresh on every run.

### 5.2 Merge into canonical rows

The two tabs are merged by order number. Where an order appears in both, the triaged tab's decision wins, and its response and substitution detail fold into that order's canonical row.

### 5.3 Open or update

For each canonical row, an existing open hold task is looked up by order number. If found, its body updates with the latest counts, source tab, and decision, and its name suffix updates from "awaiting triage" to the specific decision if the order has moved into the triaged tab since the last run. If not found, a new hold task opens.

### 5.4 Auto-close

For each currently open hold task, its order number is checked against both source tabs. Absent for two consecutive runs closes the task automatically, with a sync-back comment naming the run that cleared it. A single absent run is not enough to close — that guards against a one-run gap in the source data closing a hold that's still actually open.

### 5.5 Audit trail

Every run appends a summary to a standing daily log task, so the sync's own history is visible without reconstructing it from individual hold tasks.

### 5.6 What requires approval and what doesn't

The fetch, merge, and open/update/auto-close sync itself runs without any confirmation step — it is designed to run fully unattended. What does require approval is anything that changes a customer outcome: closing a hold because a substitution was actually actioned, or any similar disposition call, goes through the standing approval path for closing an open escalation. The sync surfaces the data; a person still decides what to do about a specific order.

## 6. Records

| Record | Where it lives |
|---|---|
| Hold task | OC3PL order management escalations queue, one per order number, open or auto-closed |
| Daily sync log | Standing rolling task, one summary comment per run |
| Auto-close event | Comment on the closed hold task naming the clearing run |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from oc3pl-order-manager's working Daily Pre-Ship Hold Sync. | Alvin Belt |
