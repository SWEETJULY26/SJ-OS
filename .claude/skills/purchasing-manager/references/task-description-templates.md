# Task Description Templates

The AC Brands Purchasing project carries three custom fields — **Status**, **Vendor**, **PLM Link** — plus standard Asana fields (assignee, due date, completion). Everything else lives in the task description. The skill writes the description; Operations reads it.

Title format is `Job — Identifier` (e.g., `PO 24178 — KDC-One`, `Onboarding — Element Packaging`). No bracketed prefixes — section placement plus the Status field carry that signal.

Each template below is the canonical format for that task type. Keep descriptions scannable. Use Asana's supported markdown (bold, lists, links). Skip restating Vendor and PLM Link in the description body when they're already in the custom fields — link out from there instead.

---

## Onboarding — Vendor Name (section: Vendor Onboarding)

Used at Step 2B. Assignee is auto-set per the `vendor_type` first-contact routing rule (see SKILL.md Job 2). The doc checklist below renders inline in the description; on **Proceed** the skill auto-creates the six items as Asana subtasks and mirrors their state to `vendors.onboarding_checklist` jsonb.

```
**Vendor:** {{vendor_name}}
**Vendor type:** {{vendor_type}}
**Source of intro:** {{email_link or referral_source or "Direct outreach"}}
**Proposed contact:** {{contact_name}}
**First-contact owner:** {{role per vendor_type routing rule}}
**Brand:** {{SJS or AC Brands}}
**Notes:** {{free text from intro thread}}

**Onboarding doc checklist:**
- [ ] NDA
- [ ] W9
- [ ] COI
- [ ] MSA
- [ ] Banking / ACH
- [ ] MSDS (only if vendor_type in {filler, ingredient})

**Gate:** NDA + W9 complete → ready for PLM vendor record creation. Task auto-moves to Compliance, Renewals & Disputes; remaining open docs stay for follow-up.
```

HITL Proceed gate: operator comments **Proceed** (advance to 2C, auto-create subtasks) or **Pass** (close the task).

---

## PO Number — Vendor (section: HITL — Needs Operations Review, Status: Draft)

```
**PO #:** {{po_number}}
**Vendor:** {{vendor_name}} (PLM ID: {{vendor_id}})
**Brand:** {{SJS or AC Brands}}
**Total:** ${{total_amount}}
**Issue date (proposed):** {{date}}
**Expected receipt:** {{date}}
**Payment terms:** {{net_30 etc}}
**Linked PD task:** {{task_link if applicable}}

**Line items:**
| Component / SKU | Qty | Unit price | Subtotal |
|-----------------|-----|------------|----------|
| {{item}}        | {{qty}} | ${{unit}} | ${{subtotal}} |

**PLM PO draft:** {{link to PLM PO record}}

**Source trigger:** {{approved reorder review / NPI ramp / manual ask}}

**On approval, the skill will:**
- Mark PLM PO as Sent
- Set Status field to **Sent**, move task to **POs In Flight**
- (Manual step) Operations emails the PDF to the vendor
```

---

## PO walking the lifecycle (Status: Sent / Acknowledged / In Transit / Received)

These are Status field changes plus section moves on the same task as it walks through the lifecycle. The task title (`PO Number — Vendor`) stays put. The description carries forward and gets appended with status events.

```
**PO #:** {{po_number}}
**Vendor:** {{vendor_name}}
**PLM PO record:** {{link}}

**Status history:**
- {{date}} — Drafted
- {{date}} — Sent (PDF sent to {{contact}})
- {{date}} — Acknowledged (clean / variance flagged)
- {{date}} — In transit (ETA {{date}})
- {{date}} — Received, batch {{batch_id}} created in PLM
- {{date}} — Invoice received, 3-way match pending
- {{date}} — Closed

**Current status:** {{current state}}

**Linked PD task:** {{task_link if applicable}}
```

---

## PO Number — Vendor (section: HITL — Needs Operations Review, Status: Variance)

```
**PO #:** {{po_number}}
**Vendor:** {{vendor_name}}
**PLM PO record:** {{link}}
**Variance type:** {{Ack / Receipt / Invoice}}

**Discrepancy:**
| Field | Original | Vendor sent | Delta |
|-------|----------|-------------|-------|
| {{field}} | {{orig}} | {{sent}} | {{delta}} |

**Source doc:** {{link to email / PDF}}

**Recommendation:**
{{accept variance / push back to vendor / open dispute}}

**On approval, the skill will:**
- {{accept: update PLM PO with new values, set Status back to the appropriate lifecycle state (Acknowledged after ack-variance, Received after receipt-variance, Closed after invoice-variance) / push back: draft reply email for Operations / dispute: open new Dispute — PO Number — Vendor task in Compliance, Renewals & Disputes}}
```

---

## Receipt — Vendor Name — PO Number (section: Receiving)

Used at Job 3e, **Scenario B (standalone)** — a PO with no linked PD project. Scenario A (PD-linked) reuses the existing PD task description and only amends the **PLM Link** field to point at the PO record; no new task and no new description. OC3PL (Logiwa WMS) notifies on receipt; the operator fills the Logiwa Receipt Order ref and actual counts, then marks Status = **Received**. Any discrepancy at receipt opens a Job 10 discrepancy task — set **Discrepancies** to the details and cross-link.

```
**Vendor:** {{vendor_name}}
**PO Number:** {{po_number}}
**PLM Link:** {{plm_po_url}}
**Logiwa Receipt Order ref:** {{logiwa_ref or "Pending"}}
**Anticipated receipt date:** {{date}}
**Actual receipt date:** {{date or "Pending"}}
**Unit count expected:** {{qty}}
**Unit count received:** {{qty or "Pending"}}
**Discrepancies:** {{none / details — if any, open a Job 10 discrepancy task and link it here}}
```

---

## Reorder Review — SKU/Component (section: HITL — Needs Operations Review)

```
**Item:** {{sku_or_component}}
**Brand:** {{SJS or AC Brands}}
**Vendor (current):** {{vendor_name}} — PLM ID {{vendor_id}}

**Inventory snapshot:**
- On hand: {{qty}}
- Safety stock: {{qty}}
- Reorder point: {{qty}}
- Last unit cost: ${{cost}}

**Suggested order:**
- Qty: {{qty}} (driven by MOQ {{moq}} and demand {{demand_qty}})
- Lead time: {{days}} days
- Estimated total: ${{total}}
- Estimated receipt: {{date}}

**Alternative vendors:** {{list if applicable, with pricing}}

**On approval, the skill will:**
- Open new `PO Number — Vendor` task in **HITL — Needs Operations Review** with Status = **Draft**
- Draft PO in PLM with line items
- Stage for Operations PO issuance review
```

---

## Compliance Gap — Vendor Name (section: Compliance, Renewals & Disputes)

```
**Vendor:** {{vendor_name}} — PLM ID {{vendor_id}}
**Brand:** {{SJS or AC Brands}}

**Missing or expiring docs:**
| Doc | Status | Expires / missing since |
|-----|--------|-------------------------|
| {{doc}} | {{expiring / missing}} | {{date}} |

**Risk:** {{regulatory / financial / operational}}

**Recommended action:**
{{request from vendor / pull from internal records / escalate}}

**Suggested email draft:** {{link or inline}}
```

---

## Renewal — Vendor Name — 60d / 30d / 15d (section: Compliance, Renewals & Disputes)

Title format `Renewal — {{vendor_name}} — {{60d / 30d / 15d}}`. Opened by the weekly Monday `purchasing-renewal-sweep` (Job 8) when `contract_renewal_date` falls inside a 60/30/15-day window (±1 day), or on operator request. Assignee is Operations; due date is the actual `contract_renewal_date`. The sweep reads `supplier/<vendor_slug>` from the wiki before drafting and prepends prior terms + recent performance signal; the PLM performance summary fills in on demand.

```
**Vendor:** {{vendor_name}} — PLM ID {{vendor_id}}
**Vendor type:** {{vendor_type}}
**Renewal date:** {{contract_renewal_date}}
**Days out:** {{60 / 30 / 15}}
**Contract type:** {{MSA / SOW / supply agreement}}

**Last contract terms (from wiki):** {{prior_terms or "Not in wiki yet"}}
**Recent performance signal (from wiki):** {{recent_signal or "None synthesized"}}

**Performance summary (from PLM, on demand):**
- POs in last 12 months: {{count}}
- On-time delivery: {{%}}
- Defect / reject rate: {{%}}
- Price drift: {{%}}

**Action needed:** {{renew / renegotiate {{specific terms}} / churn}}

**Linked contract doc:** {{link in PLM}}
```

---

## Dispute — PO Number — Vendor (section: Compliance, Renewals & Disputes, Status: Dispute)

```
**PO #:** {{po_number}}
**Vendor:** {{vendor_name}}
**PLM PO record:** {{link}}
**Dispute type:** {{quality / quantity / pricing / lead time / other}}

**What happened:**
{{narrative}}

**Linked invoice:** {{link}}
**Amount in dispute:** ${{amount}}

**Vendor position:** {{summary from email thread}}
**Our position:** {{summary}}

**Recommended path:**
{{negotiate credit / replace product / reject and refund / escalate to legal}}

**Email thread:** {{link}}
```

---

## Discrepancy — Vendor Name — PO Number (section: Compliance, Renewals & Disputes)

Used at Job 10. Opened when a count variance, damage, or missing-items issue is flagged at receipt (by logistics-manager, OC3PL, or the operator). **Discrepancy Type** and **Resolution** are inline structured fields here, not Asana custom fields. If the PO is multi-homed to a PD project, this task joins the same homes. On Resolution = **Escalate to CAPA**, notify `capa-coordinator` with this task's GID; on close (any Resolution) the vendor scorecard event is written via `asana-plm-bridge`.

```
**Vendor:** {{vendor_name}}
**PO Number:** {{po_number}}
**PLM Link:** {{plm_po_url}}
**Logiwa Receipt Order ref:** {{logiwa_ref}}
**Discrepancy Type:** [ ] Count Variance  [ ] Damage  [ ] Missing Items  [ ] Other
**Date observed:** {{date}}
**Observed by:** {{OC3PL / logistics-manager / operator name}}

**Investigation notes:** {{free text, updated in comments and synced here on resolve}}

**Resolution:** [ ] Vendor Credit  [ ] Replacement Shipment  [ ] Accepted As-Is  [ ] Escalate to CAPA
**Resolution date:** {{date}}
**Resolution notes:** {{credit amount, replacement PO, CAPA task GID, etc.}}
```

---

## RFQ — Component / Project (section: Sourcing & RFQ)

```
**Sourcing for:** {{component_or_capability}}
**Driver:** {{new SKU / cost-down / supply risk / quality issue}}
**Linked PD task:** {{task_link if applicable}}
**Target:** {{spec, MOQ, lead time, price target}}

**Suppliers in evaluation:**
| Supplier | RFQ sent | Bid | Samples | Qualification | Notes |
|----------|----------|-----|---------|---------------|-------|
| {{name}} | {{date}} | ${{bid}} | {{received}} | {{status}} | {{notes}} |

**Decision criteria:** {{price / lead time / quality / capacity / fit}}

**Recommendation:** {{when ready, hand off to PD Manager for qualification, then back to Purchasing for first PO}}
```

---

## Vendor record discrepancy (section: HITL — Needs Operations Review)

When the weekly alignment sweep finds a vendor record that's drifted across PLM / Asana / Outlook, open a single task per vendor.

```
**Vendor:** {{vendor_name}} — PLM ID {{vendor_id}}

**Drift detected:**
| Field | PLM (truth) | Asana | Outlook |
|-------|-------------|-------|---------|
| {{field}} | {{plm_val}} | {{asana_val}} | {{outlook_val}} |

**Recommended fix:** {{update Asana / update Outlook / verify with vendor}}

**On approval, the skill will:**
- Update {{system}} to match PLM (or update PLM if Operations says PLM is wrong)
- Close this task with a sync-back comment
```
