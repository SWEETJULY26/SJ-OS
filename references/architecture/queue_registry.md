# Asana queue registry

**Use:** The one place that records, per Asana queue, its project GID, its sections, its state field, and the **state → section map**. Skills read this instead of hard-coding section GIDs into their own bodies. Where a queue declares an Asana Rule owns section movement, skills write the state field only and never issue a section move.

**Scope:** The eleven queues named in `bridge_queue_contract.md`. Companion to `asana_task_contract.md` (what a write looks like) and `bridge_queue_contract.md` (which queue a task belongs to). This file answers *where inside the queue a task sits, and why*.

**Pulled live:** 2026-07-31, via `get_project` with `include_sections` and `custom_field_settings`. Every GID below came from the API, not from a skill body — several skill bodies were already stale (see Drift found, at the end).

**Last updated:** 2026-08-01 — Drift cleared: every skill body listed at the end now agrees with this file. Authored 2026-07-31. Closes the gap Alvin found: a PO could reach `Status = Received` with no rule moving it out of `POs In Flight`, because no state → section map existed in any file, for any queue.

---

## The authority rule

**The state field is the source of truth. Section is a projection of it.**

Where a queue has a state field, skills write that field and derive the section from the map below. Where the queue's row says a Rule owns movement, skills do **not** call `update_tasks` with `add_projects` to move sections — the Rule does it, and a second writer means last-write-wins.

Three queues have no state field by deliberate design and carry state in their sections instead. They are marked **section-as-state** and are exceptions, not gaps to fill.

`Gate` is orthogonal to both everywhere it appears. It records who is holding the puck, never where the task sits.

---

## AC Brands Purchasing — `1214373717266702`

**State field:** `Status` — `1214373372406268` · **Authority:** Status · **Rule owns movement:** yes (to build)

| Section | GID |
|---|---|
| Cross-Skill Dashboard | `1214843467424921` |
| HITL — Needs Operations Review | `1214373372406259` |
| POs In Flight | `1214373372406260` |
| Receiving | `1214373372406261` |
| Sourcing & RFQ | `1214373372406263` |
| Vendor Onboarding | `1215139855143672` |
| Vendor Invoices | `1215148455338976` |
| Compliance, Renewals & Disputes | `1214373372406262` |
| Closed | `1214373372406264` |

### State → section

| Status | Option GID | Section |
|---|---|---|
| Draft | `1214373372406269` | HITL — Needs Operations Review |
| Sent | `1214373372406270` | POs In Flight |
| Acknowledged | `1214373372406273` | POs In Flight |
| In Transit | `1214373372406271` | POs In Flight |
| Received | `1214373372406272` | **Receiving** |
| Variance | `1214370303255335` | HITL — Needs Operations Review |
| Dispute | `1214373372406274` | Compliance, Renewals & Disputes |
| On Hold | `1214373372406276` | POs In Flight |
| Closed | `1214373372406275` | Closed |
| Cancelled | `1214370303255310` | Closed |

Every row except `Received` restates behavior already in `purchasing-manager/SKILL.md:107,112,116,120,124,140`. **`Received → Receiving` is new** — it is the transition that had no trigger anywhere, which is why a received PO could sit in POs In Flight while the weekly scan at `SKILL.md:335` reported it as Receiving.

`POs In Flight` deliberately spans Sent, Acknowledged, In Transit and On Hold — the section means "issued, not yet here." A PO on a vendor hold has not moved backwards, so it stays.

Sourcing & RFQ, Vendor Onboarding, Vendor Invoices and Cross-Skill Dashboard hold task types that are not POs and have their own state (`Vendor Invoices` tasks carry a separate `State` field, `purchasing-manager/SKILL.md:316`). The map above governs PO tasks only.

## AC Brands Inventory — `1214374368959019`

**State field:** none usable · **Authority:** section + title prefix · **Rule owns movement:** no

| Section | GID |
|---|---|
| HITL — Needs Operations Review | `1214374252744518` |
| Active Movements | `1214374252744520` |
| Stock Risks | `1214374252744521` |
| Reconciliation | `1214374252744522` |
| Closed | `1214374252744523` |

A `Status` field exists — `1214374252744527` — but its options are `Pending Review` / `Approved` / `In Progress` / `On Hold` / `Closed` / `Cancelled`: a generic approval vocabulary that describes none of this queue's actual states. `inventory-manager` carries state in title prefixes instead (`SKILL.md:139-149`: `[Receive]`, `[Low Stock]`, `[Position Variance]`, …). Treat the field as a leftover, not a state field.

### What is actually in this queue — pulled 2026-08-01

42 tasks, 21 open. Two numbers decide the redesign:

**One task of 42 has a non-null Status** — `Terry Headband — Update UPC` `1216724829783968`, set to `Pending Review`. The field has effectively never been used, so re-optioning it costs one task.

**One task of 42 uses a title prefix** — the `[Receive]` on PO 100310 `1217082576096228`, created during this session's Element work. The eleven-prefix vocabulary at `inventory-manager/SKILL.md:139-149` is documented but not practiced; every other task carries a plain descriptive name. So the queue has no working state mechanism at all right now — not a field, and not the prefixes the skill claims to use instead.

Thirteen of the 21 open tasks are `Send [SKU] to Amazon FBA`, multi-homed into `Active Movements` from their SKU project's `Phase 5 - Final Production`. That is what this queue mostly holds, and it is why the section names are work-type buckets rather than phases.

**Resolved 2026-08-01.** Eleven of these tasks also reported membership in an `Untitled section` `1216923764491937` that is not one of the five above. It belonged to `Ciarra Robinson's previously assigned tasks` `1216923783441065`, a departed-staff handoff project — `memberships` spans every project a task belongs to, which is the trap recorded in `asana_task_contract.md`, and `get_project` confirmed Inventory has exactly five sections. All 23 tasks in that project were already assigned to Alvin, so per his call the project membership was stripped from all 23 and the project is now empty, pending archive in the UI. Worth remembering as the cheapest possible illustration of the trap: a phantom sixth section that dissolved on one `get_task`.

### Field change to make this rulable

Re-option `Status` `1214374252744527`. Delete the six generic options and create these seven:

| Status | Section |
|---|---|
| Pending Review | HITL — Needs Operations Review |
| Receiving | Active Movements |
| Movement In Flight | Active Movements |
| Stock Risk | Stock Risks |
| Reconciling | Reconciliation |
| Closed | Closed |
| Cancelled | Closed |

Seven options onto five sections — many-to-one, which is all a rule needs. Record the new option GIDs here on creation.

**Why not one option per title prefix.** The eleven prefixes name *work types*, not states, and work type alone cannot pick the section: a `[Write-Off Review]` awaiting approval belongs in HITL, and the same task after approval does not. Section here is a function of gate-and-position, which is what the seven options above encode. Keep the prefixes in titles for the finer distinction — they are free text and cost nothing. If the work type ever needs to be queryable ("show me every near-expiry item"), add a separate `Work Type` field that has **no** bearing on section, orthogonal the way `Gate` is elsewhere. Do not fold work type into Status.

**Migration:** set `Status = Movement In Flight` on the thirteen FBA-send tasks, `Pending Review` on the three in HITL, `Reconciling` on the one in Reconciliation, and `Closed` on the 21 completed. Roughly 38 writes, all mechanical, all derivable from current section — a skill can do it in one pass once the options exist.

## Sweet July Skin S&OP — `1214347479282044`

**State field:** none · **Authority:** section-as-state (declared) · **Rule owns movement:** no

| Section | GID |
|---|---|
| Untitled section | `1214347479282072` |
| Monthly run | `1214374670198667` |
| Buy Recommendations | `1214374670198668` |
| Filler Schedule | `1214374670198669` |
| Exceptions | `1214374670198670` |
| Risk Watch | `1214374670198671` |
| Archive | `1214374670198672` |

Declared exception at `supply-demand-planner/SKILL.md:218-224`. Its fields (`Buy Type`, `Urgency`, `Exception Reason`, `Recommended Qty`, `Target Ship By`, `Run ID`) classify and parameterize; none sequences. Documented movement: Buy Recommendations → Archive on PO placement. Risk Watch tasks stay until individually closed.

Live section name is **`Monthly run`**, lowercase r. `asana-s-and-op-schema.md` wrote `Monthly Run`, so a literal name match failed; it now resolves by GID `1214374670198667`. Resolve by GID here too.

## Sweet July Skin Logistics — `1214370420013442`

**State field:** `Shipment Status` — `1214374904674302` · **Authority:** Status · **Rule owns movement:** yes, once the restructure below lands

| Section | GID |
|---|---|
| Inbound — FG | `1214370392291417` |
| Inbound — Components | `1214370420023360` |
| Outbound — Retailer | `1214370316148957` |
| Outbound — Escalations | `1214370392301497` |
| Customs Watch | `1214370392286066` |
| Compliance Specs | `1214370392301434` |
| Weekly Digest | `1214370529340765` |
| Archive | `1214370302915904` |

Options: Pre-Ship `1214374904674303` · In Transit `1214374904674304` · At Port `1214374904674305` · In Clearance `1214374904674306` · Delivered `1214374904674307` · Exception `1214374904674308` · Closed `1214374904674309`.

Sections here split by *direction and cargo type* while Shipment Status splits by *position in transit*. The two axes are independent: a Pre-Ship inbound component shipment and an In Transit one both belong in `Inbound — Components`. So status alone cannot pick the section, and `logistics-manager` never states the combined rule despite `SKILL.md:330` saying "advance the section."

### The bigger problem, found 2026-08-01

**`Shipment Status` was being used as a generic progress field on tasks that are not shipments.** Of 35 tasks, roughly four were actual freight. The rest were two workstreams — Canada DTC compliance and Korea Masks — whose tasks had been given shipment positions standing in for not-started / doing / done:

| Task | Shipment Status it carried |
|---|---|
| Canada DTC — Decide approach (DDP vs DDU vs pause) | Pre-Ship |
| Canada DTC — Engage Pedrero Regulatory on CNF filings | Pre-Ship |
| Canada DTC — Implement chosen approach | In Transit |
| Canada DTC — Set up 60-day monitoring | Delivered |
| Korea Masks — Source 3 customs broker quotes | Pre-Ship |
| Korea Masks — Log customs costs to PLM | Delivered |

A rule built on the field in that state would have moved "Set up 60-day monitoring" into a Delivered section. **Cleared on 17 tasks, 2026-08-01**, per Alvin's call: the workstream tasks stay where they are, they just no longer carry a shipment position. Six tasks kept the field because they genuinely describe a shipment — PO 100346, PO 100338 (Soursop), the PO 100310 receipt, the two Pava Toner outbounds, and the UPS clearance escalation.

Four of the eight sections held nothing but their section seed.

### Restructure — decided 2026-08-01

**Sections carry position. Direction becomes a field.** Alvin's call, and it follows the registry's own principle: direction is set once when a shipment is created and never changes, so it is field-shaped. Section should carry what moves.

**Add field `Direction`** (single-select): `Inbound — FG` · `Inbound — Components` · `Outbound — Retailer` · `Outbound — DTC` · `Outbound — Sample`. Record its GID and option GIDs here on creation.

**Sections — rename two, add four, delete three, keep three:**

| Action | Section | GID |
|---|---|---|
| rename → `In Clearance` | Customs Watch | `1214370392286066` |
| rename → `Exception` | Outbound — Escalations | `1214370392301497` |
| add | Pre-Ship | — |
| add | In Transit | — |
| add | At Port | — |
| add | Delivered | — |
| add | Closed | — |
| delete | Inbound — FG | `1214370392291417` |
| delete | Inbound — Components | `1214370420023360` |
| delete | Outbound — Retailer | `1214370316148957` |
| keep | Compliance Specs | `1214370392301434` |
| keep | Weekly Digest | `1214370529340765` |
| keep | Archive | `1214370302915904` |

Rename rather than delete-and-recreate on the two, so their GIDs stay valid in `logistics-manager` and `oc3pl-order-manager`.

**Target map — 1:1, fully rulable:**

| Shipment Status | Option GID | Section |
|---|---|---|
| Pre-Ship | `1214374904674303` | Pre-Ship |
| In Transit | `1214374904674304` | In Transit |
| At Port | `1214374904674305` | At Port |
| In Clearance | `1214374904674306` | In Clearance |
| Delivered | `1214374904674307` | Delivered |
| Exception | `1214374904674308` | Exception |
| Closed | `1214374904674309` | Closed |

`At Port` stops being ambiguous under this model — it is a position, not a place, so the destination-vs-origin question no longer arises. `Compliance Specs`, `Weekly Digest` and `Archive` take no rule; they hold non-shipment records and pinned digests.

**Cost Alvin accepted:** the board no longer groups inbound vs outbound at a glance. Group by the `Direction` field instead. Worth it because full rule coverage removes the two-writer problem on the one queue that would otherwise keep it.

**Migration:** small, because only six tasks carry the field.

- PO 100346 `1215318129849303` → `Direction = Inbound — Components`, section Pre-Ship
- PO 100338 / Soursop `1211654563799701` → `Direction = Inbound — Components`, section Pre-Ship
- PO 100310 receipt `1216247022531162` → `Direction = Inbound — FG`, stays in Archive (completed)
- Pava Toner bulk to NewBeauty `1214622982736967` → `Direction = Outbound — Retailer`; **its status reads `Pre-Ship` while the task is completed and archived** — set `Closed`
- Pava Toner editorial samples `1214622865699529` → `Direction = Outbound — Sample`; same stale `Pre-Ship` on a completed task — set `Closed`
- UPS clearance escalation `1214624750932762` → `Direction = Outbound — DTC`, section Exception

Delete the section seeds for the three sections being removed; they document a layout that will no longer exist.

**Not operationally proven.** PLM's `shipments` table is empty and this queue has never carried freight at volume. The map above says what should happen; it has not yet been exercised.

## OC3PL Order Management — `1214235522292179`

**State field:** none — zero custom fields on the project · **Authority:** section-as-state (declared) · **Rule owns movement:** no

| Section | GID |
|---|---|
| ⚙️ SOPs & Templates | `1214235510232195` |
| 📋 Daily Report Log | `1214235556157469` |
| 📊 Weekly Review | `1214235510232259` |
| 🚨 Escalations / Issues | `1214235699359875` |

Declared exception at `oc3pl-order-manager/SKILL.md:96-102`. Verified live: the project has no custom fields at all.

## SJ Shipping Dashboard — `1206266539116267`

**State field:** none · **Authority:** section-as-state (declared) · **Rule owns movement:** no

| Section | GID |
|---|---|
| Errors | `1206266372382518` |
| Shipment Status - Red Alert 🚨 | `1214551768859816` |
| Shipment Status - Action Needed ⚠️ | `1214503713493616` |
| Shipment Status - Awareness 📌 | `1214551768859815` |
| Order Exceptions | `1213031356345787` |
| Returns | `1206266372382519` |
| Return to Sender | `1206266539116278` |
| Completed | `1206266374154293` |

Same declared exception. Its fields (`Order Error Type`, `Shipping Error Type`, `Return Status`, `Resolution Status`, `Replacement Order Created`, `Product Collection`) classify rather than sequence. Note the three `Shipment Status - …` **sections** are triage severity and have nothing to do with the Logistics `Shipment Status` **field** — same words, unrelated meaning.

## SJS Quality Management — `1214660401644163`

**State field:** `Status` — `1214660437047242` · **Authority:** Status · **Rule owns movement:** no (two workflows share one field)

| Section | GID |
|---|---|
| Running Log | `1214843467424901` |
| Cross-cutting Tasks | `1214660700812914` |
| Inbound Staging | `1214660401653157` |
| SOP Catalog | `1214660700812917` |
| Lab Findings Open | `1214660713569696` |
| Vendor Flag Review | `1214661413440412` |
| Batch — Active in Market | `1214660393603698` |
| Batch — Stability Schedule | `1214660393603699` |
| Batch — Watch | `1214660700812911` |
| Batch — Hold/Release Review | `1214660393603700` |
| Batch — On Hold | `1214660700812912` |
| Batch — Closed (Released, Expired, Pulled) | `1214660700812913` |
| Scorecard Signal Posted | `1214660194909535` |
| CAPA Handed Off | `1214660401653221` |
| Watch List | `1214660713569760` |
| Closed | `1214660716447873` |

The `Status` field carries **15 options spanning two unrelated workflows** — lab findings (Inbound, Triage, Vendor Flag Review, Scorecard Signaled, CAPA Open, Watch, Closed) and batch lifecycle (Active, Stability Pending, Hold/Release Review, On Hold, Released, Pulled, Expired), plus `Pending` `1214660230825945`, which appears in no skill's documented option list. A single rule keyed on this field cannot serve both, since `Watch` and `Closed` mean different sections depending on which workflow the task belongs to.

### The field does not need splitting — the second field already exists

`Batch State` `1214660230825974` is already on this project with exactly the eight batch options: Active `…825975` · Stability Pending `…825976` · Hold/Release Review `…825977` · On Hold `…825978` · Watch `…825979` · Released `…825980` · Pulled `…825981` · Expired `…825982`. `batch-lifecycle-tracker/SKILL.md:151,158` defines both fields with overlapping vocabularies and writes only `Status`.

**Pulled 2026-08-01, and the data settles which one wins.** All seven batch tasks carry both fields. On four they agree. On three they disagree, and `Batch State` is the one that matches the section:

| Task | Status | Batch State | Section |
|---|---|---|---|
| Coffee Fix Peptide Eye Cream — 25E22D1 | Active | Active | Batch — Active in Market |
| Pava Exfoliating Cleanser — 950407 | Active | Active | Batch — Active in Market |
| Irie Power Face Oil — 941407 | Active | Active | Batch — Active in Market |
| Castaway Cream — 875502 | Active | Active | Batch — Active in Market |
| Soursop Vit C — 942407 | Active | **Watch** | **Batch — Watch** |
| Pava Toner — 930312 | Active | **Watch** | **Batch — Watch** |
| Good Youth Retinol — 617411 | Active | **Watch** | **Batch — Watch** |

`Batch State` is already the authoritative field for batch tasks in practice. `Status = Active` is a stale duplicate that is wrong on three of seven. So the change is to **retire the eight batch values from `Status`**, not to split it or build anything.

### What is actually in this queue

95 tasks, 40 open. `Status` is set on 15; `Batch State` on 7. The other 80 tasks carry no state at all — including all 21 in `Inbound Staging` and all 57 in `Closed`.

Nine of the sixteen sections hold zero tasks: `Running Log`, `Lab Findings Open`, `Vendor Flag Review`, `Scorecard Signal Posted`, `CAPA Handed Off`, `Watch List`, `Batch — Hold/Release Review`, `Batch — On Hold`, `Batch — Closed`. The lab-findings half of this queue has never run a task through it.

`Pending` turns out not to be junk — it marks a **third** workflow. All five uses are cross-cutting items: four `[SOP Annual Review]` tasks and one closed migration decision, all in `Cross-cutting Tasks`.

### Field change to make this rulable

1. **Delete the eight batch options from `Status`** — Active `…825938`, Stability Pending `…825939`, Hold/Release Review `…825940`, On Hold `…825941`, Released `…825942`, Pulled `…825943`, Expired `…825944`, and the batch sense of Watch. Keep `Watch` `1214660230825936`; it stays as the lab-findings watch state and no longer collides, because the batch sense now lives on `Batch State`.
2. **Delete `Pending`** `1214660230825945`. Migrate its five tasks to `Inbound` (the four open SOP reviews) and `Closed` (the one completed).
3. **Clear `Status` on the seven batch tasks.** `Batch State` already holds the truth.

`Status` then reads: Inbound · Triage · Vendor Flag Review · Scorecard Signaled · CAPA Open · Watch · Closed.

**Target maps — two fields, disjoint section sets, so two independent rule sets:**

| Status | Section |
|---|---|
| Inbound | *no rule — see carve-out* |
| Triage | Lab Findings Open |
| Vendor Flag Review | Vendor Flag Review |
| Scorecard Signaled | Scorecard Signal Posted |
| CAPA Open | CAPA Handed Off |
| Watch | Watch List |
| Closed | Closed |

| Batch State | Section |
|---|---|
| Active | Batch — Active in Market |
| Stability Pending | Batch — Stability Schedule |
| Watch | Batch — Watch |
| Hold/Release Review | Batch — Hold/Release Review |
| On Hold | Batch — On Hold |
| Released | Batch — Closed (Released, Expired, Pulled) |
| Pulled | Batch — Closed (Released, Expired, Pulled) |
| Expired | Batch — Closed (Released, Expired, Pulled) |

**The `Inbound` carve-out.** `Status = Inbound` gets no rule, because two sections are legitimate landing homes: `Inbound Staging` for lab findings and bridge intake, `Cross-cutting Tasks` for audits, SOP reviews and retailer questionnaires. The creating skill picks; a rule cannot tell them apart from Status alone. Same shape as the `SAE Open` / `Recall Open` carve-out on SJ Skin Complaint Log — and the same reason rules must key on specific option GIDs rather than "any Status change."

`Running Log` and `SOP Catalog` also take no rule; they are pinned non-workflow sections.

**Migration:** 12 writes total. Clear `Status` on the seven batch tasks, and move five `Pending` tasks to `Inbound` or `Closed`. Everything else is already consistent, because 80 of 95 tasks carry no state to migrate.

## SJS CAPA Log — `1214660784338465`

**State field:** `Status` — `1214660230826043` · **Authority:** Status (already declared) · **Rule owns movement:** no — **pending the field change specced below**

| Section | GID |
|---|---|
| Untitled section | `1214660784338484` |
| Inbound Staging | `1214660787315994` |
| NCR Open | `1214660437005110` |
| NCR Review | `1214660784313594` |
| Investigation | `1214660784327635` |
| Action Plan | `1214660784311642` |
| Implementation | `1214660436871510` |
| Verification | `1214660784329421` |
| Effectiveness Review | `1214660787347574` |
| CAPA Open | `1214660787241932` |
| NCR Closed (No CAPA) | `1214661452224011` |
| Closed | `1214660436972438` |

| Status | Option GID | Section |
|---|---|---|
| Inbound | `1214660230826044` | Inbound Staging |
| NCR Review | `1214660230826045` | NCR Review |
| Investigation | `1214660230826046` | Investigation |
| Action Plan | `1214660230826047` | Action Plan |
| Implementation | `1214660230826048` | Implementation |
| Verification & Effectiveness | `1214660230826049` | Verification |
| Closed | `1214660230826050` | Closed |
| Closed-No-CAPA | `1214660230826051` | NCR Closed (No CAPA) |

12 sections against 8 options, so the map is not onto: `NCR Open`, `CAPA Open`, `Effectiveness Review` and `Untitled section` have no Status value pointing at them. `capa-coordinator/SKILL.md:173` already says the two are "loosely coupled" and that Status is what operators query — consistent with the authority rule. `Verification & Effectiveness` covering both the `Verification` and `Effectiveness Review` sections is the ambiguity that blocks a rule.

`Source` carries **12 options** live — the nine `capa-coordinator` documents plus `vendor-systemic` `1214660230825968`, `batch-pattern` `1214660230825969` and `COA-mismatch` `1214660230825970`. Full set: complaint-trend `…826060` · lab-OOS `…825965` · lab-OOT `…825966` · vendor-receipt `…825967` · vendor-systemic · batch-pattern · COA-mismatch · process-deviation `…826057` · audit-finding `…826058` · regulatory-observation `…826059` · internal-flag `…825971` · direct-open `…825972`.

### Field change to make this rulable

**Do it now: the queue holds one task, and that task has a null Status.** Zero tasks carry `Verification & Effectiveness`, so there is no migration — the split is a pure rename plus an add. Verified live 2026-08-01: `num_tasks: 1`, and the one task is `[SOP Revision Pending — quality-manager]` in Inbound Staging, a cross-skill staging item that never enters the CAPA phase machine.

Four UI edits, in this order:

1. **Rename** Status option `Verification & Effectiveness` — `1214660230826049` — to **`Verification`**. Rename, do not delete; the GID is cited in `capa-coordinator` and keeping it means no option GID churn.
2. **Add** Status option **`Effectiveness`**, positioned directly after `Verification`. Record its new GID here on creation.
3. **Add** Status option **`NCR Open`**, positioned directly after `Inbound` — the `NCR Open` section is currently unreachable by field.
4. **Delete** the sections **`CAPA Open`** `1214660787241932` and **`Untitled section`** `1214660784338484`.

`CAPA Open` is deleted rather than given a Status value because it is not a phase — it is the union of Investigation, Action Plan, Implementation, Verification and Effectiveness. Any task in one of those phases is also "CAPA open," so a rule keyed on Status could never choose between them. What actually distinguishes a CAPA from an NCR is the `CAPA Number` field being populated, which is already how `capa-coordinator` tracks conversion. Keeping the section guarantees the ambiguity; deleting it costs nothing, since no task sits there.

**Target map — 10 options, 10 sections, one-to-one:**

| Status | Section |
|---|---|
| Inbound | Inbound Staging |
| NCR Open *(new)* | NCR Open |
| NCR Review | NCR Review |
| Investigation | Investigation |
| Action Plan | Action Plan |
| Implementation | Implementation |
| Verification *(renamed)* | Verification |
| Effectiveness *(new)* | Effectiveness Review |
| Closed | Closed |
| Closed-No-CAPA | NCR Closed (No CAPA) |

Once the four edits land, this queue is rulable: ten rules, trigger *Status changes to X* → action *move to section Y*. Same caveats as Purchasing — bind the field by GID `1214660230826043`, not by picking "Status" from a dropdown, and stop `capa-coordinator` from issuing section moves only after a dry run confirms the rule fires.

## SJ Skin Complaint Log — `1204763097184846`

**State field:** `Status` — `1214660230826220` · **Authority:** Status (declared) · **Rule owns movement:** yes (candidate)

| Section | GID |
|---|---|
| New feedback | `1204763097184848` |
| Backlog | `1204763097184852` |
| Actioning | `1204763097184853` |
| Not actioning | `1204763097184854` |
| Completed | `1204763097184855` |

| Status | Option GID | Section |
|---|---|---|
| New | `1214660230826221` | New feedback |
| Backlog | `1214660230826222` | Backlog |
| Actioning | `1214660230826223` | Actioning |
| Not Actioning | `1214660230826224` | Not actioning |
| Completed | `1214660230826227` | Completed |
| SAE Open | `1214660230826225` | *no move — orthogonal* |
| Recall Open | `1214660230826226` | *no move — orthogonal* |

`complaint-and-event-handler/SKILL.md:133` states the last two are orthogonal by design: an SAE can be in flight while the task sits in Actioning. **A rule on this queue must exclude them**, or triggering SAE Open would move a task out of its real section. This is the clearest illustration of why rules key on specific option GIDs rather than "any Status change."

Section GIDs are recorded here for the first time — `complaint-and-event-handler/SKILL.md:130` lists the names with no GIDs. Casing differs between field and section (`New` vs `New feedback`, `Not Actioning` vs `Not actioning`), so match by GID, never by name.

## SJS Regulatory Management — `1214660807386611`

**State field:** none · **Authority:** section + Gate (declared) · **Rule owns movement:** no

| Section | GID |
|---|---|
| Inbound Staging | `1214661463988658` |
| In Pedrero Review | `1214661463988659` |
| Returned — Action Required | `1214661463988660` |
| Active / In-Effect | `1214661463988661` |
| Renewal Window | `1214661463988662` |
| Closed | `1214661463988663` |
| Registrations — Active | `1214660230826186` |
| Registrations — Renewal Window | `1214660230826187` |
| Pedrero Liaison | `1214660230826188` |
| Cross-Skill Dashboard | `1214660230826189` |

Confirmed live: **there is no Status field on this project.** `regulatory-manager/SKILL.md:175-176` instructs writing `Status = Inbound Staging` and `Status = In Pedrero Review` — those are section names being written to a field that does not exist. `references/canada-compliance.md:86` has it right with an arrow instead. The sections are the state machine.

## SJS Reportable Events — `1214660834583706`

**State field:** none · **Authority:** section + Gate (declared) · **Rule owns movement:** no

| Section | GID |
|---|---|
| Untitled section | `1214660834583725` |
| Inbound Staging | `1214660834583732` |
| In Pedrero Review | `1214660256599187` |
| Returned — Action Required | `1214660256599188` |
| Submitted to Agency | `1214660256599189` |
| Awaiting Agency Response | `1214660256599190` |
| Closed | `1214660256599191` |

`Event Type` and `Agency` classify; `Gate` holds HITL state. The six working sections are the sequence.

---

## Shared fields across queues

`Gate` — `1214660230825947` — is one field attached to CAPA Log, Quality Management, Regulatory Management and Reportable Events. Options: Open `1214660230825948` · Pending Operator `1214660230825949` · Pending QA Lead `1214660230825950` · Pending Regulatory Lead `1214660230826118`. Per the 2026-07-30 decision, `Pending QA Lead` resolves to Nicole for process-shaped gates; the label is retained in Asana.

`Linked SKU` `1214660230826031`, `Linked Batch` `1214660230826027`, `PLM Link` `1214370303255301`, `SKU` `1213879801597825`, `Severity` `1214660230825959`, `Source` `1214660230825964`, `Closeout Summary` and `Window End` are likewise shared across projects. A field GID appearing on two projects is the same field with the same options — unlike same-*named* fields, which are not (see below).

**Same name, different field.** `Status` exists as five unrelated fields: Purchasing `1214373372406268`, Inventory `1214374252744527`, Quality `1214660437047242`, CAPA `1214660230826043`, Complaint `1214660230826220`. Disjoint option sets. Resolve by GID; never by name.

---

## Asana Rules to build

None exist today — verified 2026-07-31, every section move in this system is a skill calling `update_tasks`. These have to be created in the Asana UI; the MCP cannot create them.

**Rules move sections. Nothing else.** No completion action, no assignee change, no comment, no due date. Section placement is per-project, so a rule moving a task in one queue does not disturb where it sits in another. Completion is task-global — ticking it closes the task in every project it is multi-homed into, and a rule cannot see whether the other homes are finished. See `asana_task_contract.md` Phase 4.

**Build first — AC Brands Purchasing.** One rule per row of its state → section map above: trigger *Status changes to X*, action *move to section Y*. Ten rules, or one rule with ten branches if the UI supports it.

Before building:

- **Confirm the workspace plan supports custom-field-triggered rules.** Asana gates rule triggers by tier. This is a UI check; the API does not answer it.
- **Pick the field on the right project.** Choosing "Status" from a dropdown can silently bind the wrong one of the five above.
- **A skill writing Status fires the rule.** That is the intent. It also means `purchasing-manager` must stop issuing section moves for this queue once the rule is live, or the two writers will fight and last-write-wins.

Sequencing: build the rule, dry-run it on a throwaway task (set Status to `Received`, confirm it lands in Receiving), and only then remove the section-move calls from `purchasing-manager`. Do not do both at once — a half-migrated queue with neither writer moving sections is worse than the current state.

**SJ Skin Complaint Log** is the next best candidate: a clean 5-row map, with the mandatory carve-out that `SAE Open` and `Recall Open` trigger no move.

### Build order, cheapest first

Each of the three below needs a field edit before its rules can be built. All three specs are in their queue's section above, and all three are cheap for the same reason: the state field is barely used, so there is almost nothing to migrate. That will stop being true as these queues fill, which is the argument for doing them now.

| Order | Queue | UI edits | Tasks to migrate | Result |
|---|---|---|---|---|
| 1 | SJS CAPA Log | 2 renames/adds, 1 add, 2 section deletes | **0** | 10 options → 10 sections, 1:1 |
| 2 | SJS Quality Management | 9 option deletes | 12 | two fields, disjoint sections, 13 rules |
| 3 | AC Brands Inventory | re-option one field | ~38, all mechanical | 7 options → 5 sections |

Quality is second rather than last because it needs no new field — `Batch State` already exists and is already authoritative in practice. Inventory is last because its migration is the largest, not because it is hard.

| 4 | Sweet July Skin Logistics | add 1 field, 2 renames, 5 adds, 3 deletes | 6 | 7 options → 7 sections, 1:1 |

Logistics is last because it is the only structural change — sections get rebuilt around position and direction moves to a new field. Decided 2026-08-01; see that queue's section for the full spec.

**Not rulable, and not a gap:** Regulatory Management, Reportable Events, S&OP, OC3PL and SJ Shipping Dashboard have no state field to trigger on and are declared section-as-state.

---

## Drift found while pulling this

Recorded because each is a place a skill body disagrees with the live workspace.

**Cleared 2026-08-01.** Every item below is now fixed in the skill bodies. The two that were live bugs rather than stale text: `regulatory-manager` was writing a `Status` field onto a project that has none, so those writes were failing; and eight skills pointed at `asana-field-gids.md` on a local Mac path that no session or Routine can open, which is why the GIDs got copied into skill bodies and drifted. Both now resolve to this file. Kept as a record of what was wrong and where to look if it recurs.

- **`inventory-manager/SKILL.md:130-132`** claims its project is "AC Brands Ops Dashboard (GID to be confirmed on first run)" with a "single section, no subsections" and "no custom fields." Live: `AC Brands Inventory` `1214374368959019`, five sections, three fields. `gids.md:109-113` marks AC Brands Ops Dashboard archived, "do not route to."
- **`purchasing-manager/SKILL.md:277`** lists an `Untitled section` `1214373372406252`. Not present live — deleted since.
- **`complaint-and-event-handler/SKILL.md:130`** documents its five sections with no GIDs. Now recorded above.
- **`capa-coordinator/SKILL.md:161-171`** documents 11 sections; live has 12.
- **`claims-il-and-label-keeper/SKILL.md:149-154`** documents 6 sections for SJS Regulatory Management; live has 10, matching `regulatory-manager/SKILL.md:261-270`.
- **`regulatory-manager/SKILL.md:175-176`** writes Status values on a project with no Status field.
- **`gids.md:214`** lists a Quality `Pending` option no skill documents. Confirmed live.
- **`supply-demand-planner`** section is `Monthly run` live, `Monthly Run` in `asana-s-and-op-schema.md:11,116`.
- **Untitled sections** survive live on S&OP `1214347479282072`, CAPA Log `1214660784338484` and Reportable Events `1214660834583725`. Harmless as long as nothing routes to them, but they are where a task lands when a section resolve fails.
