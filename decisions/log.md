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
