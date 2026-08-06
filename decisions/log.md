# Decisions Log

Append-only record of meaningful decisions and why they were made. `/level-up` Phase 2 (Method interview) writes scoped automation specs here. You can also append manually whenever you decide something worth remembering.

**Format per entry:**

```
## YYYY-MM-DD — Short title

**Decision:** what was decided.

**Why:** the reasoning, constraints, and what would change your mind.

**Alternatives considered:** what else was on the table.

**Owner:** who's accountable.
```

Keep it terse. Future-you will thank present-you for capturing the *why*, not just the *what*.

---

## 2026-04-29 — Skills system: migrate from per-skill duplication to shared architecture (Phase 0, settled)

**Decision:** Adopt a master-router + shared-canonical-file architecture for the Sweet July Skin skills system instead of every skill hardcoding its own copy of team names, GIDs, product lists, style rules, and SOP text. `sjs-master` (brand-level) and system routers (`sjs-pd-system`, `sjs-ops-system`, `sjs-quality-system`, `sjs-regulatory-system`) hold no domain data themselves — they route, and canonical facts live in shared files or PLM.

**Why:** Duplicated facts drift. A product list hardcoded in 4 different skills goes stale in 3 of them the moment it changes in the 4th. Centralizing means one skill (or the PLM live-read) is the single place a fact changes, and every consumer benefits automatically.

**Alternatives considered:** Leave each skill self-contained (simpler per-skill, but the audit that triggered this decision found stale product lists, inconsistent skill counts, and contradictory brand specs across skills from exactly this problem).

**Owner:** Alvin.

**Status:** PD and Ops phases (3, 4, 5, 8 in the original tracker) stalled after Quality and Regulatory got the full treatment — bandwidth, not a priority call. See `decisions/skills-architecture-tracker.md` for the full phase-by-phase backlog; picking this back up counts as direct progress on the "build out the AI-assisted skill/agent system" Q3 priority, not separate overhead.

---

## 2026-07-19 — Consolidate skills system into SJ-OS as the single architecture root

**Decision:** SJ-OS absorbs the entire skill system going forward — not just a thin index pointing at it. Cross-system canonical files that lived alongside `sjs-master` (system_map, gids, style_rules, tool_patterns, bridge_queue_contract, automations, daily recap + Monday briefing specs) moved to `references/architecture/` at the SJ-OS repo root. The migration tracker (`sjs-master/AUDIT_TRACKER.md`) moved to `decisions/skills-architecture-tracker.md` as the living backlog for finishing this work.

**Why:** The skills, the scheduled Routines that run them, and the AIOS shell (context/connections/decisions) were three things in one repo that didn't know about each other. SJ-OS is meant to be the operating system for the brand, built for succession — that only works if the deep operational knowledge actually lives where the AIOS's own Context layer can see it, not three folders deep inside one router skill.

**Alternatives considered:** Leave `references/architecture/` living inside `sjs-master/` and just link to it from SJ-OS root. Rejected — doesn't hold up as headcount grows past one operator; the whole point of absorbing is one place to look, not a pointer to another place to look.

**Owner:** Alvin.

**Status:** System-specific canonical files (Quality's role-map/SOP catalog, Regulatory's role-map/partner contacts, etc.) deliberately stayed local to their own skill's `references/` — only genuinely cross-system facts moved. No live Routine needed to change: scheduled-prompts only hardcode paths to each skill's top-level `SKILL.md`, and the deeper file reads are driven by `SKILL.md` content, which Routines re-read fresh on every clone.

---
## 2026-07-17 — Retire the Ops Coordinator role; hire two specialists instead

**Decision:** Ciarra Robinson's Operations Coordinator role is retired rather than backfilled — a role redesign, not a performance-out. It's replaced by two new specialist roles: an **Operations Specialist** and a **Product Development Project Manager Specialist**, both reporting to Nicole. In the interim, Alvin and Nicole split her work — Alvin takes inventory and logistics, Nicole takes order management and OC3PL.

**Why:** One generalist coordinator seat was covering inventory, logistics, order management, and OC3PL at once, which is two specialties wearing one hat and no depth in either. Splitting the seat is what lets each half get owned properly, and it lines up with this quarter's stated hiring priority in `context/priorities.md`. Both roles reporting to Nicole rather than Alvin also moves day-to-day ops management off the VP seat, which is the succession point this whole system is being built for.

**Alternatives considered:** Backfill the coordinator role as-is — rejected, it recreates the same too-broad seat. Absorb the work permanently between Alvin and Nicole with no hires — rejected, it's the current interim state and it doesn't scale past the two of them.

**Owner:** Alvin, with Nicole on the two new roles once filled.

**Status:** Ciarra departed as of 2026-07 (earlier than the "end of August" target set on 7/17). Interim split is live. Repo-side cleanup done 2026-07-29 — `role-map.md` seat marked vacant with the interim split, her address removed from the `ac-brands-holiday-comms` BCC list, and her name cleared from the bridge people lists, PD system roster, comp-intel ownership, and the Ayesha briefing's OC3PL read. Two items still open: 22 of her Asana tasks sit unassigned in a holding project (`1216923783441065`), 4 already overdue, and her `contact/ciarra-robinson` wiki page still reads as an active internal contact, so the bridges' run-time lexicon will keep resolving her as internal until it's updated.

**Logged late.** The 2026-07-17 `fireflies-asana-bridge` eval run captured this decision from the SJS Builder Session and flagged it for the log; it was never written up. Surfaced again 2026-07-29 when the role map's stale row broke collaborator resolution during the task-write-contract build.

---
## 2026-07-29 — PLM is runtime truth when the three SOP surfaces disagree

**Decision:** Any SOP fact lives on three surfaces — `quality-manager/references/sop-catalog.md` in the repo, `sop_documents` in PLM, and a `sop/` page in the wiki. When they disagree, **PLM is runtime truth**: fix the repo catalog to match, then confirm the wiki page exists. A change that lands on one surface and not the other two is the defect, not a difference of opinion.

**Why:** A wiki-layer audit found four separate instances of exactly this drift. SKN-OPS-005 was ratified in the repo on 2026-05-09 and had no PLM row and no wiki page at all, so for eleven weeks the runtime catalog couldn't answer "current revision of SKN-OPS-005" while every NCR cited it. SKN-OPS-008 sat at Rev 1.0 in the repo against Rev 2.0 in PLM. `next_review_date` was NULL on all 13 PLM rows, so quality-manager's annual-review sweep had nothing to fire on — nine SOPs and forms are now showing 29 days overdue once the dates were restored. Four skills still described ratified SOPs as working drafts. Skills read PLM at run time and the repo only when a human opens it, so PLM being authoritative matches how the system actually behaves.

**Alternatives considered:** Make the repo catalog authoritative — rejected, it's the surface nothing reads at run time. Collapse to one surface and drop the others — rejected for now; the repo file is what a human reviews and the wiki page is what the bridges' lexicon loads, so all three earn their place. Revisit if drift recurs.

**Owner:** Alvin. Quality-side SOP changes route through quality-manager.

**Status:** All four drift instances fixed 2026-07-29. Full findings in `decisions/wiki-layer-audit-2026-07-29.md`. Two items left open there — Job 0 (the bridges' wiki write-back) has not fired since 2026-05-26, leaving 123 of 133 pages as untouched seed; and `Bridge-and-System-Audit-2026-05-26.md` is cited from three files but exists nowhere, most likely lost in the 2026-07-19 consolidation.

---
## 2026-08-06 — Every activity carries a description and a worked example

**Decision:** Clicking an activity on the RACI page opens a drawer describing what the work actually is, with a concrete example, the full A/R/C/I list by name and title, why it sits there, and the source citation. All 102 activities are covered. The text lives in `deliverables/activity_notes.py` and `verify.py` fails if a row loses its breakdown or a breakdown loses its row.

**Why:** Alvin's call, and the gap was real. A RACI answers who owns a thing and says nothing about what the thing is. Half the rows on this matrix are named in vocabulary that only makes sense if you were in the room: reformulation claim bridge, UBM cohort positioning, three-way reconciliation, OOS versus OOT. Handing that to Danielle and Nicole, and later to two new hires, meant handing over a document that needs a translator. The examples matter more than the definitions, because "acknowledgement variance" becomes obvious the moment you read a case where the vendor confirms a different price and date than you ordered.

It also makes the matrix usable as an onboarding artifact rather than only a resourcing one. The two specialists arrive into 34 transitioning rows, and this is what tells them what those rows mean.

**Alternatives considered:** Tooltips on hover. Rejected, no room for an example and useless on touch. A separate glossary document. Rejected, it separates the definition from the assignment so both go stale independently. Generating descriptions from the skill files at build time. Rejected, the skills describe how the automation works rather than what the activity is, and several activities have no skill at all; the marketing, wholesale and web rows are exactly the ones that most needed explaining.

**Status:** Shipped 2026-08-06. The drawer replaced the per-row source disclosure, which showed a file path and nothing else. Verified inside a sandboxed iframe: 102 triggers, sections render in order, focus moves to Close on open and returns to the activity on dismiss, Escape and scrim both close, tab focus stays in the panel, body scroll locks, mobile renders as a bottom sheet, edit mode keeps the activity as editable text rather than a trigger, and a hand-added row says it has no breakdown yet. `PUB["version"]` stayed at v7 so local edits survived. All eight verify checks pass.

**Open:** The breakdowns are written from the repo and from how the work actually runs, so they are mine rather than sourced to a procedure. Worth Nicole reading the Quality and Regulatory ones and Soraya the Marketing ones, since a wrong description is more misleading than a missing one.

---
## 2026-08-05 — No browser modals in the artifact frame

**Decision:** The RACI page uses no `confirm`, `prompt` or `alert`. Destructive actions act immediately and offer Undo on the toast; anything that needed text input uses an inline field. `deliverables/README.md` records the rule so a future edit does not reintroduce them.

**Why:** Alvin reported delete not working. The artifact frame is sandboxed without the `allow-modals` keyword, so the browser ignores `confirm()` and returns false, and ignores `prompt()` and returns null, logging only a console warning. Delete was guarded by `if(!confirm(...)) return`, so it always bailed. The same root cause had silently broken **Revert to published** and **Add function**, neither of which had been reported yet. One symptom, three dead controls.

The testing lesson is the more useful half. Every earlier round was driven against a `file://` open of the page, where modals work normally, so all three controls passed. Verifying inside a sandboxed iframe is what reproduced it, and that is now how this page gets tested.

**Alternatives considered:** Ask for `allow-modals`. Not available to declare, and modal dialogs are the wrong pattern for a page people edit live in a meeting. Build a custom modal overlay for confirmation. Rejected as more machinery than the job needs; an immediate action with Undo is fewer clicks and more forgiving than a dialog, because it does not make you decide before you can see the result.

**Status:** Shipped 2026-08-05. Delete removes the row and offers Undo, which restores it at its original index. Revert snapshots the edited copy first and offers Undo, so the button can no longer destroy a session's work outright. Add function opens an inline field with Enter to commit, Escape to cancel, and duplicate names rejected by name. Verified inside a sandboxed iframe rather than a bare file open. `PUB["version"]` deliberately left at v7 so viewers holding local edits keep them across the republish.

**Open:** Nothing on this page relies on a modal now. Worth remembering for anything else published as an artifact: the sandbox also blocks the `beforeunload` prompt, so the unsaved-changes guard on this page is decorative rather than real. Export is the only durable save.

---
## 2026-08-05 — More than one A is allowed; R is single and cannot be taken by accident

**Decision:** An activity can have several positions accountable. Taking A displaces nobody. R stays single, sits last in the cell cycle, and cycling can never move it off its holder: if R is already held on that activity the cycle steps over R and names the holder, so clearing their cell is the only way to move it. Shift-click steps the cycle backwards.

This replaces the exactly-one-A rule that the original RACI brief set. Two restrictions are unchanged: an open seat can hold only the transition arrow, and a partner organisation can hold R but never A.

**Why:** Alvin's call, and both halves came out of using the thing. Shared accountability is real on this team, so a matrix that forces a single A was making him pick a winner where two people genuinely answer together. The ordering was a straight defect: R sat mid-cycle, so clicking a cell towards C, I or A passed through R and silently pulled R off whichever position held it on that row, wrecking selections elsewhere. Ordering alone was not enough, because a full lap back to blank still crosses R. Refusing to move R by cycling is what actually makes clicking safe.

**Alternatives considered:** Keep one A and add a second column for co-owners. Rejected, it encodes the same ambiguity the RACI is meant to remove and nobody would read the second column. Let R be multi as well. Rejected, R is who does the work and splitting it is how a task ends up done by nobody; the A/R flag on the Gaps sheet only means something while R is single. Let cycling steal R but announce it, which is what shipped first. Rejected after using it: a toast does not undo a change you did not want, and the whole complaint was edits leaking into cells he was not looking at.

**Status:** Shipped 2026-08-05. The page carries A as a list. `deliverables/raci_rows.py` still holds one code per row because that is what today's data says, but `build_raci.py` accepts a code or a list, and `verify.py` now checks for at least one A and exactly one R and reports how many rows carry more than one. So an export with shared A folds back in without another schema change. Proved the tolerance with a temporary two-A row: both positions get an A marker in the spreadsheet. Verified in Chromium: cycle order is C, I, A, R, blank; four positions held A on one row at once with tallies tracking; R untouched throughout; R settable once its slot is free; existing A/R cells still render and clear in one click; open-seat and partner limits intact; edits survive a reload.

**Correction, same day.** Making A a set removed A/R from the cycle, so it could no longer be set by hand. Restored: the cycle is blank, C, I, A, A/R, R. Both A/R and R claim R, so both sit at the end and both are skipped when another position holds R, with the toast naming the holder. A/R and a separate A can coexist on one activity, which is a shape the old one-A rule could not express at all.

**Open:** The A/R count in the banner still reads "same person on A and R" per row, which is literally true but means less now that a row can carry other A's alongside. If shared A becomes common, the single-point-of-failure measure on the Gaps sheet needs rethinking, since it was written when one A per row was guaranteed.

---
## 2026-08-04 — The RACI page is the editing surface, and the repo is still the source of truth

**Decision:** The team-facing RACI page becomes editable in the browser. Cells cycle through blank, C, I, R and A; activity and function names are editable; rows can be reordered, moved between functions, added and deleted; functions can be added. The page is now client-rendered from a JSON payload instead of static markup, which is what makes any of that possible.

Two things stay put. The **repo is still the source of truth**: `deliverables/raci_rows.py` is what the spreadsheet, the summary and the page are all generated from, and a change is only real once it lands there. And the **three data invariants are enforced in the editor**, not just in `verify.py`: one A and one R per activity, with the page naming whoever just lost a letter; open seats can hold only the transition arrow, because a vacancy cannot be accountable; partner organisations can hold R but never A, because accountability does not leave the company. A row left without an A or an R is flagged and counted rather than silently accepted.

**Why:** Every change so far has come back through Claude, which makes a five-second correction cost a whole session. The people who spot a wrong cell are the people in the meeting looking at it. Letting them make the change where they see it is the point, and enforcing the invariants in the editor means the shape of a RACI survives contact with people who have not read the framework.

**Alternatives considered:** Make the spreadsheet the only editing surface. Rejected, not because it cannot be edited but because it is the artifact nobody opens in a meeting, and edits there are just as unshared while losing the invariant checks. Wire the page to write back to the repo directly. Rejected for now: it needs credentials in a page anyone with the link can open, and the review step before a change becomes canonical is worth keeping. Let the page write to shared storage so the team edits one copy together. Not available: the account has `downloads` and `mcp` runtime capabilities and no shared-state capability, so this was ruled out by what exists rather than by preference.

**Status:** Shipped 2026-08-04 as v7. Same 102 activities, same owners, same counts. Edits live in each viewer's own browser via `localStorage` keyed to the payload version, survive a reload, are not shared, and can be discarded with Revert to published. Export JSON uses the `downloads` capability with a blob fallback; Copy for Excel puts the matrix on the clipboard as tab-separated text; Import JSON loads an export back in. Verified in Chromium: the cycle order, the A and R displacement messages, the open-seat and partner restrictions, add, delete, reorder, move between functions, persistence across reload, and revert.

**Open:** The round trip is manual. An export has to come back to Alvin to be folded into `raci_rows.py`. If that starts happening often, the next step is a proper write path rather than a page that emails itself. Also worth watching: because local edits are keyed to the payload version, anyone holding local edits will not see a newly published baseline until they revert, so bumping the version is how you force everyone onto new data.

---
## 2026-07-31 — Coastal Interactive on the matrix; nobody blank on a product decision

**Decision:** Two additions after the first RACI merge.

1. **Coastal Interactive is the managed IT service provider** and belongs on the matrix. They hold the higher-level IT and systems work: back-end infrastructure, identity and endpoint management, equipment procurement and onboarding, asset lifecycle. **Alvin is the liaison and accountable**; Coastal is responsible. Three new rows plus consult on connector configuration and on employee onboarding, where they split the work with Calm HR — Calm HR runs the employment side, Coastal runs equipment and accounts.

2. **Perrine and Soraya are never blank on a Product Development row.** Perrine's accountability is unchanged; she was blank on one row (founder brand-line approval) and is now Informed. Soraya was blank on all eight PD rows and is now Informed on every one.

**Why:** Coastal was simply missing — the same failure mode as Ironclad, Calm HR, WITHIN and Teknologics before them, and the fifth time an external party turned out to be doing work the matrix showed as either unowned or absent. Worth naming the pattern: when a function looks thin on this matrix, the first question is whether a partner is missing rather than whether the work is unowned.

On the blanks: a blank cell is ambiguous in a way Informed is not, because blank does not tell you whether the omission was deliberate. Perrine gives technical guidance across PD and should see every product decision even where she holds no gate. Soraya had no formal visibility into any product decision at all, which is wrong for a Marketing Manager who has to launch the thing — marketing needs the PD signal early, and the PD Specialist job description says as much when it describes creative getting launch dates and packaging details early.

**Alternatives considered:** Drop Perrine's accountability on PD entirely and make her consult-only there — raised and then withdrawn in the same breath; her formula and testing gates are genuine technical authority and stay. Fold Coastal's rows into the existing IT rows — rejected, back-end infrastructure and the web storefront are different partners with different accountability (Coastal under Alvin, Teknologics under Danielle) and collapsing them would hide that.

**Owner:** Alvin, as liaison to Coastal Interactive.

**Status:** RACI at 102 activities, 18 columns, 11 IT rows. `references/external-partners.md` extended to nine parties, `connections.md` registers Coastal. All seven verification groups pass.

**Open:** Engagement terms and renewal dates still recorded for Pedrero only — eight partners now need them. The landing hub still shows Finance and Marketing as "Owned by TBD".

---
## 2026-07-31 — Capture the whole business, not just the parts with a skill

**Decision:** Add real Marketing, Retail & Wholesale and Web activities to the RACI, sourced from the AC Brands landing hub rather than the skill suite, and resolve the three functions the hub left unowned.

- **Marketing: Soraya accountable.** Editorial calendar, Klaviyo email, paid media, social content, influencer and earned media, product copy and PDP content, and the WITHIN agency relationship. WITHIN responsible for paid and email execution; Kate for social content; Danielle consulted throughout and retains campaign direction.
- **All channels: Nicole accountable.** DTC, Amazon and wholesale together — Alvin consulted, Danielle informed. Broader than the hub, which split DTC and Amazon to Alvin and left wholesale as "TBD". Picks up wholesale pipeline, retail price architecture and the retailer promo calendar.
- **Web: Danielle accountable, Nicole the systems and tech owner.** Teknologics responsible for development. Erin and Ivy on visual design, Soraya consulted on merchandising and content, Alvin informed.
- **WITHIN and Teknologics added as partner organisations.** Eight external parties now hold execution of eight functions.

**Why:** The matrix was built by extracting ownership from the skill suite, which is the right discipline for anything the system automates and a poor proxy for what the business does. There are no skills for marketing, wholesale or the website, so none of it existed on the matrix — the entire Marketing function was nine rows of competitive intelligence and holiday emails. The landing hub's `data/links.json` is the missing source: it defines the eleven business functions with an explicit `lead` per function, and three read "Owned by TBD". That file is a better answer to "what does this company actually do" than the skill catalogue is, and it should have been read on the first pass.

**Alternatives considered:** Leave marketing and web off until skills exist for them — rejected outright; the RACI's job is to describe the business, and the absence of automation is not the absence of work. Keep DTC and Amazon with Alvin per the hub — rejected in favour of one accountable owner across all channels, so channel economics and retailer commitments do not fragment.

**Owner:** Alvin. Soraya on Marketing, Nicole on channels and the web/digital stack, Danielle on web and finance reporting.

**Status:** Encoded 2026-07-31. RACI at 99 activities, 17 columns, and for the first time **every row has a sourced owner** — no inferred owners remain. `references/external-partners.md` extended to eight parties. `connections.md` now registers the landing hub as the function-map source and lists the four partner organisations. `deliverables/verify.py` resolves citations against both repos.

**Open:** "Nicole is the systems and tech owner" was scoped to the web and digital stack. PLM write path, Asana configuration, landing-hub publish and the 23 scheduled Routines still sit with Alvin — confirm whether that was meant more broadly. Engagement terms and renewal dates are recorded for Pedrero only; the other seven external parties need the same. The landing hub still shows Finance and Marketing as "Owned by TBD" and should be updated to match this decision.

---
## 2026-07-31 — External partners belong on the RACI: Pedrero, Ironclad Finance, Calm HR

**Decision:** Add the three partner organisations that hold execution of a whole function, with accountability split as follows.

1. **Pedrero Regulatory** — external regulatory partner. Already documented in `regulatory-manager/references/pedrero-contacts.md` but absent from the RACI. Consulted on 11 rows, responsible for none, which is the direct consequence of the existing consult-only rule.

2. **Ironclad Finance (Dan Bender)** — runs AP, bookkeeping, payroll, month-end close, reporting, budget consolidation, and inventory valuation into the books. **Accountability splits: Danielle on reporting-side work, Alvin on cost-side work.** Cost sits with Operations because it flows out of purchasing and the inventory ledger, and the vendor-invoice pipeline with its five approval gates is already there.

3. **Calm HR** — PEO and co-employer. Handbook and policy, benefits, payroll processing, onboarding and offboarding, employment compliance, separations, recruiting. **Alvin accountable throughout as liaison; Danielle co-approves** on all of it, matching her presence on every Calm HR thread.

Partners hold R, never A. Accountability stays with an employee on every row, and `deliverables/verify.py` now enforces it.

**Why:** The first RACI pass reported Finance and People & Admin as unowned functions. That was wrong, and the reason it was wrong is instructive — those functions were unowned *in this repo*, not in the business. Ironclad and Calm HR appeared nowhere in SJ-OS, so a matrix built strictly from repo sources could not see them. Extracting rather than assuming is the right discipline and it produced a false negative here, which is worth remembering: absence from the repo means the repo has a gap, not that the work has no owner. Pedrero was documented but only inside one skill's references, so it read as a regulatory implementation detail rather than as one of six external parties the company depends on.

**Alternatives considered:** Keep partners out of the matrix and list them separately — rejected, it hides that three functions have no internal execution capacity, which is exactly what a resourcing conversation needs to see. Give Pedrero R on the regulatory review rows — rejected for now; our own procedures make them consult-only with no system access, so R would misstate who can actually act. That constraint is itself a finding and is on the Gaps sheet.

**Owner:** Alvin. Danielle on finance reporting and as HR co-approver.

**Status:** Encoded 2026-07-31. RACI at 86 activities, 15 columns. `references/external-partners.md` created as the canonical registry — it did not exist, which is the underlying gap. Finance and People & Admin removed from the Gaps sheet as unowned and replaced with resolved rows. Shopify revenue and channel position is now the only genuinely unowned row on the matrix.

**Open:** Continuity across six functions rests on engagements rather than employment — three partner organisations plus Erin, Jan and Perrine. Each is a renewal decision. Engagement terms and renewal dates are confirmed only for Pedrero; Ironclad and Calm HR need the same recorded.

---
## 2026-07-31 — Erin is lead technical authority on packaging; Danielle and Ayesha get real Creative and Marketing roles

**Decision:** Three corrections surfaced while reviewing the RACI.

1. **Erin Hover is a contractor and the lead technical authority on packaging and artwork.** Packaging development, artwork execution and the label artwork archive answer to her, with Jan Haeck executing under her. Perrine consults where formula contact or compatibility is in play. Previously packaging development was accountable to Perrine, which collapsed packaging and formulation into one gate.

2. **Danielle Iturbe holds brand guideline custody and campaign direction**, and is consulted across Creative and Marketing rather than only receiving finished work. Campaign direction did not exist as an activity anywhere, which is why the President had almost no Marketing presence — it is now a row.

3. **Ayesha Curry is consulted wherever the brand carries her name** — brand guidelines, creative direction, campaign direction, claim substantiation, retailer attestations, packaging — and keeps sole accountability for brand-line moves. She was informed-only on most of these.

**Why:** The v2 matrix had Perrine accountable for packaging because the PD role-map bundled "PD / R&D / Quality / Regulatory" into one owner. Packaging is Erin's technical domain and Jan reports to her, so the accountability was in the wrong place. Danielle and Ayesha were structurally absent from Creative and Marketing despite the President managing Soraya and the founder's name being on every product — a RACI that shows the President as informed-only on brand custody is describing something that is not true. The margin sources already had Danielle approving every repricing and channel call, so brand and campaign accountability is consistent with how she already operates.

**Alternatives considered:** Keep packaging with Perrine and add Erin as consult — rejected, it leaves a formulation contractor answering for tooling and deco decisions she does not make. Give Danielle accountability for every Marketing row — rejected, it would move teardowns, the trend digest and social off Soraya, Nicole and Kate, who genuinely own them; consult is the accurate level there. Make Ayesha accountable for brand identity — rejected, Erin holds the craft and Danielle the custody; the founder's input is real but it is consultation, not approval, outside brand-line moves.

**Owner:** Alvin. Erin on packaging and artwork authority; Danielle on brand and campaign.

**Status:** Encoded 2026-07-31. `asana-pd-manager/references/role-map.md` carries the Creative and brand-custody rows; `claims-il-and-label-keeper/references/role-map.md` adds the artwork-authority row and states explicitly that artwork authority and the Reg Lead archive gate are separate people. RACI is at 79 activities.

**Open:** Three of the four holders in the packaging and creative chain are contractors — Erin, Jan and Perrine — and between them they hold accountability for 11 activities. On creative direction Erin is both accountable and responsible with no internal counterpart, same shape as Perrine on stability and RIPT. Neither specialist job description covers creative or formulation authority, so the two approved hires do not close this. It is on the RACI Gaps sheet and is not currently on the hiring plan.

---
## 2026-07-30 — Quality gets a gate: Nicole owns quality control, Perrine advises, Ops Specialist hires first

**Decision:** Three changes out of the leadership business review with Danielle and Nicole.

1. **Nicole Iturbe is the primary quality control owner.** Anything related to quality of product or quality of documentation goes through her as the final quality check, across every function. Each function still owns its own work — the gate sits on top of it, not instead of it. She also calls out inconsistencies in product quality or documentation wherever they surface. Verbatim from the recording: *"with Nicole taking the primary focus on the quality management side of things with quality control... anything related to quality of service or quality of product will go through, you know, Nicole's eyes as sort of that final quality check... Even with each function having or being the primary owner, we'll still have that quality gate just to make sure all of our I's are dotted and T's across."*

2. **Alvin owns the overall framework.** The quality management system itself, the SOP framework, and the RACI. Nicole runs the system inside it. A monthly quality-trend review is the reporting layer that makes the gate useful — a single complaint is noise, a pattern across a quarter is a decision input (the pump defect was the worked example: repeated failures should force a packaging reconsideration). Target: implemented by end of Q3.

3. **Perrine Calvet moves from owner to technical advisor.** She provides guidance on R&D, Quality, Production and Regulatory *requirements for product*. She keeps decision authority where the judgment is genuinely technical — formula stage-gate, compatibility / stability / RIPT / PET, in-market stability testing, packaging development, reformulation direction — and becomes consult-only on everything process-shaped: CAPA lifecycle, batch hold and release, vendor flags, lab-finding classification, SOP ratification, regulatory filings.

4. **Hiring sequence: Operations Specialist first, PD Specialist phased in after.** Both still report to Nicole per the 2026-07-17 decision and the 2026-07-27 proposal. Danielle: *"we're going to prioritize the operations... Specialist... and then as we work through exactly, you know, sort of redefining what this PD help is going to look like and how that's going to function, that will come after."* The PD role is scoped as project management and accountability — *"air traffic control, holding people accountable"* — not strategy or ideation.

**Why:** Quality was structurally owner-less. The role-map named Perrine as QA Lead holding every technical gate, but Danielle's read was that there were things the team had assumed Perrine would manage or organize that she does not, and that leadership needs to be able to override her sign-off — *"even if Perrine is submitting an approval, if we need to pull the plug, we can pull the plug."* Treating a contractor's technical opinion as a process gate conflated two different things. Nicole has the attention to detail the gate actually requires, and separating technical judgment from process ownership makes both legible. Ops first because the RACI shows Alvin doing the work on 11 of 12 Operations rows against 5 of 8 in PD, and because the Ops job description maps almost one-to-one onto that list — it is the more defined function and the faster relief.

**Alternatives considered:** Leave the quality gates with Perrine and add reporting — rejected, it keeps a contractor as the single approver on batch release with no internal backup. Put every quality gate including formula and stability on Nicole — rejected, it puts a non-technical approver on PET and RIPT calls where Perrine's judgment is the actual value. Hire both specialists at once — rejected, Danielle's condition was cleaning up the system first so the roles can function, and two simultaneous onboardings against an uncleaned system recreates the too-broad seat the 2026-07-17 decision was designed to avoid.

**Owner:** Alvin on the framework and the hiring sequence. Nicole on the quality gate and on both specialist roles once filled.

**Status:** Encoded 2026-07-31. All nine role-maps updated — `quality-manager` (System B canonical), `asana-pd-manager` (PD canonical), `regulatory-manager` (System C canonical), plus the six mirroring sub-skill role-maps. "QA Lead" is retired as a gate label: process gates resolve to Quality Gate (Nicole), technical gates to Technical Advisor (Perrine). The QA Manager seat that SOP §7 requires is no longer vacant — review outcomes sit with Nicole, ratification with Alvin. Skill bodies and SOP text were deliberately left unchanged; each role-map carries a resolution note so runtime reads land correctly without a suite-wide rewrite. The org-wide RACI (78 activities, eleven functions) is in `deliverables/` with a team-facing web version.

**Open:** SOP cleanup and operational prep before onboarding is not done, and it is Danielle's stated condition on the hire. 22 tasks from the retired coordinator seat are still unassigned in an archived holding project with 4 overdue. The RACI goes to Danielle for final review, then to Claire at Calm HR to open the Ops Specialist search. Two exposures survive both hires and are not on the hiring plan: Perrine is a contractor accountable for 8 technical rows with no internal backup, and Operator plus Reg Lead remain the same person, so two regulatory gates designed to be independent still fire against one approver.

---
## 2026-07-31 — Nicole is a collaborator on every Asana task the system writes

**Decision:** Nicole Iturbe is an unconditional follower on every Asana task any skill creates, in every queue, alongside Alvin. She is added whether or not she is the assignee, whether or not she holds that queue's gate, and whether or not the source email or transcript mentions her.

**Why:** This is the 2026-07-30 quality-gate decision reaching the task layer. That decision put quality of product *and* quality of documentation through Nicole as the final check "across every function." The follower rule in `asana_task_contract.md` Phase 3 hadn't caught up: it named Alvin unconditionally and picked Nicole up only when she held the queue's gate or was named in the source, which left her off most Ops and PD tasks — exactly the ones where a documentation-quality gate has something to say. A gate that only sees the tasks that already route to it isn't a gate.

**Where it lives:** Phase 3 of `references/architecture/asana_task_contract.md`, the single contract all nine Asana-writing skills walk. Deliberately **not** in the nine `role-map.md` copies. A role-map row answers "who holds this queue's gate," which is a per-queue question with a per-queue answer; Alvin and Nicole hold every task regardless of queue. Putting it in the role maps would encode one rule in nine files that can drift apart, and the maps already carry Nicole's Quality Gate row for the queue-specific case. The four skills that restate the Phase 3 follower list inline rather than delegating to the contract — both Outlook bridges, `fireflies-asana-bridge`, `asana-pd-manager` — were updated in the same pass, plus the Phase 3 dedupe note (Alvin and Nicole are frequently the assignee or gate-holder too, and a doubled follower is an error, not a second watcher).

**Interpretation taken:** Alvin's instruction was "for all Asana tasks, the creator, Nicole, should always be a collaborator." Read as an appositive — Nicole, always. The alternative reading, "the creator" as a person distinct from Nicole, adds nothing: the skills run as Alvin, so he is the de facto creator on every task, and he was already an unconditional follower. Recorded here because the wording admits a second reading and the encoded rule should not be mistaken for the only one available.

**Owner:** Alvin on the contract. Nicole on what she does with the visibility.

**Status:** Encoded 2026-07-31. `asana_task_contract.md` Phase 3 carries the rule, the rationale, and the dedupe note; its confirmation-preview example was updated so the pattern the model matches on shows Nicole (a stale example is how a new rule gets skipped in practice). `outlook-asana-bridge/evals/evals.json` gained eval 6, which asserts Nicole lands as a follower on a task where she is neither assignee nor mentioned — the case the old rule missed — and eval 3's collaborator expectation was updated under the new rule.

**Open:** Every task in the system now notifies Nicole. If the volume turns into noise the fix is a narrower rule — by queue, or by a task's quality relevance — not a silent revert, since the contract now states the rule is deliberate. Worth revisiting at the monthly quality-trend review the 2026-07-30 decision set up. Also unaddressed: the four skills that restate Phase 3 inline will drift from the contract again on the next change; the durable fix is having them delegate rather than restate, which is a larger edit than this one.

---
## 2026-07-31 — The Asana state machine becomes data: Status is authoritative, sections are a projection

**Decision:** Three changes, from Alvin asking why a PO in `POs In Flight` doesn't move to `Receiving` when it goes into transit.

1. **The state field is the source of truth; section is a projection of it.** Where a queue has a state field, skills write the field and derive the section from a map. Queues with no state field by design — OC3PL, S&OP, SJ Shipping Dashboard, and the two Regulatory projects on section + Gate — are recorded as declared exceptions rather than gaps.
2. **A new canonical registry, `references/architecture/queue_registry.md`,** holding all eleven queues' project GIDs, sections, state fields, and state → section maps. Pulled live from Asana, not transcribed from skill bodies.
3. **An inbound PO with a freight leg homes into Purchasing and Logistics both** — Purchasing primary and owns the close, Logistics secondary and owns the move.

**Why:** Alvin's specific guess was wrong — `POs In Flight` is defined as spanning issued *through* in transit, so In Transit is meant to stay put. But the thing he sensed was missing was real: **no trigger anywhere moved a PO from POs In Flight to Receiving, ever.** Job 3e creates a separate receipt task and never moves the PO, while the weekly scan reads `Receiving queue → Status = Received` by field. A received PO sat in POs In Flight while reporting as Receiving.

Nobody could have caught that by reading, because there was no artifact to read. Every state → section rule in the system existed as a prose sentence inside a job description — never as a table, in any file, for any queue. `asana_task_contract.md` asserted "each queue keeps a state → section map" without saying where, and told skills never to hard-code section GIDs while every Ops, Quality and Regulatory skill did exactly that. Four files claimed canonicity for section data and all four deferred to `asana-field-gids.md`, which is not in the repo — it lives on Alvin's Mac, so nothing running in a remote session could read it. That is the direct cause of the Quality section GIDs existing in four separate copies.

The Status-authoritative choice is what makes Alvin's Asana Rule idea safe rather than hazardous. There are zero Asana Rules in the system today; every section move is a skill calling `update_tasks`. Adding a rule on top of that would have made two writers race on one field. With the field authoritative and the section derived, one rule per queue becomes the only section-mover and skills stop moving sections entirely. The registry carries the rule specs to build in the UI, plus the sequencing — build, dry-run, then remove the skill's section moves, never both at once.

**Alternatives considered:** Section authoritative, matching `claims-il-and-label-keeper` and `adverse-event-and-recall-reporter` — rejected, it rules out Asana Rules for movement and would force a rewrite of every reporting scan that queries by Status. Let each queue declare its own convention — rejected, that is the current situation written down, and it leaves the four bridges needing to know which convention each of eleven queues follows. Patch just the one missing transition — rejected, it would have fixed the symptom Alvin noticed and left the reason nobody noticed it.

**Owner:** Alvin on the registry and on building the Asana Rules (they cannot be created through the MCP).

**Status:** Encoded 2026-07-31. Registry authored from live Asana. `asana_task_contract.md` Phase 4 carries the authority rule; `bridge_queue_contract.md` carries the freight both-case and stopped sending readers to skill bodies for sections. Purchasing's map adds `Received → Receiving`, the missing transition. Fixed in the same pass: `inventory-manager` was written against `[PO In Transit]` and `[PO Received — Pending Invoice]`, a title-prefix vocabulary Purchasing abandoned, and had its own project recorded as the archived `AC Brands Ops Dashboard` with one section and no fields (live: `AC Brands Inventory`, five sections, three fields); the Job 9 routing matrix named two projects that do not exist; and `purchasing-manager` claimed its Status field mirrors `purchase_orders.status` "1:1, options identical" — queried live and false, PLM has `Complete` where Asana has `Closed`, five Asana values appear in no PLM row, and the column has no CHECK constraint.

**Open:** Four queues cannot be ruled yet and the registry says why — Quality Management has one Status field carrying two unrelated workflows, CAPA Log's `Verification & Effectiveness` spans two sections, Logistics' sections split by direction while its status splits by position so status alone cannot pick a section, and Inventory's Status options describe none of its states. Each needs a field or section redesign, not a rule. Also open: a CHECK constraint on `purchase_orders.status` so the Asana and PLM vocabularies cannot drift silently again — a schema change on live data, needs its own approval. And the Quality/Regulatory drift held out of scope by Alvin's call is listed at the end of the plan file and in the registry's drift section, including two skills disagreeing on how many sections the Regulatory project has.

---

---

## 2026-08-01 — All four unrulable Asana queues get field designs; Logistics restructures

**Decision.** The four queues the registry marked "not rulable yet" each get a field change so an Asana Rule can own section movement. Two calls were Alvin's: Logistics rebuilds its sections around position with direction moving to a new field, and the workstream tasks that were misusing `Shipment Status` get the field cleared rather than being moved to their own project.

**Why now.** Every one of the four is cheap today for the same reason — the state field is barely used. CAPA holds one task with a null Status, so its option split migrates nothing. Quality has 15 of 95 tasks carrying Status. Inventory has one of 42. Logistics has six real shipments. That stops being true as the queues fill, so the window for a free migration is now.

**What the live pull changed about the plan.**

Quality did not need its Status field split, which is what I recommended before checking. `Batch State` already existed on the project with exactly the eight batch options, and it was already the authoritative field in practice: on the three near-expiry batches it read `Watch` and the task sat in `Batch — Watch`, while `Status` still said `Active`. So the fix is subtraction — delete the batch options from `Status` — not surgery. The `Watch` collision that made the queue unrulable disappears without renaming anything.

Logistics was worse than "independent axes," which is how the registry had it. `Shipment Status` was being used as a generic progress field on 17 tasks that are not shipments — "Engage Pedrero on CNF filings" was `Pre-Ship`, "Log customs costs to PLM" was `Delivered`. A rule built on the field in that state would have filed a monitoring task under Delivered. Cleared.

**The general principle, stated because it decided Logistics.** Direction is set once when a shipment is created and never changes; position changes constantly. The field carries what is stable and queryable, the section carries what moves. Alvin accepted losing at-a-glance inbound/outbound board grouping in exchange for full rule coverage, since Logistics would otherwise stay the one queue where skills and rules both move sections.

**Build order, cheapest first:** CAPA (0 tasks to migrate) → Quality (12) → Inventory (~38) → Logistics (6, but structural). All four specs live in `references/architecture/queue_registry.md`. The UI edits are Alvin's; the MCP cannot create or edit custom fields, sections, or rules.

**Also settled.** `Ciarra Robinson's previously assigned tasks` is emptied — all 23 tasks were already assigned to Alvin, so the stale project membership came off. It had been surfacing as a phantom sixth section on AC Brands Inventory, which is the cheapest illustration yet of why `memberships` must never be read as belonging to the project you asked about.

---

## 2026-08-04 — SOPs move to `sops/` as canonical text; fresh start on SKN-OPS-004; annual review deferred to a single pass

**Decision:** Three calls made together while finishing the SOP migration (#26, #27).

1. **`sops/*.md` is canonical for every ratified SOP, not SharePoint and not a Supabase row.** SKN-OPS-001 through 009 were migrated out of their skill-side mirror files (capa-coordinator, complaint-and-event-handler, quality-lab-coordinator, batch-lifecycle-tracker, claims-il-and-label-keeper, adverse-event-and-recall-reporter) into `sops/`, joining SKN-OPS-010. The six skills keep their reference files, but as an operational walk layered on top of the canonical text, not a second source of truth — each now points at its `sops/` file instead of a SharePoint path. `quality-manager/references/sop-catalog.md` gained a Canonical text column alongside its existing Skill-side Mirror column.
2. **SKN-OPS-004's reconstructed text stands as the real version — no reconciliation against a SharePoint original.** The migration flagged SKN-OPS-004 (Customer Complaint Handling) as a reconstruction from skill behavior rather than a transcription, since no original text existed anywhere in the repo. Alvin's call: this is a fresh start on SOPs going forward, not a transcription project — don't chase the old SharePoint doc. The content notice in the file is removed.
3. **The overdue annual review on SKN-OPS-001–004 (due 2026-06-30) waits for the full SOP set, then runs once.** Rather than firing a review per SOP as each one gets touched, it holds until the rest of the SOPs Alvin is about to author are populated in `sops/`, then runs as a single pass across everything.

**Why:** SOPs were scattered across SharePoint docx files, skill-side markdown mirrors, and a PLM `sop_documents` table that had already drifted from at least one of them (the 2026-07-29 catalog reconciliation note). Picking one canonical location and making every other copy point at it is what actually stops the drift instead of documenting it after the fact. SKN-OPS-004 specifically had nothing to reconcile against in-repo — treating it as done rather than a standing gap matches the "fresh start" framing and avoids a chase for a document that may not even reflect current practice anymore. Deferring the annual review to one pass avoids doing the review work four separate times against a SOP set that's about to grow.

**Alternatives considered:** Leave the six skills' mirror files pointing at SharePoint and only add `sops/` as a new, uncited copy — rejected, it recreates exactly the multi-copy drift this migration exists to close. Fully rewrite the six skills to read `sops/` directly instead of keeping their own reference files — rejected for now; Alvin doesn't want the skills gutted while he's mid-flow on writing new SOPs, and the mirror-file layer is where skill-specific operational detail (job mappings, HITL gates, field maps) legitimately lives. Pull the real SKN-OPS-004 from SharePoint before calling this done — rejected per Alvin's explicit "don't worry about the original, fresh start."

**Owner:** Alvin. Skill-side mirror files updated in this pass; `sops/` is where all future SOP edits land first.

**Open:** The annual review for SKN-OPS-001–004 is still owed, just batched for later. No date is set for when "the rest of the SOPs are populated" — that's Alvin's call as he authors them.

---

## 2026-08-06 — 13 new SOPs ratified for PD, Ops, and DTC/E-comm

**Decision:** Alvin's call to populate the rest of the SOP set. Same pattern as SKN-OPS-006 through 010 — write down the procedure a skill already runs, ratify it in place — extended outside Quality for the first time, across three domains:

- **PD:** SKN-OPS-011 (Formula Development Stage-Gate & IL Review Gate), SKN-OPS-012 (PD Readiness → PO Request Handoff, joint with Purchasing).
- **Ops:** SKN-OPS-010 (Vendor Onboarding, previously draft — ratified in this pass with its first-contact routing table filled in from purchasing-manager), SKN-OPS-013 (PO Lifecycle), SKN-OPS-014 (Receipt Discrepancy Investigation), SKN-OPS-015 (Vendor Invoice Cost Classification & Routing), SKN-OPS-016 (Receiving & Batch Creation), SKN-OPS-017 (Inventory Adjustment, Write-Off, and Return Disposition), SKN-OPS-018 (Monthly S&OP Run), SKN-OPS-019 (Inbound Shipment Receipt & Fault-Attribution), SKN-OPS-020 (Retailer Outbound ASN & Routing Compliance), SKN-OPS-021 (International Outbound DTC Compliance).
- **DTC/E-comm:** SKN-OPS-022 (DTC Order Exception Routing), SKN-OPS-023 (Pre-Ship OOS Hold Sync).

**Numbering call.** There is no non-Quality SOP sequence anywhere in the repo, and SKN-OPS-010 already crossed into Purchasing before this pass, so all 13 new SOPs took the next open slots in the single existing SKN-OPS-NNN sequence rather than starting a second prefix. Next open slot is 024.

**Why this scope, not more.** Each skill surveyed (asana-pd-manager, purchasing-manager, inventory-manager, supply-demand-planner, logistics-manager, oc3pl-order-manager) had a mix of genuinely governed procedures — staged workflows with roles, gates, and defined states — and thinner read/report jobs that don't carry the shape of a procedure a person is required to follow. Only the governed ones got a SOP; the read-side jobs (position keeping, sourcing/RFQ tracking, vendor performance scorecards, the daily fulfillment KPI log, customs watch, the weekly digest) stayed as skill behavior, not procedure.

**What didn't happen.** None of the six PD/Ops/DTC skills got a dedicated skill-side mirror reference file the way the Quality skills have (`references/skn-ops-*.md`). Their working procedure text stayed inline in each `SKILL.md` — the `sops/` files are migrated from that inline text, and the `quality-manager` catalog cites the inline location rather than a mirror path. Externalizing each skill's mirror file is a follow-on, not done here.

**Owner:** Alvin. `quality-manager/references/sop-catalog.md` carries all 23 SOPs now, with an open item flagging that a Quality-owned catalog holding non-Quality SOPs is a structural question, not a settled one.

**Open:** Same annual-review deferral as the 2026-08-04 decision now applies to this batch too — SKN-OPS-011–023 join the "run once the full set is populated" review, not a per-SOP review on next review date. Whether a second catalog should exist for non-Quality SOPs, and whether the six skills should get dedicated mirror files, are both unresolved and noted in the catalog's own Open Items.
