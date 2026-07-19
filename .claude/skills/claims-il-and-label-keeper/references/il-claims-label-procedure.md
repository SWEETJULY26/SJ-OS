# IL / Claims / Label Procedure — SKN-OPS-008 Rev.2

**SOP Number:** SKN-OPS-008
**Title:** IL / Claims / Label Procedure
**Effective Date:** May 12, 2026 (Rev.2)
**Revision Number:** 2.0
**Prepared by:** Alvin Belt (claims-il-and-label-keeper skill-side); Reg Lead (procedural-side); Pedrero Regulatory consult on substantive content (2026-05-12 touchbase prompted Rev.2 additions).
**Approved by:** Alvin Belt
**Status:** Rev.2 ratified 2026-05-12 in-place during the post-Pedrero update session — same pattern as Rev.1. Rev.1 (effective 2026-05-09) superseded. SharePoint master copy filed at `Sweet July/PD/Quality Control & Assurance/SOP/IL Claims Label Procedure SKN-OPS-008 Rev.2.docx`.

**Owner:** claims-il-and-label-keeper (skill-side); Reg Lead (procedural-side, currently Alvin Belt at v6.6)
**Anchors:** SKN-OPS-001 Rev.1 §5.6 (retention), system-c-regulatory-scope.md (system architecture), `regulatory-manager/references/state-packaging-laws.md` (CA SB 343, 19-state toxics, EPR), `regulatory-manager/references/canada-compliance.md` (Health Canada notification, extended allergens, Quebec French-language)

## Revision history

| Revision | Date | Author | Summary |
|---|---|---|---|
| 1.0 | 2026-05-09 | Alvin Belt | Initial issue. Authored during v6.1 build of claims-il-and-label-keeper; ratified in-place same session. Same in-place pattern as SKN-OPS-006 (Lab) and SKN-OPS-007 (Batch Lifecycle). |
| 2.0 | 2026-05-12 | Alvin Belt | Post-Pedrero touchbase update. §3.2 adds 19-state packaging-toxics certificate of compliance as required IL packet element. §6 adds three new passes to label cross-check: Pantone per CA SB 343, Canada extended-allergens, Quebec French-language. §7 adds §7.4 reformulation claim-bridge gate (Eye Cream, Toner, Power Oil flagged as initial scope). Ratified in-place at build review. |

---

## Why this exists

Sweet July Skin's regulatory artifacts — ingredient lists, sustained claim substantiation, label artwork versions, retailer attestation responses — currently scatter across Slack, Outlook attachments, Founder folders, and individual heads. Pedrero Regulatory does the substantive review work, but without a documented procedure:

- IL versions drift. The IL Pedrero approved on a formula doesn't always match what the printer prints.
- Sustained claim substantiation isn't audit-ready. When Sephora asks for evidence on "clinically tested" or "dermatologist-approved," the supporting evidence is hard to find on demand.
- New claims slip onto packaging. A new claim added by marketing or founder skips Pedrero sign-off because there's no gate.
- Retailer attestations get missed or renewed without fresh review. A SKU drops off Sephora Clean because the renewal window passed unnoticed.

This procedure closes those gaps so every regulatory artifact is staged through Pedrero, archived with a version stamp, and renewed on cadence.

---

## 1. Scope

Applies to any pre-launch or post-launch regulatory artifact for a Sweet July Skin SKU:

- Ingredient list (IL) for any approved formula, including reformulations
- Sustained claim substantiation evidence (per claim per SKU, audit-ready)
- New claims added to packaging or marketing copy after launch
- Component and carton label artwork archive (with IL match cross-check)
- Retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo)

Does not apply to:
- Pre-launch claim evidence generation (clinical, in-vitro, ingredient data) — asana-pd-manager keeps
- MoCRA registrations, state filings (CA Prop 65, NY/WA/OR), retailer attestation cadence dashboard — regulatory-manager (v6.3)
- SAE filing prep, FDA recall agency reporting — adverse-event-and-recall-reporter (v6.2)
- International regulatory work — parked
- Print-side QA, color management, dieline approval — Operations and the printer
- Vendor compliance docs at intake (COA, COC, COI, MSDS) — purchasing-manager

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee, designer, or external partner that surfaces an artifact for review. PD designer for label artwork; Marketing or Founder for new claims; Retailer for attestation requests. |
| **Operator** | Reviews intake, classifies the artifact, drafts packet contents, approves the path forward. Currently Alvin Belt. |
| **Reg Lead** | Internal sign-off on every Pedrero send and every retailer-facing submission. Currently Alvin Belt at v6.1 (same person as Operator; gate fires as a separate confirmation step for audit trail). v6.3 may split if a dedicated internal reg lead joins. |
| **External Reg Partner** | All substantive regulatory review. No internal authority. Pedrero Regulatory: Amy Pedrero principal, Heather Folkes and Teona Bebia secondary. |
| **QA Lead** | Consult-only on quality-side overlaps (e.g., a label cross-check that surfaces a batch-affecting issue). Currently Perrine (technical QA/QC lead). |
| **Voice of Customer** | Consult-only on retailer attestation responses where customer-perceived attributes matter. Currently Nicole Iturbe. |

Names live in the runtime role map, not in this procedure.

---

## 3. IL Review Gate

### 3.1 What triggers an IL review

An IL review fires when any of these is true:

- A formula in the asana-pd-manager Formula Tracker reaches `Stage = Signed Approvals`. The asana-pd-manager hook flips `IL Status = Pending IL Review` and creates an inbound task.
- A formula reformulation event flips `IL Status = IL Reformulated — Re-review Required` on the existing Formula Tracker task.
- The Operator or Reg Lead requests one explicitly (e.g., portfolio-level IL review on a SKU about to enter a new retailer).

### 3.2 IL packet contents

Every IL packet sent to Pedrero must include:

| Element | Notes |
|---|---|
| SKU code + name | Pulled from PLM via plm-assistant |
| Formula version stamp | From Formula Tracker |
| Full INCI list | INCI names in regulatory order, exact spelling per existing supplier-provided INCI |
| Allergen breakdown | EU 26-allergen list; flag any that are present at >0.001% leave-on or >0.01% rinse-off (informational; Pedrero confirms applicability) |
| Canada extended-allergens disclosure (Rev.2) | Required when the SKU is in scope for Canadian distribution. Map ingredients to Health Canada's extended-allergens schedule per `regulatory-manager/references/canada-compliance.md`. |
| Supporting docs | Latest formula composition sheet, supplier IL attestations for any blended raw materials |
| 19-state packaging-toxics certificate of compliance (Rev.2) | Required for retailer-distributed SKUs (Target, Walmart, large retailers). One certificate per active component supplier (Elements ACT, HCT, Impress, CDW, others) certifying heavy metals ≤100 ppm collectively. Heather Folkes at Pedrero supplies the request verbiage SJS uses on first run; reputable suppliers turn certificates around quickly. Missing cert pauses IL approval until cert lands. DTC-only SKUs may proceed without the cert with Operator sign-off. |
| Prior IL version | If reformulation, the prior approved IL plus a written diff of changes |
| Reformulation QIL note (Rev.2) | If reformulation, note whether prior-formula QIL has been recovered. If not recovered, surface §7.4 reformulation claim-bridge gate ahead of any clinical-claim ride-through. |
| IL version stamp | New stamp assigned by this skill: `IL-[SKU-CODE]-v[N]`, incremented from prior version |
| Specific reg question | Plain-language ask: "please review the IL for [SKU] — [first IL | reformulation | annual re-review]. Confirm INCI accuracy, allergen disclosures, and any flags vs prior approved IL." |

### 3.3 IL packet HITL

- Operator approves the packet contents at intake (Job 1 of SKILL.md). Operator gate.
- Reg Lead approves the Pedrero send (Job 2). Reg Lead gate. The send draft is composed locally; Operator hits send manually after Reg Lead approval.

---

## 4. Pedrero Send Mechanics

### 4.1 Subject line conventions

All Pedrero correspondence follows a subject prefix so outlook-asana-bridge can auto-route replies:

| Artifact | Subject prefix |
|---|---|
| IL review | `[IL Review — SKU-CODE]` (e.g., `[IL Review — CST-CRM]`) |
| New claim sign-off | `[New Claim Sign-Off — SKU-CODE]` |
| Retailer attestation | `[Attestation Review — RETAILER — SKU-CODE]` (e.g., `[Attestation Review — Sephora — CST-CRM]`) |
| Label cross-check | `[Label Cross-Check — SKU-CODE]` |
| Re-review (annual or reformulation) | Same as above with `— Re-review` suffix |

### 4.2 Contacts

| Field | Recipient |
|---|---|
| To | Amy Pedrero (amy@pedreroregulatory.com) |
| Cc | Heather Folkes (heather@pedreroregulatory.com), Teona Bebia (teona@pedreroregulatory.com) |
| Cc (internal) | Operator (Alvin Belt) for record |

### 4.3 Return windows

Default: 10 business days. Operator can tighten with explicit `URGENT — by [date]` in subject when a retailer deadline is binding. The skill sets `Window End` on the Asana task to the expected return date and surfaces overdue tasks in the daily status sweep.

### 4.4 Send commit

The skill never sends Outlook autonomously. The send draft is composed and staged; Operator hits send manually after Reg Lead approval. The Asana task moves to **In Pedrero Review** on Operator-confirmed send, with the outbound timestamp captured.

---

## 5. Pedrero Return Processing

### 5.1 Return classifications

When a Pedrero reply arrives, classify per:

| Classification | Action |
|---|---|
| **Approved** | Move artifact to **Active / In-Effect**. Write to archive. For IL: sync-back to Formula Tracker with `IL Status = IL Approved`; PD can finalize component and carton artwork. For new claim: add to claim sub file. For attestation: ready for Operator submission to retailer (§8). For label: archive entry written. |
| **Returned for revision** | Move to **Returned — Action Required**. Capture Pedrero's rationale. For IL: sync-back to Formula Tracker with `IL Status = IL Returned for Reformulation` plus rationale; Operator decides next PD step. For other artifacts: route to Operator for response. |
| **Question / clarifying request** | Stage a clarifying reply to Pedrero. Reg Lead approves the reply send (§4.4). Asana task stays in **In Pedrero Review** with a comment capturing Pedrero's question and the staged reply. |

### 5.2 HITL on return

- Operator approves the classification. Operator gate.
- Reg Lead approves any sync-back to PD (the IL Status flip is a write that affects downstream PD work) or any clarifying reply send.

### 5.3 No verbal-only approvals

Verbal Pedrero approvals from a call don't satisfy the procedure. If Pedrero says "yes" on a call, stage a written confirmation send with subject `[CONFIRMING — IL Review — SKU-CODE — verbal OK on call]` and ask for written confirmation. Archive only after written reply.

---

## 6. Label Artwork Cross-Check and Archive

### 6.1 Cross-check trigger

Fires when:
- A PD designer sends label artwork via outlook-asana-bridge
- The Operator requests an explicit cross-check ("did Pedrero sign off on the new label")
- A new label artwork file is dropped into the SharePoint regulatory folder (post-v6.3)

### 6.2 Cross-check rules — four passes (Rev.2)

For each artwork piece (component, carton, secondary packaging if in scope per §6.4), the skill runs four passes in sequence. Any fail in any pass pauses archive until resolved.

#### Pass 1 — IL match

The skill pulls the latest approved IL version for the SKU and compares to the IL printed on the artwork.

| Outcome | Action |
|---|---|
| **Match** | Pass; advance to Pass 2. |
| **Drift — older approved version** | Pause. Flag to Operator with the diff. Either: re-confirm the older version is still the right one (rare; usually means a SKU is using an older formulation), or update the artwork to current IL. Route through §6.3 if a new Pedrero send is needed. |
| **Drift — IL not approved** | Pause. Route to §3 IL review gate before archive. |
| **New claim on artwork not yet sub'd** | Pause. Route to §7 new-claim sign-off before archive. |
| **Already-printed-with-wrong-IL discovery** | Archive captures truth, but stage a separate task: a Pedrero send describing the print error and proposed remediation (label correction sticker, recall depending on severity), and an issue task in **Returned — Action Required**. The archive entry references the issue task. |

#### Pass 2 — Pantone per CA SB 343 (Rev.2)

For each component or carton displaying the recycling chasing-arrows symbol:

| Outcome | Action |
|---|---|
| **Pass** — Pantone within approved gradient | Symbol may stay. Advance to Pass 3. |
| **Lighten** | Pantone falls outside gradient but adjustment is feasible. Flag to Operator; PD designer adjusts Pantone; re-run Pass 2 on revised artwork. |
| **Remove symbol** | Pantone stays dark per brand. Recycling symbol comes off the artwork. PD designer revises; re-run Pass 1 and Pass 2 on revised artwork. |
| **Unclear** | Borderline Pantone. Stage to Pedrero (Job 2) with `[Pantone Review — SKU-CODE]` subject; Heather Folkes confirms gradient applicability. |

Approved gradient and the per-Pantone pass/fail rule live in `regulatory-manager/references/state-packaging-laws.md` (Heather Folkes at Pedrero supplied; updated when SB 343 revises).

#### Pass 3 — Canada extended-allergens (Rev.2)

Fires only when the SKU is in scope for Canadian distribution (set at IL gate intake or on the SKU profile).

| Outcome | Action |
|---|---|
| **Pass** — disclosure present and correct | Advance to Pass 4. |
| **Missing** | Pause. Route to PD designer for revision per Pedrero's extended-allergens schedule. Hard deadline 2026-07-31 per Sephora Canada cutoff; any Canada-bound SKU without this pass cannot ship to Canada after the deadline. |
| **Unclear** | Stage to Pedrero with `[Canada Notification — SKU-CODE]` subject; Pedrero confirms which SJS ingredients map to which extended allergens. |

#### Pass 4 — Quebec French-language (Rev.2)

Fires only when the SKU is in scope for Quebec distribution.

| Outcome | Action |
|---|---|
| **Pass** — every inscription bilingual | Archive the version. Move to **Active / In-Effect**. Task title `Label Archive — [SKU] — [COMPONENT or CARTON] — v[N]`. |
| **Partial** — mandatory statements bilingual but other inscriptions English-only | Flag to Operator. Route to Perrine for translation pass on missing inscriptions; PD designer integrates and re-runs Pass 4. |
| **Fail** — English-only | Route back to PD designer for bilingual rework. |
| **Unclear** | Stage to Pedrero or Ecomundo with `[Quebec Label Review — SKU-CODE]` subject; confirm which inscriptions qualify as bilingual-required. |

Pass 4 outcome of **Pass** is the only path that archives.

### 6.3 When does an artwork need a new Pedrero send

Not every archive entry needs a Pedrero send. Send to Pedrero only when:
- The artwork's IL doesn't match an already-approved IL version (drift requires Pedrero call)
- The artwork carries a claim that hasn't been sub'd or signed off
- A retailer-specific artwork variant (e.g., Sephora-exclusive packaging) triggers attestation-tied review

A simple match against an already-approved IL with no new claims is an Operator + Reg Lead approval for the archive entry, no Pedrero send required.

### 6.4 Scope of components archived

At v6.1, archive scope: primary cartons, primary component (bottle, jar, tube), and any printed insert. Out of scope: shipping packaging, hangtags, marketing collateral that ships separately. Operator can extend scope per SKU at the build of the SKU's first archive entry; document the per-SKU scope on the Claim Sub task for that SKU.

---

## 7. New-Claim Sign-Off

### 7.1 What counts as a new claim

Any claim added to packaging, marketing copy, retailer-facing copy (e.g., Sephora product detail page), or e-commerce product page that wasn't on the SKU at launch or at the last Pedrero attestation cycle. Includes claim text changes (e.g., "clinically tested" → "dermatologist tested").

Out of scope: ingredient name corrections (handle via §3 IL re-review), copyediting that doesn't change claim substance.

### 7.2 Three paths

For every new claim, walk:

| Path | Trigger | Action |
|---|---|---|
| **Covered by existing evidence** | The claim is already supported by evidence in the SKU's claim sub file. | Stage to Pedrero with the citation: "Confirming this new claim text is supported by [evidence reference]; please sign off." |
| **Needs new evidence** | The claim isn't sub'd; new evidence (clinical, in-vitro, ingredient data) is required. | Pause. Route the evidence-generation ask to PD via asana-pd-manager. Hold the claim review until evidence lands. Then proceed via the "Covered by existing evidence" path with the new evidence. |
| **Not defensible** | The claim cannot be supported (e.g., a structure-function claim with no ingredient justification, or a claim that crosses into drug territory). | Flag to Operator with rationale. Recommend reword or drop. Do not stage to Pedrero — Pedrero is reviewing defensible claims, not authoring rewrites. |

### 7.3 Claim sub file structure

One Claim Sub task per SKU, titled `Claim Sub — [SKU]`. Subtasks per claim, each holding:

- Exact claim text (verbatim from packaging or marketing)
- Evidence reference (clinical study report, in-vitro test, peer-reviewed citation, formal Pedrero opinion letter)
- Pedrero approval reference (subject line + date of approval reply)
- Effective date (when claim went on packaging or copy)
- Retirement date if applicable (when a claim was retired or replaced)

Evidence files attach to the subtask (Asana attachment at v6.1 interim; SharePoint regulatory folder post-v6.3).

### 7.4 Reformulation claim-bridge gate (Rev.2)

Fires when a SKU reformulates (e.g., transition to a new manufacturer such as AMR) without QIL parity to the prior formula. Existing clinical-test claims — consumer-testing percentages ("90% of people said..."), efficacy claims ("clinically proven to..."), dermatologist-tested claims — cannot ride through reformulation by default. Formula similarity has to be established before the prior evidence supports the new formula.

Three resolution paths:

| Path | Trigger | Action |
|---|---|---|
| **a — Recover original-formula QIL** (preferred) | Operator has access to the prior manufacturer (e.g., an open order is still in motion, or the relationship is still active for unrelated reasons). | Operator drafts a request to the prior manufacturer for the QIL under NDA. The legitimate access framing per 2026-05-12 Pedrero touchbase: routine consumer-complaint investigation. With the QIL in hand, Pedrero can compare old vs new formulas and ride the prior claims through. Reg Lead approves the QIL request before send. |
| **b — Analytical comparison testing** | No path to original QIL. | Commission analytical testing comparing old and new formulas. Pedrero confirmed at 2026-05-12 this is "dicey" — viable but not preferred. Pedrero reviews results and decides whether claims ride through. |
| **c — Retire or reword the claim** | Neither path a nor path b lands. | Claims tied to consumer testing or clinical efficacy retire from the SKU. Marketing and PD update copy. Substitute claims (e.g., ingredient-data claims that don't require formula-level evidence) may be developed via §7.2 Needs new evidence path. |

**SKUs in scope at Rev.2 ratification:** Eye Cream (open order with prior manufacturer — path a window is open), Toner (recently approved formula; reformulation candidate during AMR transition), Power Oil (currently with AMR for review, prior documentation from Veggie Labs). Each gets a §7.4 task at Rev.2 first invocation.

**HITL:** Operator approves the chosen path. Reg Lead approves the QIL request send on path a. Reg Lead approves any Pedrero send on path b or path c (Job 2).

---

## 8. Retailer Attestation Response

### 8.1 Retailer scope at v6.1

| Retailer | Attestation type | Cadence |
|---|---|---|
| Sephora | Clean at Sephora + Planet Positive | Annual + ad-hoc on new SKU |
| Ulta | Conscious Beauty | Annual + ad-hoc on new SKU |
| Whole Foods | Body Care Quality Standards | Annual + ad-hoc |
| Credo | Credo Clean Standard | Annual + ad-hoc |

Other retailers added at v6.3 with regulatory-manager.

### 8.2 Drafting workflow

For each attestation:

1. Pull the retailer's current questionnaire. Templates live in SharePoint regulatory folder (Asana attachments at v6.1 interim). Templates updated when the retailer publishes a new questionnaire revision.
2. For each question, pull the matching evidence from the SKU's claim sub file. Map question to evidence category (formula composition, ingredient data, certifications, clinical, in-vitro, sourcing).
3. Draft the response per question.
4. Flag any question without sufficient evidence to Operator before Pedrero stage. Common gaps: fair-trade or organic certifications when a SKU's supplier hasn't provided them; specific ingredient sourcing details when supplier won't disclose.
5. Voice of Customer consult on questions that turn on customer-perceived attributes (e.g., Sephora Clean's "free from..." list interpretation when a borderline ingredient is involved).

### 8.3 HITL

- Operator approves the draft. Operator gate.
- Reg Lead approves the Pedrero stage. Reg Lead gate.
- After Pedrero approval (§5), Reg Lead approves the actual retailer submission. Second Reg Lead gate (separate audit-trail entry from the Pedrero send approval).

### 8.4 Submission and renewal

Once submitted, the task moves to **Active / In-Effect**. Set `Window End` to the retailer's renewal date. Renewal task fires at 60/30/14-day proximity per §9.

---

## 9. Closeout, Renewal, Close-the-Loop

### 9.1 Closeout on terminal artifacts

Once a Pedrero return is processed and the artifact lands in **Active / In-Effect** (or attestation in **Active / In-Effect** post-retailer-submission):

- Three-line summary on the Asana task: artifact type, version stamp, Pedrero reference number / approval date
- Close-the-loop comment back to the originating system: Formula Tracker for IL approvals; the marketing or PD task for new-claim approvals; the printer-side task for label archives (post-v6.3 if exists)
- `Window End` set to next re-review or renewal date

### 9.2 Renewal firing

When `Window End` approaches, the skill spawns a renewal task in **Renewal Window**:

| Reminder | Action |
|---|---|
| 60-day | Renewal task created in **Renewal Window**. Operator notified in daily sweep. |
| 30-day | Operator urgency flag escalates. Reg Lead notified. |
| 14-day | Treated as urgent. The skill auto-stages the renewal packet draft if all upstream evidence is current. |

### 9.3 Renewal categories

| Category | Default cadence |
|---|---|
| IL re-review (annual portfolio sweep) | Every 12 months from last Pedrero approval |
| IL re-review (reformulation) | Fires immediately on `IL Status = IL Reformulated — Re-review Required` |
| Retailer attestation | Per retailer's published renewal cycle (most: annual) |
| Sustained claim sub | No fixed renewal; re-fires on new evidence or new claim adds |

---

## 10. Retention and Records

Retention per SKN-OPS-001 §5.6 anchor:

| Record | Retention |
|---|---|
| IL packets sent to Pedrero | 7 years from approval date (longer than SKN-OPS-001 §5.6 default; IL records anchor active SKUs and may be requested in retailer or regulatory audits) |
| Pedrero approval/return correspondence | 7 years from correspondence date |
| Sustained claim sub evidence | 7 years from claim retirement date or 3 years from last sub use, whichever is longer |
| Label artwork archive | 3 years from artwork retirement date |
| Retailer attestation submitted responses | 3 years from submission date or 1 cycle past renewal, whichever is longer |
| Working drafts that didn't ship | 1 year from abandonment |

Storage:
- v6.1 interim: Asana task attachments. The skill's Asana task is the version-of-record; attachments live on the task.
- v6.3 forward: SharePoint regulatory folder per system-c-regulatory-scope.md decision L. v6.3 build migrates v6.1 attachments to SharePoint and updates retention pointers.

---

## 11. Procedure review

Annual review on the SOP anniversary (first review: 2027-05-09 if ratified 2026-05-09). Review path mirrors SKN-OPS-001 §7:

- Reg Lead reviews the procedure walk against actual artifact outcomes from the prior 12 months
- Pedrero consult on any substantive content updates
- Quality-manager catalog updates with new revision
- Skill SKILL.md updated with new revision reference

Mid-cycle revisions allowed when:
- Retailer attestation question structure changes materially (e.g., Sephora republishes the Clean criteria)
- A new artifact type joins scope (e.g., Amazon-specific attestations)
- An audit finding surfaces a procedure gap

---

## Appendix A — IL packet template

(To be drafted at first IL review. Lock the template at the second IL review by comparing what worked and what didn't.)

## Appendix B — Retailer questionnaire templates

(To be populated at first attestation per retailer. Templates stored in SharePoint regulatory folder post-v6.3; Asana attachments at v6.1 interim.)
