# QoS Threshold Definitions

Quality-of-service metrics pulled from oc3pl-order-manager and complaint-and-event-handler. Thresholds drive `[QoS Threshold Crossed]` task creation per Job 3 and SKILL.md cross-cutting-tasks.md §6.

Defaults set 2026-05-09 at v5.5 build. Revise after first quarter of data.

---

## 1. Metric definitions

### On-Time Delivery Rate

**Source:** OC3PL Order Management Asana project → 📋 Daily Report Log → latest task → "On-Time Delivery (≤24h)" line.
**Definition:** Percentage of orders shipped where Hours to Ship ≤ 24 (per oc3pl-order-manager Step 1).
**Window:** Rolling 7 days (sum of last 7 daily reports).
**Threshold:** < 95%.

### Fulfillment Rate

**Source:** OC3PL Order Management Asana project → 📋 Daily Report Log → latest task → "Fulfillment Rate" line.
**Definition:** Percentage of orders with a Shipment Date Time (per oc3pl-order-manager Step 1).
**Window:** Rolling 7 days.
**Threshold:** < 99%.

### Damage Rate

**Source:** SJ Shipping Dashboard (gid `1206266539116267`) — count of Returns + RTS where reason category is damage-related, divided by total orders shipped over the same window.
**Definition:** % of shipped orders where customer reported damage on receipt or carrier returned damaged.
**Window:** Rolling 30 days.
**Threshold:** > 0.5%.

### Missing/Incorrect Rate

**Source:** SJ Shipping Dashboard (gid `1206266539116267`) — count of Order Exceptions + Errors where reason category is missing-item or incorrect-item, divided by total orders shipped.
**Definition:** % of shipped orders where customer reported missing or incorrect items.
**Window:** Rolling 30 days.
**Threshold:** > 1%.

### Fulfillment-Related Complaint Trend

**Source:** complaint-and-event-handler → SJ Skin Complaint Log filtered to fulfillment categories (damage, missing, incorrect, late delivery, packaging issue).
**Definition:** % of shipped orders that generated a complaint coded to a fulfillment category.
**Window:** Rolling 30 days.
**Threshold:** > 3%.

---

## 2. Threshold detection cadence

- **Auto-fire:** during weekly rollup (Job 2 — Monday 9am PT). Skill reads each metric, compares against threshold, opens `[QoS Threshold Crossed]` task per Job 4 cross-cutting pattern.
- **On-demand:** any "QoS rollup" or "shipping quality this week" trigger reads metrics + flags crossings without opening a task (read-only path).
- **Threshold task creation always requires QA Lead approval.** Operator stages from auto-detection or on-demand; QA Lead approves on creation.

---

## 3. Threshold tuning

Defaults are starting points. Tune after first quarter of data based on observed baseline performance.

| Metric | Default threshold | Rationale | Tune after |
|---|---|---|---|
| On-Time Delivery | < 95% | Industry-standard SLA for DTC fulfillment | Q1 2027 quarterly review |
| Fulfillment Rate | < 99% | Most days should approach 100%; <99% indicates a sustained issue | Q1 2027 |
| Damage Rate | > 0.5% | Industry baseline for cosmetics DTC; low water-content products see lower damage | Q1 2027 |
| Missing/Incorrect Rate | > 1% | OC3PL pick accuracy SLA target | Q1 2027 |
| Fulfillment Complaint Trend | > 3% | Most fulfillment issues self-resolve via OC3PL refund/replace; >3% indicates a pattern customers can't absorb | Q1 2027 |

---

## 4. Cross-cuts

The QoS metrics intentionally cross multiple skills:

- **On-Time + Fulfillment** sit in OC3PL data → oc3pl-order-manager owns the operational signal.
- **Damage + Missing/Incorrect** sit in SJ Shipping Dashboard → oc3pl-order-manager owns the operational signal.
- **Complaint Trend** sits in complaint-and-event-handler → that skill owns intake; trend-crossing fires a separate alert there. quality-manager surfaces the cross-cut.

When a QoS threshold crosses AND complaint-and-event-handler has independently flagged a trend on the same window, both skills' tasks reference each other (multi-home or comment cross-link).

---

## 5. Pattern persistence and CAPA handoff

If the same metric crosses threshold for **2 consecutive windows** (2 weeks for 7-day metrics, 2 months for 30-day metrics), the QoS task escalates per cross-cutting-tasks.md §6:

- Stage a CAPA handoff to capa-coordinator with `source = QoS-threshold`.
- Include trend chart, both windows' metric values, and operational signals from the source skill.
- QA Lead approves the CAPA handoff stage.

This prevents one-off bad weeks from triggering CAPA fatigue while ensuring sustained quality drops get a root cause investigation.

---

## 6. Source-field mappings

| Metric | Source field path | Computation |
|---|---|---|
| On-Time | OC3PL Daily Report Log task description, "On-Time Delivery (≤24h): X%" line | Average across last 7 daily report tasks |
| Fulfillment | OC3PL Daily Report Log task description, "Fulfillment Rate: X%" line | Average across last 7 daily report tasks |
| Damage | SJ Shipping Dashboard tasks where category = damage AND created_at within last 30d, divided by sum of "Total Orders Shipped" across last 30 daily reports | Computed |
| Missing/Incorrect | SJ Shipping Dashboard tasks where category in (missing, incorrect) AND created_at within last 30d, divided by sum of "Total Orders Shipped" across last 30 daily reports | Computed |
| Complaint Trend | SJ Skin Complaint Log filtered to fulfillment categories, count within last 30d, divided by sum of orders shipped last 30d | Computed |

---

## 7. Open at first build session

- Confirm the exact category enum values used in SJ Shipping Dashboard for damage / missing / incorrect classification.
- Confirm the exact complaint category enum values used in SJ Skin Complaint Log for fulfillment-related complaints.
- Confirm Operations consensus on the default thresholds before they fire any tasks.
- Decide whether to backfill historical OC3PL Daily Report Log tasks for baseline calibration.
