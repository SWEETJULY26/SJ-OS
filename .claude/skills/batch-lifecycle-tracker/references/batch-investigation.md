# Batch Lifecycle Task Template

Structure for the batch lifecycle Asana task content. The skill drafts; the Operator (and QA Lead at the gates) approves. Mirrors capa-investigation.md and lab-investigation.md so handoffs to capa-coordinator and quality-lab-coordinator carry forward without rework.

---

## Cover block

```
**Batch:** [batch_code]
**SKU:** [SKU code + name]
**Procedure version:** Batch Lifecycle Procedure v0.1 (2026-05-08)

**PLM batch record:**
- batch_code: [PLM batch_code + link]
- batch_quantity: [units]
- supplier_production_date: YYYY-MM-DD
- shelf_life_months: [N]
- sj_expiration_date: YYYY-MM-DD (computed)
- sj_pull_date: YYYY-MM-DD (computed = expiration - 3 months)

**Linked records:**
- Vendor: [name + purchasing-manager record link]
- Source PO: [PO number + link]
- Source receipt task: [inventory-manager Asana gid + title]
- PD project (transition source): [Asana project link, set at Job 1 only]

**Formula type:** Water-based emulsion | Anhydrous | Hybrid
**Stability schedule:** [generated from Lab Quality Procedure §5.1, listed below]
**Current state:** Active | Stability Pending | Hold/Release Review | On Hold | Watch | Released | Pulled | Expired
**Current Gate:** Open | Pending Operator | Pending QA Lead
```

---

## Transition record (pinned comment, Job 1 — first batch only)

```
**Transition to in-market stability — [SKU] — YYYY-MM-DD**

**Trigger:**
- inventory-manager batch creation: PLM batch_code [code], batch_quantity [N], supplier_production_date [date]
- asana-pd-manager Formula Development Tracker: [SKU] reached Signed Approvals on [date]

**Operator approval:** [role + name] | YYYY-MM-DD HH:MM

**PD-side closures:**
- [pre-launch stability task name] | [Asana gid] — closed with sync-back comment
- [pre-launch stability task name] | [Asana gid] — closed with sync-back comment

**In-market schedule generated:** see Stability Schedule section below.

**Notes:** [optional — anything specific about this SKU's launch context]
```

---

## Stability schedule block

Generated at task creation. Each row is a subtask that lives in `Batch — Stability Schedule`. Cadence per `references/batch-lifecycle-procedure.md` §5.1.

```
**Stability schedule — [batch_code]**

| # | Test | Due | Lab destination | Status | Result |
|---|---|---|---|---|---|
| S1 | PET-launch | YYYY-MM-DD | [Lab name] | Open / Dispatched / Returned / Pass / Fail | [value or link to result comment] |
| S2 | Accelerated-3mo | YYYY-MM-DD | [Lab name] | … | … |
| S3 | Real-time-annual | YYYY-MM-DD | [Lab name] | … | … |
| S4 | PET-EOL | YYYY-MM-DD (= sj_expiration_date - 90d) | [Lab name] | … | … |
```

For anhydrous, only the Real-time-annual row applies. For hybrid, the anhydrous row plus a Microbial-spot-check row at launch.

---

## Hold record (Job 4 — drafted on hold trigger, approved by QA Lead)

```
**Hold record — [batch_code] — YYYY-MM-DD**

**Hold Reason:** Lab fail | Complaint trend | Vendor signal | Regulatory observation | Internal flag | Other
**Source:** [originating skill or task — quality-lab-coordinator LF-YYYY-NNN, complaint-and-event-handler complaint task gid, etc.]
**Severity:** Critical | Major | Minor

**Containment scope:**
- Whole batch | Specific distribution lane | Specific retailer | Specific channel
- Carve-outs (if any): [explicit list — e.g., "DTC stops, Ulta DC continues until 2026-06-15"]

**Affected position (read at hold time):**
- On-hand by location: [from plm-assistant — DC1, DC2, OC3PL, etc.]
- In-transit: [units, lanes]
- Allocated to retailer POs: [retailer + units]

**Statement of issue:** [1-2 sentences — what triggered the hold]

**Containment actions:**
- [action 1 — e.g., "Pull retailer ASN to OC3PL"]
- [action 2 — e.g., "Notify oc3pl-order-manager to stop fulfilling this batch"]

**QA Lead approval:** [role + name] | YYYY-MM-DD HH:MM
```

On approval: Status = On Hold, task moves to `Batch — On Hold`, Gate = Open, containment actions execute.

---

## Release record (Job 4 — drafted on release trigger, approved by QA Lead)

```
**Release record — [batch_code] — YYYY-MM-DD**

**Release rationale:** [2-3 sentences tying release to evidence — what's resolved and why this batch is safe to return to distribution]

**Resolution path:** CAPA closed Effective | Clean retest | Pattern broken | Other
**Evidence:**
- [CAPA closeout link — CAPA-YYYY-NNN]
- [Retest result — link to LF or test report]
- [Pattern resolution — comment thread on complaint-and-event-handler task]

**Original Hold reference:** [Hold record date + the QA Lead approver who held it]

**Downstream notifications staged:**
- [Retailer comms — recipient list, drafted message link]
- [inventory-manager update — task gid, comment posted]
- [Internal stakeholders — list]

**QA Lead approval:** [role + name] | YYYY-MM-DD HH:MM
```

On approval: Status = Released, task moves to `Batch — Active in Market` (or `Batch — Closed` if at natural EOL), Gate = Open, downstream notifications fire.

---

## Near-expiry decision block (Job 5 — drafted on cross-post from inventory-manager)

```
**Near-expiry quality call — [batch_code] — YYYY-MM-DD**

**Threshold:** 90d | 60d | 30d
**Cross-post source:** inventory-manager Asana task [gid + link]
**Days to expiration:** [N]
**On-hand at threshold:** [units by location]

**Quality call:** Continue to release | Schedule late-life test | Pull plan | Expedite EOL
**Rationale:** [tied to procedure §7.2 decision tree]

**Actions staged:**
- [If pull plan: pull recommendation by location and target retailer]
- [If late-life test: stability subtask added with date]
- [If expedite EOL: PET-EOL date pulled forward]

**Operator approval (30d only):** [role + name] | YYYY-MM-DD HH:MM
```

On approval: outcome posts back to inventory-manager's task as a comment so they have the quality decision before any write-off action.

---

## CAPA handoff block (Job 6 — drafted on CAPA-route hold decision or operator-direct)

Mirrors NCR Procedure §3.2 intake fields so capa-coordinator picks up cleanly.

```
**Handoff to:** capa-coordinator → SJS CAPA Log Inbound Staging
**NCR intake context:**
- Source: batch-pattern | batch-fail (single-batch)
- Category: Product | Process | Vendor
- SKU: [code + name]
- Batch / lot code(s): [list — single or multi-batch pattern]
- Vendor: [name, if relevant]
- Description: [pulled from hold record's Statement of issue]
- Evidence: [batch task link, hold record link, lab finding links if any]
- Suspected severity: [matches batch hold severity]
- Containment action taken: [from hold record's Containment actions]

**Handoff Asana task created:** [SJS CAPA Log gid + link]
**Handoff status:** Staged / Picked up by capa-coordinator / NCR opened (NCR-YYYY-NNN) / CAPA opened (CAPA-YYYY-NNN)
```

Skill comments back on the batch task with the NCR / CAPA number once capa-coordinator opens.

---

## Watch list block (drafted when batch enters Watch state)

```
**Watch — [batch_code] — YYYY-MM-DD**

**Reason:** [single LF that didn't escalate | late-life pattern | marginal evidence | other]
**Window:** [N monthly cycles, default 2]
**Re-review trigger:** [date — first business day of [month + N]]
**Indicators monitored:**
- [indicator 1]
- [indicator 2]

**Operator approval:** [role + name] | YYYY-MM-DD HH:MM
```

On re-review: pivot to Active (clean), Hold/Release Review (signal escalates), or extend Watch with rationale.

---

## Closeout summary

```
**Batch [batch_code] — [SKU] closeout (YYYY-MM-DD):**
- **Lifecycle highlights:** [holds with dates, stability passes/fails, watch-list periods]
- **Terminal state:** Released | Pulled | Expired
- **Reason:** [for Pulled — pull rationale; for Released — natural EOL or post-hold release; for Expired — PLM auto]
- **Retention end:** [sj_expiration_date + 3 years]
- **Linked CAPAs:** [CAPA-YYYY-NNN list, if any]
```

Posted as the final comment + captured in the `Closeout Summary` custom field. Used by Job 7 close-the-loop comments on inventory-manager source records.

---

## What goes where

| Artifact | Where |
|---|---|
| Cover block | Task description |
| Transition record | Pinned comment (Job 1, first batch only) |
| Stability schedule block | Pinned comment, kept current as subtasks generate and complete |
| Hold record | Comment, posted at QA Lead approval |
| Release record | Comment, posted at QA Lead approval |
| Near-expiry decision block | Comment per threshold |
| CAPA handoff block | Comment when handoff stages |
| Watch list block | Comment when entering Watch + each re-review |
| Closeout summary | Final comment + `Closeout Summary` custom field |
| Stability test results | Subtask comments + attachments |
| Custom fields (Batch State, Stability Phase, Linked SKU, Hold Reason, Window End, Status, Gate, Severity, Linked Batch, Linked Vendor, Linked CAPA) | Asana fields per SKILL.md |
| Evidence (test reports, COAs, photos, retailer comms drafts) | Task or subtask attachments |
