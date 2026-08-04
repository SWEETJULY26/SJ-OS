---
sop_id: SKN-OPS-008
title: IL / Claims / Label Procedure
revision: "2"
status: ratified
owner: Alvin Belt, VP of Operations
effective_date: 2026-05-12
next_review_date: 2027-05-12
---

# IL / Claims / Label Procedure

## 1. Why this exists

Sweet July Skin's regulatory artifacts — ingredient lists, sustained claim substantiation, label artwork versions, retailer attestation responses — used to scatter across Slack, Outlook attachments, founder folders, and individual heads. Pedrero Regulatory does the substantive review work, but without a documented procedure, IL versions drift from what's actually printed, sustained claim substantiation isn't audit-ready, new claims slip onto packaging without sign-off, and retailer attestations get missed or renewed without fresh review. This procedure closes those gaps: every regulatory artifact is staged through Pedrero, archived with a version stamp, and renewed on cadence. Anchors: SKN-OPS-001 §5.6 (retention).

## 2. Scope

Applies to any pre-launch or post-launch regulatory artifact for a Sweet July Skin SKU: the ingredient list (IL) for any approved formula including reformulations; sustained claim substantiation evidence; new claims added to packaging or marketing copy after launch; component and carton label artwork archive (with IL match cross-check); and retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo).

Does not apply to: pre-launch claim evidence generation (clinical, in-vitro, ingredient data — PD keeps); MoCRA registrations, state filings, the retailer attestation cadence dashboard; SAE filing prep or FDA recall agency reporting (SKN-OPS-009); international regulatory work; print-side QA, color management, dieline approval; or vendor compliance docs at intake (COA, COC, COI, MSDS).

## 3. Roles

| Role | Responsibility |
|---|---|
| **Reporter** | Any employee, designer, or external partner surfacing an artifact for review. |
| **Operator** | Reviews intake, classifies the artifact, drafts packet contents, approves the path forward. |
| **Reg Lead** | Internal sign-off on every Pedrero send and every retailer-facing submission — a distinct gate even when held by the same person as Operator. |
| **External Reg Partner** | All substantive regulatory review; Pedrero Regulatory (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary). No internal authority. |
| **QA Lead** | Consult-only on quality-side overlaps. |
| **Voice of Customer** | Consult-only on retailer attestation responses turning on customer-perceived attributes. |

## 4. IL Review Gate

### 4.1 What triggers a review

A formula reaching final sign-off in the PD tracker; a reformulation event; or an explicit request (e.g., a portfolio-level IL review ahead of a new retailer).

### 4.2 IL packet contents

SKU code and name; formula version stamp; full INCI list in regulatory order; EU 26-allergen breakdown flagging anything present above the leave-on/rinse-off thresholds (informational — Pedrero confirms applicability); a Canada extended-allergens disclosure when the SKU is in scope for Canadian distribution; supporting docs (formula composition sheet, supplier IL attestations); a 19-state packaging-toxics certificate of compliance for retailer-distributed SKUs (one certificate per active component supplier certifying heavy metals at or below 100 ppm collectively — a missing certificate pauses IL approval unless the SKU is DTC-only, which may proceed with Operator sign-off); the prior IL version and a diff, if a reformulation; a note on whether the prior formula's qualitative ingredient list (QIL) has been recovered for a reformulation (if not, see §7.4 before any clinical claim rides through); a new version stamp (`IL-[SKU-CODE]-v[N]`); and a plain-language reg question.

### 4.3 HITL

Operator approves packet contents at intake. Reg Lead approves the Pedrero send; the send itself is composed and then sent manually after that approval.

## 5. Pedrero Send Mechanics

Correspondence uses a consistent subject prefix by artifact type (`[IL Review — SKU-CODE]`, `[New Claim Sign-Off — SKU-CODE]`, `[Attestation Review — RETAILER — SKU-CODE]`, `[Label Cross-Check — SKU-CODE]`, with a `— Re-review` suffix for annual or reformulation re-reviews). Default return window is 10 business days, tightened with an explicit `URGENT — by [date]` when a retailer deadline binds. Sends are never automated — drafted and staged, sent manually after Reg Lead approval, moving the record to **In Pedrero Review** with the outbound timestamp captured.

## 6. Pedrero Return Processing

**Approved** — moves to Active/In-Effect; IL syncs back to the formula tracker as approved, claims add to the claim sub file, attestations become ready for retailer submission, label archive entries are written.

**Returned for revision** — moves to Returned — Action Required with Pedrero's rationale captured; routes to the next step per artifact type.

**Question / clarifying request** — a clarifying reply is staged and Reg Lead-approved; the record stays In Pedrero Review.

Verbal approvals from a call do not satisfy this procedure — a written confirmation send is staged (`[CONFIRMING — ... — verbal OK on call]`) and archiving happens only after a written reply.

## 7. Label Artwork Cross-Check and Archive

For each artwork piece in scope (primary cartons, primary component, printed inserts — other packaging out of scope by default, extendable per SKU), four passes run in sequence; any fail pauses the archive until resolved.

**Pass 1 — IL match.** Compares the artwork's printed IL to the latest approved version. A match advances; a drift to an older approved version or an unapproved IL pauses for resolution; a new unsubbed claim on the artwork routes to §8; an already-printed-with-wrong-IL discovery still archives the truth but opens a remediation task.

**Pass 2 — Pantone per CA SB 343.** For any component or carton showing the recycling chasing-arrows symbol: pass (Pantone within the approved gradient) advances; lighten (adjustable) or remove-symbol (stays dark per brand) route back to the designer; unclear stages to Pedrero.

**Pass 3 — Canada extended-allergens.** Fires only when the SKU is in scope for Canadian distribution. Pass advances; missing routes to the designer for revision (any Canada-bound SKU without this pass cannot ship to Canada past the applicable cutoff); unclear stages to Pedrero.

**Pass 4 — Quebec French-language.** Fires only when the SKU is in scope for Quebec distribution. Pass (every inscription bilingual) is the only outcome that archives; partial (mandatory statements bilingual, others English-only) routes to translation; fail routes back for bilingual rework; unclear stages to Pedrero or Ecomundo.

A new Pedrero send is required only when the artwork's IL doesn't match an already-approved version, carries an unsubbed claim, or is a retailer-specific variant triggering attestation-tied review. A simple match with no new claims archives on Operator + Reg Lead approval alone.

## 8. New-Claim Sign-Off

### 8.1 What counts as a new claim

Any claim added to packaging, marketing copy, retailer-facing copy, or an e-commerce product page that wasn't present at launch or the last attestation cycle, including claim text changes. Ingredient-name corrections and non-substantive copyediting are out of scope.

### 8.2 Three paths

**Covered by existing evidence** — staged to Pedrero citing the existing evidence reference for sign-off.

**Needs new evidence** — paused; the evidence-generation ask routes to PD; proceeds via the covered path once evidence lands.

**Not defensible** — flagged to the Operator with rationale to reword or drop; not staged to Pedrero, since Pedrero reviews defensible claims rather than authoring rewrites.

### 8.3 Claim sub file

One record per SKU, one entry per claim: exact claim text, evidence reference, Pedrero approval reference (subject + date), effective date, and retirement date if applicable.

### 8.4 Reformulation claim-bridge gate

Fires when a SKU reformulates without QIL parity to the prior formula. Existing clinical-test, efficacy, and dermatologist-tested claims cannot ride through by default — formula similarity must be established first. Three resolution paths: **(a) recover the original-formula QIL** (preferred, when access to the prior manufacturer still exists — Reg Lead approves the request before send); **(b) commission analytical comparison testing** when path (a) isn't available (Pedrero reviews the results and decides); **(c) retire or reword the claim** when neither lands. Operator approves the chosen path; Reg Lead approves any resulting request or Pedrero send.

## 9. Retailer Attestation Response

Covers Sephora (Clean at Sephora + Planet Positive), Ulta (Conscious Beauty), Whole Foods (Body Care Quality Standards), and Credo (Credo Clean Standard), each on an annual-plus-ad-hoc cadence. Each response: pulls the retailer's current questionnaire; maps each question to matching evidence from the claim sub file; drafts the response; flags any question without sufficient evidence before staging to Pedrero; and pulls in Voice of Customer consult where a question turns on customer-perceived attributes.

Operator approves the draft. Reg Lead approves the Pedrero stage, and — after Pedrero approval — Reg Lead separately approves the actual retailer submission, a second and distinct gate. Once submitted, the record moves to Active/In-Effect with the renewal date set for the §10 reminder cadence.

## 10. Closeout, Renewal, Close-the-Loop

On a terminal artifact: a three-line closeout summary (artifact type, version stamp, Pedrero reference/approval date); a close-the-loop note back to the originating system; and a renewal or next-review date set.

Renewal reminders fire at 60 days (task created, Operator notified), 30 days (urgency flag, Reg Lead notified), and 14 days (treated as urgent — the renewal packet auto-stages if upstream evidence is current). Default cadence: annual IL portfolio sweep every 12 months; reformulation IL re-review fires immediately on a reformulation event; retailer attestation follows the retailer's own published cycle (most: annual); sustained claim sub has no fixed renewal and re-fires on new evidence or new claims.

## 11. Retention

| Record | Retention |
|---|---|
| IL packets sent to Pedrero | 7 years from approval date |
| Pedrero approval/return correspondence | 7 years from correspondence date |
| Sustained claim sub evidence | 7 years from claim retirement, or 3 years from last use, whichever is longer |
| Label artwork archive | 3 years from artwork retirement |
| Retailer attestation submitted responses | 3 years from submission, or 1 cycle past renewal, whichever is longer |
| Working drafts that didn't ship | 1 year from abandonment |

## 12. Procedure Review

Annual review on the SOP anniversary. Reg Lead reviews the procedure walk against actual artifact outcomes from the prior 12 months, with Pedrero consult on substantive updates. Mid-cycle revisions are triggered by a material change to a retailer's attestation structure, a new artifact type entering scope, or an audit finding surfacing a procedure gap.

## 13. Revision History

| Revision | Date | Description | Author |
|---|---|---|---|
| 1 | 2026-05-09 | Initial issue. | Alvin Belt |
| 2 | 2026-05-12 | Post-Pedrero touchbase update: §4.2 adds the 19-state packaging-toxics certificate as a required IL packet element; §7 adds three passes to the label cross-check (Pantone per CA SB 343, Canada extended-allergens, Quebec French-language); §8.4 adds the reformulation claim-bridge gate (Eye Cream, Toner, and Power Oil flagged as initial scope). | Alvin Belt |
