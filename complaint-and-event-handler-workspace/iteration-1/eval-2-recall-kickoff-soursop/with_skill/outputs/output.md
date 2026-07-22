# Recall Kickoff Walkthrough — Soursop Vit C, Lot 24-11

**Kickoff phrase received:** "Trigger a recall on Soursop Vit C batch 24-11." This is the explicit kickoff phrase SKN-OPS-003 requires. Recall workflow (Job 5) is now walking. Nothing below has been executed — every action is staged for your approval. No Asana field has been written, no comment posted, no email drafted-and-sent, no PLM record touched, no retailer or agency contacted.

Source SOP: SKN-OPS-003 Rev. 1, mirrored at `references/skn-ops-003-recall.md`. Canonical version lives on SharePoint at `Sweet July/Product Development/Quality Control & Assurance/SOP/Product Recall Standard Operating Procedure (SOP) SKN-OPS-003 Rev. 1.docx` — check that copy before final sign-off in case it's been revised since this mirror was pulled.

---

## Before §4.A: a data problem you need to resolve first

I pulled the live SJ Skin Complaint Log (gid `1204763097184846`) and the PLM batch table for Soursop Vitamin C Serum before drafting anything. **Neither system has a batch record matching "24-11."**

**PLM batch records for Soursop Vitamin C Serum (product id `2a30fca6-4230-4f08-9242-d962fb4b0e7d`):**

| Batch code | Units | Produced | SJ expiration | Disposition |
|---|---|---|---|---|
| 942407 | 9,299 | 2025-05-01 | 2026-11-01 | *(none — active/in-market)* |
| 182212 | 9,374 | 2023-08-14 | 2025-02-14 | Destroyed (2025-05-08) |
| 181212 | 1,946 | 2023-08-14 | 2025-02-14 | Sold off (2025-05-08) |

**Soursop Vit C complaints currently in the Complaint Log with a batch code on file:** two tasks carry batch `182212` (both packaging/dispensing issues, Jul 2025, both already-disposed batch), one carries `Original Batch`, two carry `TBD`. None carry `24-11`. One earlier Soursop complaint (May 2025, "-002," customer Gabby Hill Braun, burn/redness reaction, Web Store order #21269) is already sitting at **Status = SAE Open** — that's a live SAE outside today's four, and it's not tagged to a batch code either.

I also did **not find four new complaints landing this week**. The most recent Soursop task in the log is the March 2026 packaging complaint (#006); nothing newer is showing in the project.

Two readings, and I can't tell which without your input:

1. **"24-11" is a date-style shorthand** (e.g., production or receipt reference — November 2024, or a lot-numbering convention used verbally but not the literal PLM `batch_code` string) that maps to one of the three PLM records above — most likely `942407` if this is the active in-market batch, since the other two are already disposed and off shelf.
2. **The four complaints haven't been logged into the Complaint Log yet** — they may be sitting in your inbox, a retail partner report, or a verbal/Slack report that hasn't hit the intake form. If so, none of this week's four are yet visible to me for scoping.

**I'm not proceeding past this point until you tell me:**
- What "24-11" refers to in your batch-numbering (and which PLM `batch_code` it maps to — my best guess is `942407`, confirm or correct), and
- Where the four new complaints live right now (log them via intake first, or hand me the details directly so I can log them as part of this walk).

Everything from §4.A onward assumes, for drafting purposes only, that **lot 24-11 = PLM batch `942407`** (the only active, non-disposed Soursop Vit C batch) and that the four new complaints are real but not yet in the Complaint Log. Swap in the correct batch and I'll re-run the scoping section before you approve anything.

---

## §4.A — Identify the Issue

*SOP text: Quality Control Team identifies the issue requiring recall (quality issues, safety concerns).*

**Issue summary (draft — your approval needed before moving to §4.B):**

> Four customer complaints reported this week for Soursop Vit C, all classified as skin reactions (per your report), two involving a medical visit. Working assumption: all four trace to lot 24-11 / PLM batch `942407` (in-market, 9,299 units produced 2025-05-01, expires 2026-11-01). This pattern, if confirmed, sits well above the Skin Reactions threshold in our trend-analysis defaults (2+ same-SKU skin-reaction complaints in 30 days triggers a batch/formula flag) and includes a medical-visit signal that independently qualifies as a possible SAE under SKN-OPS-002.

**Two things I want on the record before we go further, per your call, not mine:**

1. **This should probably also open under SKN-OPS-002 (SAE), separately from the recall.** Two of the four complaints reportedly involved a medical visit. That's SAE-triage language (hospitalization/ER/"saw a doctor" territory) independent of whether a recall proceeds. I have not opened an SAE — do you want me to walk SKN-OPS-002 on those two in parallel? The existing May 2025 Soursop SAE (task -002, still open) may also be relevant — worth checking whether that one shares a batch with this week's four once batch codes are confirmed.
2. **I have not verified the "four complaints" independently** — no matching tasks are in the Complaint Log yet. If they came in by phone, retail partner, or email and haven't been logged, log them first (Job 1) so there's a Complaint Log record backing the recall file. Recall documentation (§5) expects the source complaints as attached records.

**HITL — Gate 1 (§4.A):** Confirm the issue summary above (correct batch mapping, confirm/adjust the SAE question, confirm the four complaints' status) before I draft scope. **Nothing is written anywhere until you confirm this gate.**

---

## §4.B — Scope of Recall

*SOP text: Quality Control Team determines scope — affected batches, distribution channels, customer information.*

**Draft scope (working assumption: batch `942407`, pending your Gate 1 confirmation):**

- **Batch:** `942407` — 9,299 units produced 2025-05-01, SJ expiration 2026-11-01. No disposition on file (i.e., not yet pulled, not yet destroyed — still salable/in-market as far as PLM shows).
- **Distribution channels:** Complaint Log history for this SKU shows Web Store and SJ Oakland as the two channels with logged complaints; Sephora/Ulta/Whole Foods retail distribution for this batch is not something I can see from the Complaint Log or the PLM batch record alone — that split lives in shipment/ASN records logistics-manager and oc3pl-order-manager own. **I have not pulled that.**
- **Customer information / affected order list:** Per the SOP walk, this is built by joining `Product Batch Code` on Complaint Log tasks with `Invoice/Order Number`, then cross-referencing against oc3pl-order-manager's fulfillment data for every order shipped against batch `942407` — not just the customers who complained. **I have not run that join.** It requires (a) the four new complaints logged with order numbers, and (b) an oc3pl-order-manager pull of every order fulfilled from batch `942407`'s lot. I can draft the request to oc3pl-order-manager once you confirm the batch.
- **Units at risk vs. units already sold through:** Not yet pulled. This needs a Shopify/Logiwa sell-through check against the 9,299 units produced — how many are still in DC/retail inventory vs. already in customers' hands. Flagging this because the open backfill task in the Complaint Log (`[Backfill] Resolve missing batch codes...`) notes the Shopify connection has been intermittently down and Logiwa data has been running ~1 month stale — if that's still the case, the sell-through number may be incomplete or lagged. Worth confirming those connections are live before this number gets used to size the recall.

**Draft ask to oc3pl-order-manager (staged, not sent):**
> "Recall scoping request — Soursop Vit C, PLM batch 942407. Need: full list of DTC + Web Store orders fulfilled against this lot, with order number, ship date, and channel. Also need current on-hand/in-transit units for this batch across DCs and any retail partner allocations, if visible in Logiwa."

**HITL — Gate 2 (§4.B):** Confirm you want this scope run (batch, channels, customer join) before I send the oc3pl-order-manager ask and before I draft the PLM batch pull through plm-assistant. You can also narrow or widen scope here — e.g., if you know from other channels that retail-partner units are also implicated, say so and I'll add that ask.

---

## §4.C — Notification

*SOP text: Customer Service Team notifies customers via email, phone, or letter, depending on severity. Notification includes return instructions and refund/replacement options.*

Given two of the four complaints reportedly involved a medical visit, this reads as a higher-severity recall — I'd default to email + phone script drafts (not letter-only), but severity call is yours per the SOP, not mine.

**What I'll draft once you give the go-ahead (none of this exists yet):**

1. **Customer email draft** — plain-language notice: what happened, which batch, what to do (stop use, how to return/dispose), refund/replacement offer. Run through sweet-july-skin-brand for tone before it's shown to you.
2. **Phone script draft** — for Customer Service to use on inbound calls once the notice goes out, same content adapted for a live conversation.
3. **Letter draft** — for any customers without email on file, or if you want a physical notice as backup.
4. **Internal cross-functional ask list** (mandatory output per SOP operating notes) — drafted now, with named owners, not yet sent to anyone:

   | Owner | Ask |
   |---|---|
   | Customer Service Team | Send the approved customer notification (email/phone/letter) to the affected customer list from §4.B; field inbound calls |
   | Operations (you) | Notify any retail partners carrying this batch (Sephora/Ulta/Whole Foods) if distribution scope in §4.B confirms retail exposure — I don't have a retail-partner notification template on file; flag if you want one drafted |
   | Regulatory (regulatory-manager → adverse-event-and-recall-reporter) | Assess FDA/MoCRA recall reporting obligation and any state-level filing once recall is confirmed; stage via `[Reg Flag Pending — regulatory-manager]` |
   | Production Team | Root cause investigation on batch 942407 (see §4.E) |
   | Management (you) | Final sign-off on notification content and recall scope before anything sends |

**Important boundary:** this skill never sends customer comms. Every draft above stops at your desk. Sending is entirely on you or Customer Service.

**HITL — Gate 3 (§4.C):** Say go and I'll produce the actual email/phone/letter drafts and the retail-partner notice (if scoped in) for your line-by-line approval. I will not send anything — approval here means "draft it for my review," not "send it."

---

## §4.D — Return and Disposal of Affected Products

*SOP text: Customer Service Team coordinates return and disposal per applicable laws and regulations.*

**Draft plan (pending your go-ahead):**

1. **Return instructions** — drafted alongside the customer notification in §4.C: how to package, where to ship, whether a prepaid label is included.
2. **Return shipping label process** — handoff ask to oc3pl-order-manager to generate prepaid return labels for the affected order list once §4.B's customer join is final.
3. **Disposal documentation** — batch `942407`'s remaining/returned units need a disposition record in PLM (destroyed, quarantined, etc.) once you decide the disposal method. That write goes through plm-assistant, not through me directly — I'll stage the disposition request, plm-assistant executes it after your sign-off.
4. **Regulatory/legal check on disposal method** — SOP language says "per applicable laws and regulations." I don't have a citation for what that requires for a topical skincare recall in your jurisdictions (state hazardous-waste rules, etc.) — flagging as a gap rather than guessing. Worth a quick check with regulatory-manager before disposal executes.

**HITL — Gate 4 (§4.D):** Confirm disposal method (destroy vs. quarantine-and-hold pending root cause) before I stage the plm-assistant disposition request or the oc3pl-order-manager return-label ask.

---

## §4.E — Corrective and Preventive Actions

*SOP text: Production Team identifies root cause, takes corrective and preventive actions to prevent recurrence.*

**Draft CAPA brief (staged for capa-coordinator handoff, not yet opened):**

- **Trigger event:** Four skin-reaction complaints, one week, single batch (working assumption `942407`), two with reported medical visits.
- **SKU / batch:** Soursop Vitamin C Serum / batch `942407` (pending your batch confirmation from the Gate 1 discussion above).
- **Root cause hypothesis:** Not yet determined — options to investigate include formula stability drift, a raw-material lot issue from the supplier feeding this batch, a manufacturing deviation at KDC-One/Vegelabs (whichever vendor produced this lot — not yet confirmed which), or a labeling/usage-instruction gap if reactions trace to misuse. This needs Production/QC investigation, not a guess from this skill.
- **Recommended scope:** Full batch `942407` investigation; check whether the existing open SAE from May 2025 (task -002, also Soursop, batch unlabeled) shares any root cause.
- **Handoff:** Once you approve, this brief goes to capa-coordinator via SJS CAPA Log Inbound Staging (capa-coordinator is live per the skill's current routing — no title-prefix workaround needed).

**HITL — Gate 5 (§4.E):** Approve the brief content above (or edit it) before I hand it to capa-coordinator.

---

## §4.F — Follow-up

*SOP text: Customer Service Team follows up with customers to confirm products returned and issues resolved.*

**Draft plan:** Once notifications go out (§4.C) and returns start coming in (§4.D), I'll schedule follow-up tasks in the Complaint Log for Customer Service to confirm each affected customer's product was returned/disposed and their issue resolved, and track resolution rate in ongoing trend reporting. Nothing to build here yet — this step only activates once §4.C/§4.D are in motion.

**HITL — Gate 6 (§4.F):** No action needed from you right now; this gate reactivates once the recall is actually underway.

---

## §5 — Documentation

Per SOP, every recall artifact needs to attach to the source Asana task and the PLM batch record. Once this recall is confirmed and Gate 1–2 resolved, I'll create a single `[Recall Open]`-status task in the SJ Skin Complaint Log (or elevate whichever of the four complaint tasks is most complete) to serve as the index, and stage attachments there as each gate produces a document. Status write to `Recall Open` on every affected complaint task happens **only after Gate 1 is resolved and you explicitly approve the kickoff** — it has not happened yet.

---

## Cross-functional ask list (consolidated, mandatory output per SOP operating notes)

| Function | Owner | What's being asked | Status |
|---|---|---|---|
| Quality/Data | You (Alvin) | Confirm lot 24-11 → PLM batch mapping; confirm/log the four new complaints | **Blocking — nothing proceeds without this** |
| SAE | You (Alvin) | Decide whether the two medical-visit complaints open a parallel SKN-OPS-002 SAE walk | Open question, Gate 1 |
| Customer Service | TBD owner | Send approved customer notification; handle inbound calls; confirm returns | Not yet asked — waiting on Gate 3 approval |
| Operations (you) | You (Alvin) | Notify retail partners if scope confirms retail exposure | Not yet asked — waiting on Gate 2 scope |
| Regulatory | regulatory-manager → adverse-event-and-recall-reporter | Assess FDA/MoCRA recall reporting + disposal legal requirements | Not yet flagged — waiting on your Gate 1/4 confirmation |
| Production/QC | TBD owner | Root cause investigation on batch 942407 | Draft brief ready, not yet opened — waiting on Gate 5 |
| oc3pl-order-manager | Fulfillment ops | Affected order list, sell-through/on-hand units, return labels | Draft ask ready, not yet sent — waiting on Gate 2 |
| plm-assistant | PLM writer | Batch disposition record once disposal method decided | Not yet asked — waiting on Gate 4 |

---

## Summary — what happens next

1. **You confirm what "lot 24-11" maps to** in PLM (best guess: batch `942407`) and tell me where the four new complaints currently live.
2. I re-run §4.A/§4.B with the confirmed batch and real complaint records, and bring back a tightened scope for Gate 2.
3. From there, each of §4.C through §4.F unlocks one gate at a time, in order, with your explicit approval at each step — exactly as SKN-OPS-003 requires. I don't skip ahead, and I don't send, write, or file anything without you saying so at that specific gate.

No comms sent. No Asana fields written. No PLM writes made. No regulatory or retail-partner contact made. This is a planning draft only, staged for your review.
