# Trigger Phrases

The skill triggers on any of the phrases below, plus close paraphrases. Triggers are grouped by intent so the skill can route to the right job quickly.

If the operator says something that doesn't match a trigger but clearly belongs in purchasing (vendor, PO, sourcing, compliance, contract), default to scoping the request before acting.

---

## Vendor lookup / status

- "what's the latest with [vendor]"
- "pull up [vendor]"
- "vendor record for [name]"
- "show me [vendor]"
- "is [vendor] active"
- "who's our vendor for [component]"

→ Reads PLM vendor record, summarizes status, recent POs, open tasks, compliance state.

---

## New vendor / onboarding

- "new vendor coming in"
- "vendor coming in"
- "new vendor"
- "got an intro from [vendor]"
- "set up [vendor]"
- "onboard [vendor]"
- "[vendor] reached out about [thing]"
- "we're working with a new supplier — [name]"
- "[vendor] sent over their NDA"
- "vendor is sending docs"
- "did [vendor] clear onboarding"
- (auto) outlook-plm-bridge flags an inbound from an unknown sender/domain

→ Job 2 (2A → 2D): opens `Onboarding — Vendor Name` task in **Vendor Onboarding**, assignee per the `vendor_type` first-contact routing rule. HITL Proceed gate at 2B; on Proceed the six doc subtasks auto-create (2C). NDA + W9 complete fires the gate — task auto-moves to **Compliance, Renewals & Disputes** for PLM record creation (2D, HITL).

---

## PO actions

- "place a PO for [X]"
- "draft a PO for [X]"
- "status on PO [number]"
- "what's the status of PO [number]"
- "ack came in for [PO]"
- "issued PO [number]" (manual marker)
- "close out PO [number]"
- "PO [number] received"
- "what POs need attention"
- "what POs are open"
- "any variances I need to look at"

→ Job 3: routes to the right sub-flow (3a–3f).

---

## Receipt / receiving

- "log the receipt for PO [number]"
- "[vendor] delivered"
- "OC3PL flagged a receipt"
- "receipt is in"
- "create a receiving task for [PO]"
- "Logiwa receipt order [ref]"
- "PO [number] received"
- (auto) OC3PL / logistics-manager notifies on goods received

→ Job 3e: PD-linked PO (Scenario A) → set PLM Link on the existing PD task and multi-home it into **Receiving**; standalone PO (Scenario B) → open `Receipt — Vendor Name — PO Number` in **Receiving**. Operator records the Logiwa Receipt Order ref and counts, marks Status = **Received**; `plm-assistant` writes the PLM PO status and batch entry. Any count variance, damage, or missing items opens a Job 10 discrepancy task.

---

## Receipt discrepancy / damage

- "log a discrepancy on PO [number]"
- "[vendor] shipped short"
- "damaged units on receipt"
- "OC3PL flagged a count variance"
- "open a discrepancy task"
- "escalate this receipt to CAPA"
- "vendor credit for the [vendor] receipt"
- (auto) logistics-manager / OC3PL flags a vendor-attributable receipt issue

→ Job 10: opens `Discrepancy — Vendor Name — PO Number` in **Compliance, Renewals & Disputes**, inheriting the PO's multi-home set. Operator investigates and sets Resolution (Vendor Credit / Replacement Shipment / Accepted As-Is / Escalate to CAPA). Escalate to CAPA hands off to `capa-coordinator`; close feeds the vendor scorecard via `asana-plm-bridge`.

---

## Vendor performance

- "how's [vendor] doing"
- "scorecard for [vendor]"
- "quarterly vendor review"
- "vendor performance review"
- "are we having issues with [vendor]"
- "show me [vendor] on-time rate"

→ Job 5: pulls PLM PO history, composes scorecard. Branded output via sjs-status-reporter when needed.

---

## Compliance

- "missing docs for [vendor]"
- "what's missing on [vendor]"
- "COA came in for [batch]"
- "what COIs expire this quarter"
- "compliance gaps"
- "what's expiring on the vendor side"
- (auto) outlook-plm-bridge routes a compliance doc inbound

→ Job 7: files docs, flags gaps.

---

## Contracts and terms

- "contract renewal for [vendor]"
- "[vendor] is up for renewal"
- "payment terms changed for [vendor]"
- "[vendor] just sent new terms"
- "dispute with [vendor]"
- "we have a problem with [vendor] — invoice doesn't match"
- "what renewals are coming up"

→ Job 8: opens `Renewal — Vendor Name — 60d / 30d / 15d` or `Dispute — PO Number — Vendor` task in **Compliance, Renewals & Disputes**. Renewals run automatically via the weekly Monday `purchasing-renewal-sweep` (PLM `contract_renewal_date` at 60/30/15-day windows) and also fire on operator request. Disputes get Status = Dispute.

---

## Reorders (manual-trigger only in v1)

- "review reorders for [SKU]"
- "should we reorder [component]"
- "are we running low on [item]"
- "reorder check"

→ Job 6: opens `Reorder Review — SKU/Component` task in **HITL — Needs Operations Review**. HITL.

*Note:* In v1, reorder review only fires on operator request. Inventory-driven auto-triggering is the future Demand Planner skill's job.

---

## Sourcing / RFQs

- "find an alt supplier for [component]"
- "RFQ status"
- "how's the RFQ on [thing] going"
- "qualifying [vendor] for [X]"
- "we need a backup for [vendor]"
- "what's our second source for [component]"

→ Job 4: opens / updates RFQ task with supplier evaluation tracking.

---

## Vendor record alignment

- "align vendors"
- "sweep the vendor records"
- "are vendors in sync"
- "audit our vendors"
- (auto) weekly schedule

→ Job 1: cross-checks PLM / Asana / Outlook, opens discrepancy tasks.

---

## Generic / overview

- "what's open in purchasing"
- "purchasing status"
- "what's my P2P queue"
- "catch me up on purchasing"
- "what needs my attention in purchasing"

→ Scans the AC Brands Purchasing project by section + Status field. HITL queue = everything in **HITL — Needs Operations Review** (regardless of Status — covers PO Drafts, Variances, reorder review, cancellation review). Onboarding queue = **Vendor Onboarding** (2B awaiting Proceed, 2C collecting docs). In-flight POs = Status in {Sent, Acknowledged, In Transit}. Receiving = Status = Received. Stuck = Status = On Hold. Closed (history) = Status in {Closed, Cancelled}. Compliance / renewal / dispute work pulls from **Compliance, Renewals & Disputes**. Sourcing pulls from **Sourcing & RFQ**. Summarizes by section.

---

## Routing notes

- If the operator names a specific PO number, route directly to Job 3 sub-flow based on current PO state in PLM.
- If the operator names a specific vendor, default to vendor lookup unless an action verb is present.
- If the request touches PD work (formula, packaging, qualification), check whether the task already exists in a PD project before creating in Purchasing. If it does, multi-home it rather than duplicating.
- If the request is ambiguous (e.g., "what's going on with Vegelabs" — could be vendor lookup, PO status, performance, or compliance), default to a brief summary that names the relevant categories and let the operator pick.
