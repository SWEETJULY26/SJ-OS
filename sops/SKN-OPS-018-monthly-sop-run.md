---
sop_id: SKN-OPS-018
title: Monthly S&OP Run Procedure
revision: "1"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-08-06
next_review_date: 2027-08-06
---

# Monthly S&OP Run Procedure

## 1. Purpose

Define the nine-step sequence a monthly sales and operations planning run follows, from pulling actuals through handing recommended buys to Purchasing — so forecast, inventory targets, and buy recommendations are produced the same governed way every cycle rather than depending on who happens to run it.

## 2. Scope

Applies to the recurring monthly S&OP cycle across all Sweet July Skin channels — DTC, wholesale/UBM, and Amazon where applicable. Covers demand forecasting, inventory target setting, buy recommendations, and the fill calendar. Does not cover the purchase order itself once a buy recommendation is approved (SKN-OPS-013) or the operational inventory writes that follow a target reset (owned by inventory management).

## 3. Definitions

- **Analogue method** — the technique used to forecast a new launch with no sales history, by proposing a comparable existing SKU's demand curve and having it ratified before the forecast commits. There is no standing analogue library — each new-launch forecast picks a fresh comparison.
- **Auto-adjustment** — a forecast factor applied from an external signal (competitive or retail intelligence) rather than from the SKU's own sales history.
- **Exception** — a SKU whose forecast, target, or buy recommendation crosses a defined threshold and is pulled out for individual review rather than clearing with the bulk approval.

## 4. Responsibilities

| Role | Responsibility |
|---|---|
| **Operations** | Runs the cycle, approves the bulk batch, reviews every exception individually. |
| **PD lead** | Ratifies the analogue chosen for any new launch before its forecast commits. |
| **Brand lead** | Ratifies the analogue chosen for any new launch before its forecast commits, alongside the PD lead. |
| **purchasing-manager** | Receives the finished-good and component buy recommendations at handoff. |
| **inventory-manager** | Receives the inventory targets at handoff. |

## 5. Procedure

### 5.1 Pull actuals

Sell-through and shipment data are pulled from every live channel — DTC, wholesale sell-in proxy, and Amazon where applicable — with a manual upload path always available as a fallback so the cycle never stalls on a data feed being down.

### 5.2 Run baseline forecast

A trailing-velocity plus seasonality forecast runs per SKU, per channel, per month. A new launch with no sales history uses the analogue method instead: an analogue SKU is proposed, and the PD lead and Brand lead ratify it before the forecast built on it commits.

### 5.3 Apply auto-adjustments

Signals from competitive and retail intelligence are read and converted into adjustment factors. Every adjustment applied surfaces in the run summary with its signal source, signal date, the math applied, and the before/after numbers — nothing shifts the forecast invisibly.

### 5.4 Compute targets

Safety-stock days, reorder points, and target days-of-supply are computed per SKU per channel, staged for review, and committed only after approval.

### 5.5 Recommend buys

Finished-good and component buy recommendations are drafted with vendor, target ship-by date, and rationale. Component recommendations run through a bill-of-materials explosion so a finished-good buy translates correctly into its underlying component needs.

### 5.6 Lay out the fill calendar

Recommended production is laid out at the month grain by contract manufacturer, with bulk-to-fill alignment notes per SKU per month. The fill calendar is internal-facing only — it is never sent to a filler directly from this process.

### 5.7 Auto-flag exceptions

Any SKU that clears a defined threshold is pulled out of the batch for individual review before the bulk approval clears. This is what keeps a genuinely unusual case from riding through on a batch approval meant for the routine majority.

### 5.8 Stage the writes

Forecast changes, target resets, auto-adjustments, and buy recommendations all draft and stage together. The batch clears on one bulk approval; each flagged exception is approved individually. Nothing commits to PLM until approval — this cycle never writes silently.

### 5.9 Hand off

Buy recommendations go to purchasing-manager. Targets go to inventory-manager. A branded one-pager summarizing the cycle goes out through the standard reporting path.

## 6. Records

| Record | Where it lives |
|---|---|
| Forecast lines | PLM forecast tables, one row per SKU per channel per month |
| Inventory targets | PLM inventory-targets table |
| Buy recommendations | S&OP project, Buy Recommendations section, picked up by Purchasing on approval |
| Fill calendar | S&OP project, Filler Schedule section, internal-facing |
| Run summary | S&OP project, with every auto-adjustment and exception itemized |

## 7. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-08-06 | Initial ratification, migrated from supply-demand-planner's working nine-step monthly run. | Alvin Belt |
