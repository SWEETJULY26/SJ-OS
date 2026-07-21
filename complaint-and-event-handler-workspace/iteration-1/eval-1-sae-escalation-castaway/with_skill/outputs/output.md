# SAE Protocol Walk — Castaway Cream ER Complaint

**Mode: DRY RUN.** Nothing below was written to Asana. Every task, comment, field, and status change is staged for your approval only. No Asana write tool was called with commit intent — reads/writes below are simulated per the eval instruction.

---

## 0. Wiki context check

Simulated lookup: `wiki_lookup(p_slug => 'sku/castaway-cream')`.

No live Supabase connection was queried for this walkthrough (dry run) — treating this as a page-not-found / no-prior-context case. In a live run, the skill would pull `public.wiki_pages` for `sku/castaway-cream` first and prepend any complaint/AE history before proceeding. Flag: if a real Castaway Cream wiki page exists with prior reaction complaints or batch issues, re-run this before finalizing severity discussion at §5.3 — that history matters for the operator's call.

---

## 1. Intake read (Job 1)

This complaint didn't arrive through the normal path yet — no Asana task gid, no Invoice/Order Number, no batch code. Before anything else, this needs to become a real intake record.

**Missing required fields, per the intake gate:**
- Invoice/Order Number — not provided. Per skill rule, this blocks classification until we have it or a documented reason we can't get it (severity may justify proceeding in parallel — see below).
- Product Batch Code — not provided. Needed to pivot into PLM batch context and to check if other complaints share this lot.
- Customer name / contact info — needed for medical follow-up and any regulatory filing.
- Sales channel (Amazon / SJ Oakland / Web Store) — not provided.

**Staged, not committed:** a new task in the **SJ Skin Complaint Log** (gid `1204763097184846`), section `New feedback`, with:
- Complaint Type (proposed): **Skin Reactions & Irritations**
- Description: customer reports facial swelling after using Castaway Cream; sought ER treatment; prescribed steroids by attending physician.
- Draft back-to-customer ask: order number, batch/lot code (bottom of tube/jar), date of purchase and first use, and — with her consent — a copy of the ER visit summary or physician's note if she's willing to share it.

**HITL checkpoint 1:** Approve creating this intake task, and approve sending the info-request to the customer. Given the severity, I'd run the customer outreach and the SAE walk in parallel rather than waiting on her reply — flag that as a judgment call for you, not something the skill decides on its own.

---

## 2. SAE keyword recognition

Description matches SAE trigger language directly: **"ER" / "emergency room"**, **"swelling"**, **medical intervention (steroid prescription)**. This routes straight into Job 4 — SKN-OPS-002.

Per the classification reference, any **Skin Reactions & Irritations** complaint gets scanned against SAE keywords before first-response closes. This one trips it immediately, so first-response classification is paused and the SAE walk takes priority.

---

## 3. SKN-OPS-002 walk (verbatim, §5.1 → §5.8)

Source of record: SharePoint → `Sweet July/Product Development/Quality Control & Assurance/SOP/Serious Adverse Event (SAE) SOP SKN-OPS-002 Rev. 1.docx`. The mirror below is for this walk only — treat SharePoint as canonical if anything here looks off.

### §5.1 Identification and Reporting
Event identified: customer alleges ER visit, facial swelling, steroid prescription following Castaway Cream use. Per SOP, this gets reported immediately to QA/supervisor — that's this conversation.

**Staged draft — SAE Report Form (Appendix A):**

| Field | Value |
|---|---|
| Product | Castaway Cream |
| Batch/Lot Code | Unknown — pending customer response |
| Event date | Unknown — pending customer response |
| Report date | 2026-07-21 |
| Description | Facial swelling following product use; customer sought emergency room treatment; physician prescribed steroids |
| Patient demographics | Unknown — pending customer response, if she consents to share |
| Medical treatment required | Yes — ER visit, steroid prescription |
| Reporter | Alvin Belt (VP Ops) |
| Source | Customer complaint (channel unconfirmed) |

**HITL checkpoint 2:** Approve staging this form as-is (with the gaps flagged), or hold until customer info comes back. Recommend staging now — an SAE clock doesn't wait on paperwork.

### §5.2 Documentation
Once approved, the form draft above gets posted as a comment on the SAE-flagged Asana task, cross-linked to the source complaint task. `[SAE Open]` framing applied via the `Status` field (see below), not a title prefix.

**Staged write (not committed):** `Status = SAE Open` on the complaint task.

### §5.3 Initial Assessment — **your call**

This is the step the SOP puts in your hands. It doesn't define a formal severity matrix, and the skill isn't going to invent one — that's a documented content gap (see bottom of this doc). Here's what's on the table for you to decide:

1. **Severity call.** ER visit plus a steroid prescription is a documented medical intervention — that alone typically clears the SOP's definition of "significant health event requiring medical intervention" (§3). Your call on whether this is SAE-confirmed (not just AE) — I'd lean yes given ER + Rx, but that's yours to make, not mine.
2. **Immediate risk mitigation.** Options to consider: pull remaining stock of the same batch from sale pending batch ID (once you have it), post an internal hold flag, or wait for batch confirmation before acting. Nothing here is triggered automatically.
3. **Urgency of customer contact.** Whether Ops or someone in a clinical/legal-aware role reaches out to the customer directly, and what's said.

None of these are decided yet. I need your answer on at least #1 before the walk continues past this point in a way that matters (recall consideration, regulatory flag, etc. all downstream of this).

### §5.4 Investigation
Pending your §5.3 call, the next step is standing up an investigation team — SOP specifies Product Safety Officer plus relevant personnel.

**Staged ask (not committed):** investigation team roster draft — Product Safety Officer (name TBD — who holds this role currently?), QA lead, and whoever owns the Castaway Cream formula file in PD. Root cause tools per Appendix C (Fishbone / 5 Whys) get run once batch code and any other same-lot signal are in hand.

**HITL checkpoint 3:** Confirm who sits on this team before I stage the ask as a real Asana comment.

### §5.5 Corrective and Preventive Action Plan
Not staged yet — sequenced behind root cause. Once investigation lands on a root cause hypothesis, the skill drafts a CAPA brief (root cause hypothesis, batches affected, SKU, trigger event, recommended scope) and hands it to **capa-coordinator**, live in this environment — direct handoff via SJS CAPA Log Inbound Staging, not the old title-prefix queue.

### §5.6 Communication and Reporting
Two tracks:

- **Internal:** staged stakeholder summary (QA, PD, you) once §5.3 is settled.
- **External/regulatory:** this is the one that matters most here. An ER visit plus a prescribed medical treatment following product use is squarely the kind of event MoCRA serious-adverse-event reporting exists for. The skill does not decide reportability — that's regulatory-manager's call, fed by **adverse-event-and-recall-reporter** for the actual MoCRA filing and clock tracking (SKN-OPS-009).

**Staged (not committed):** `[Reg Flag Pending — regulatory-manager]` task in SJS Quality Management, containing: event summary, product, suspected reportability basis (ER + prescribed steroid treatment), batch (pending), severity (pending your §5.3 call).

**HITL checkpoint 4:** Approve posting the reg flag now rather than waiting on batch code. Given MoCRA's reporting clock, I'd push this now — recommend not waiting on the customer's callback to start the regulatory conversation.

### §5.7 Verification and Effectiveness
Not applicable yet — this runs after corrective action is implemented. Noting it here only so you can see the full arc: once closed, a follow-up task gets scheduled on the SAE close date for the effectiveness review.

### §5.8 Documentation and Records
Every artifact from this walk — SAE Report Form, investigation notes, CAPA brief, reg flag — attaches to the source Asana task as the index, with any batch-specific record pointing to PLM via plm-assistant. Nothing here writes to PLM directly.

---

## 4. What's actually blocking progress right now

In order of urgency:

1. **Your §5.3 severity call** — SAE confirmed or not. Everything downstream (recall consideration, regulatory posture, CAPA scope) reads off this.
2. **Order number and batch code from the customer** — without it we can't confirm channel, pull other complaints on the same lot, or scope a recall if it comes to that.
3. **Who's on the investigation team** — specifically who's currently the Product Safety Officer.
4. **Whether to fire the regulatory flag now or hold for batch confirmation** — leaning toward now, your call.

## 5. What this explicitly does NOT do on its own

- Does not classify this as SAE-confirmed vs. AE — that's your Initial Assessment call, not a skill decision.
- Does not open a recall. Nothing here suggests one is warranted yet (single report, no batch pattern established), but if you want to raise it, the explicit kickoff phrase is required — "trigger a recall on [SKU/batch]" — plus step-by-step approval per SKN-OPS-003. Nothing in this walk fires that on its own.
- Does not file anything with FDA/MoCRA. That's adverse-event-and-recall-reporter's job, gated behind regulatory-manager confirming reportability.
- Does not write anything to Asana. Every task, comment, and field change above is staged, pending your approvals at the four HITL checkpoints marked.

---

## Content gap flagged (per skill design)

SKN-OPS-002 §5.3 has no formal severity triage tree — this has been true since the SOP was ratified. The skill surfaces the call rather than inventing scoring logic. If you want a triage tree added (e.g., ER visit + prescription = automatic SAE-confirmed threshold), that's a CAPA-worthy SOP improvement, not something to patch in ad hoc — routes to the SOP owner (you / Shirlene Loi) for a Rev. 2.
