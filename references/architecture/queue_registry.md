# Asana queue registry

**Use:** The one place that records, per Asana queue, its project GID, its sections, its state field, and the **state → section map**. Skills read this instead of hard-coding section GIDs into their own bodies. Where a queue declares an Asana Rule owns section movement, skills write the state field only and never issue a section move.

**Scope:** The eleven queues named in `bridge_queue_contract.md`. Companion to `asana_task_contract.md` (what a write looks like) and `bridge_queue_contract.md` (which queue a task belongs to). This file answers *where inside the queue a task sits, and why*.

**Pulled live:** 2026-07-31, via `get_project` with `include_sections` and `custom_field_settings`. Every GID below came from the API, not from a skill body — several skill bodies were already stale (see Drift found, at the end).

**Last updated:** 2026-07-31 — Authored. Closes the gap Alvin found: a PO could reach `Status = Received` with no rule moving it out of `POs In Flight`, because no state → section map existed in any file, for any queue.

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

A `Status` field exists — `1214374252744527` — but its options are `Pending Review` / `Approved` / `In Progress` / `On Hold` / `Closed` / `Cancelled`: a generic approval vocabulary that describes none of this queue's actual states. `inventory-manager` carries state in title prefixes instead (`SKILL.md:139-149`: `[Receive]`, `[Low Stock]`, `[Position Variance]`, …). Treat the field as a leftover, not a state field. **No state → section map is possible until the field is re-optioned to match the work types** — flagged, not fixed here.

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

Live section name is **`Monthly run`**, lowercase r. `asana-s-and-op-schema.md:11,116` writes `Monthly Run` — a literal name match fails.

## Sweet July Skin Logistics — `1214370420013442`

**State field:** `Shipment Status` — `1214374904674302` · **Authority:** Status · **Rule owns movement:** no (map incomplete)

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

**No state → section map can be written yet, and this is a genuine design gap rather than a declared exception.** Sections here split by *direction and cargo type* (inbound FG vs inbound components vs outbound) while Shipment Status splits by *position in transit*. The two axes are independent: a Pre-Ship inbound component shipment and an In Transit one both belong in `Inbound — Components`. So status alone cannot pick the section — direction is needed too, and `logistics-manager` never states the combined rule despite `SKILL.md:330` saying "advance the section."

Two rows are unambiguous and can be ruled today if wanted: `Exception → Outbound — Escalations` (already the practice at `oc3pl-order-manager/SKILL.md:382`) and `In Clearance → Customs Watch`. `At Port` is ambiguous — the section order implies destination port, the name does not.

Resolving this needs a decision on whether inbound and outbound get separate status fields, or sections get restructured by position instead of direction. Out of scope for this pass; recorded so it is not mistaken for an oversight.

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

The `Status` field carries **15 options spanning two unrelated workflows** — lab findings (Inbound, Triage, Vendor Flag Review, Scorecard Signaled, CAPA Open, Watch, Closed) and batch lifecycle (Active, Stability Pending, Hold/Release Review, On Hold, Released, Pulled, Expired), plus `Pending`. A single rule keyed on this field cannot serve both, since `On Hold` and `Closed` mean different sections depending on which workflow the task belongs to. Splitting the field is the prerequisite for ruling this queue. Out of scope for this pass.

Also live: option `Pending` `1214660230825945`, which appears in no skill's documented option list.

## SJS CAPA Log — `1214660784338465`

**State field:** `Status` — `1214660230826043` · **Authority:** Status (already declared) · **Rule owns movement:** no

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

12 sections against 8 options, so the map is not onto: `NCR Open`, `CAPA Open`, `Effectiveness Review` and `Untitled section` have no Status value pointing at them. `capa-coordinator/SKILL.md:173` already says the two are "loosely coupled" and that Status is what operators query — consistent with the authority rule. `Verification & Effectiveness` covering both the `Verification` and `Effectiveness Review` sections is the ambiguity to resolve before ruling this queue.

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

**Not rulable yet:** Quality Management (one field, two workflows), CAPA Log (`Verification & Effectiveness` spans two sections), Logistics (status and sections are independent axes), Inventory (Status options describe nothing). Regulatory Management, Reportable Events, S&OP, OC3PL and SJ Shipping Dashboard have no state field to trigger on.

---

## Drift found while pulling this

Recorded because each is a place a skill body disagrees with the live workspace. Fixed in this pass where the plan scoped it; otherwise listed for follow-up.

- **`inventory-manager/SKILL.md:130-132`** claims its project is "AC Brands Ops Dashboard (GID to be confirmed on first run)" with a "single section, no subsections" and "no custom fields." Live: `AC Brands Inventory` `1214374368959019`, five sections, three fields. `gids.md:109-113` marks AC Brands Ops Dashboard archived, "do not route to."
- **`purchasing-manager/SKILL.md:277`** lists an `Untitled section` `1214373372406252`. Not present live — deleted since.
- **`complaint-and-event-handler/SKILL.md:130`** documents its five sections with no GIDs. Now recorded above.
- **`capa-coordinator/SKILL.md:161-171`** documents 11 sections; live has 12.
- **`claims-il-and-label-keeper/SKILL.md:149-154`** documents 6 sections for SJS Regulatory Management; live has 10, matching `regulatory-manager/SKILL.md:261-270`.
- **`regulatory-manager/SKILL.md:175-176`** writes Status values on a project with no Status field.
- **`gids.md:214`** lists a Quality `Pending` option no skill documents. Confirmed live.
- **`supply-demand-planner`** section is `Monthly run` live, `Monthly Run` in `asana-s-and-op-schema.md:11,116`.
- **Untitled sections** survive live on S&OP `1214347479282072`, CAPA Log `1214660784338484` and Reportable Events `1214660834583725`. Harmless as long as nothing routes to them, but they are where a task lands when a section resolve fails.
