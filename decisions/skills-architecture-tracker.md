# AC Brands Skills System — Audit & Migration Tracker

**Started:** 2026-04-29
**Owner:** Alvin Belt
**Goal:** Migrate from per-skill duplication to `_shared/` + master router architecture without losing context across sessions.

---

## Status legend

- `[ ]` open
- `[~]` in progress
- `[x]` done
- `[-]` deferred / out of scope this pass

---

## Phase 0 — Architecture decisions (settled)

- [x] Top-level master router: `ac-brands-master`
- [x] Shared folder: `/mnt/skills/user/_shared/` (underscore sorts first)
- [x] PLM is runtime truth for products, batches, vendors, components, POs, BOMs
- [x] `_shared/` is recognition layer — things real-in-the-world before they're PLM-truth
- [x] Brand skill is shared dependency for every output-producing skill
- [x] Lint script: explicit-run only, not post-edit auto
- [x] Migration audit: dry-run first, always
- [x] Router style: invisible (silent routing, only the answer surfaces)
- [x] First-pass scope: PD (7), Margin (6), Comp/Retail intel (2), brand, ingredient lookup, find/replace
- [x] Deferred this pass: Ops sub-skills, Quality, Ayesha briefing, Holiday Comms

---

## Phase 1 — `_shared/` build

- [x] `senders.md` — internal team + external partners (consolidate from Skills 1, 2, 3, 6)
- [x] `team.md` — internal AC Brands team with Asana GIDs once looked up
- [x] `suppliers.md` — supplier-product mapping + manufacturer notes
- [x] `products.md` — current PD product list + Asana project GID + PLM product ID (or "read live from PLM")
- [x] `gids.md` — Asana portfolio GID, project GIDs, custom field GIDs (incl. MCP-blocked ones)
- [x] `terminology.md` — vendor terminology rules (HCT lip tubes, turnkey definitions, no "vessel")
- [x] `style_rules.md` — banned words, no parentheses in titles, status update title format
- [x] `automations.md` — daily 2 PM PT recap, running log task GID, Cowork patterns
- [x] `system_map.md` — every skill, which system, which router, dependencies
- [x] `tool_patterns.md` — search strategy notes (date/scope > keyword for Fireflies/Outlook)
- [x] `build_patterns.md` — Python build-script pattern, programmatic validation, Chrome MCP fallback

---

## Phase 2 — Master router build

- [x] `ac-brands-master/SKILL.md` — top-level router shell
- [x] Routing map: question → which sub-system router
- [x] Cross-system handoff playbook (PD↔Margin, PD↔Ops, PD↔Quality, etc.)
- [x] No domain data — all reads via `_shared/` or PLM

---

## Phase 3 — PD skills refactor (audit findings from 2026-04-29)

### Cross-skill structural

- [x] **C-1** Skill count inconsistency — checked 2026-07-20, false positive. The only "4-skill" mention left is a historical changelog note about a past rename, not a live inconsistency.
- [x] **C-2** Skill 5 hardcoded wrong brand fonts (Barlow/Nunito) vs actual (GT America Expanded / Adrianna) — fixed 2026-07-20.

### Skill 1 — asana-pd-manager

- [x] **S1-1** Project list stale — resolved back in the 2026-05-17 modernization (moved to live PLM/Asana lookup via `references/pd-projects.md`); one stale "13 active SKUs" claim in the description fixed 2026-07-20.
- [x] **S1-2** Status update title convention missing — added 2026-07-20: `[RAG emoji] [Color], [Month Day], [Year] Update`.
- [x] **S1-3** Portfolio MCP limitation — documented 2026-07-20 in a new "Known MCP limitation" section.
- [x] **S1-4** Daily recap cross-link — added 2026-07-20 to the Reference index, pointing to `references/architecture/daily_pd_recap.md` and `automations.md`.
- [x] **S1-5** Vendor terminology rules — present in `references/suppliers.md`; found and fixed a dangling `sjs-master/tool_patterns.md` reference left over from the 2026-07-19 consolidation.
- [x] **S1-6** No-parentheses-in-titles rule — present in `references/architecture/style_rules.md`.
- [x] **S1-7** Allure Labs — present in `references/suppliers.md`.

### Skill 2 — fireflies-asana-bridge

- [x] **S2-1** Search strategy — checked 2026-07-20: Mode 1 already instructs "search... with appropriate date filters" before fetch. Adequate, though outlook-asana-bridge's version (explicit `afterDateTime`-first language) is more explicit — could tighten wording later, not a functional gap.
- [x] **S2-2** "4-skill system" stale description — not found, already resolved.

### Skill 3 — outlook-asana-bridge

- [x] **S3-1** Search strategy — checked 2026-07-20: already uses `afterDateTime`-first pattern explicitly. Resolved.
- [x] **S3-2** CDW mini-box outreach — clarified by Alvin 2026-07-20: it's shipping packaging, not product development. Added an explicit `ops`-routing override to the classifier table so CDW mini-box correspondence doesn't get misclassified as `pd` via the general CDW supplier-domain signal.

### Skill 4 — asana-plm-bridge

- [x] **S4-1** "4-skill system" / "extends the existing PLM Assistant" stale text — not found, already resolved.
- [x] **S4-2** Stale 13-product mapping — not found, already resolved.

### Skill 5 — sjs-status-reporter

- [x] **S5-1** Brand spec wrong (see C-2) — fixed 2026-07-20.
- [x] **S5-2** Hardcoded hex codes — checked against `sweet-july-skin-brand` canonical spec, they match. Not actually wrong.
- [x] **S5-3** Added Output Templates 6 (Portfolio Audit / Health-Check) and 7 (Creative Artwork Tracker) 2026-07-20, sourced from real Asana project data (`Creative Requests`) and PLM (`public.brand_assets`).
- [x] **S5-4** **Corrected 2026-07-20** — first pass wrongly claimed no PD HTML dashboard exists. Alvin flagged it; checking the `acb-thelanding` hub repo directly (not just skill files) found three live PD dashboards already in production: `pd-portfolio.html` (fed by `pd-quarterly-rollup`), `pd-weekly.html` (fed by `weekly-pd-update`), `pd-readiness-tracker.html` (fed by `pd-monthly-rollup`), plus `pd-system.html`. Documented the real build pattern (static JSON index + client-side fetch, published via the same `landing-hub-publish` mechanism as Quality/Regulatory) in `sjs-status-reporter/SKILL.md`. Lesson: verify against the actual target repo, not just the skill's own documentation, before concluding something doesn't exist.
- [ ] **S5-5** Banned-words check — only internal meta-description language found ("comprehensive" describing a report type), not customer-facing output copy. Low priority.
- [x] **S5-6** Skill 6 (outlook-plm-bridge) already referenced as a data source.

### Skill 6 — outlook-plm-bridge

- [x] **S6-1** Added 2026-07-20, based on Alvin's clarification: the same vendor thread carries three distinct signal types that touch different tables — (1) SKU assignment (tube SKU usually named; carton SKU often separate, don't wait for both) → `UPDATE components.sku`; (2) artwork proof once approved → `INSERT public.attachments` (`entity_type='component'`, `category='Artwork'` — verified this is already a real, in-use convention, not invented); (3) everything else stays the original cost/spec Flow G pattern. Written up in `references/flows.md`.
- [x] **S6-2** `references/flows.md` exists and is current. `references/senders.md` intentionally absent — retired 2026-05-26 in favor of live Supabase wiki reads (see `references/architecture/system_map.md`).

### Master router — sjs-pd-system

- [x] **MR-1** Added 2026-07-20: the two missing text output types (portfolio audit/health-check, creative artwork tracker), the three real HTML dashboards + daily recap automation, and fixed a stale "13 active" SKU count and stale Barlow/Nunito font mentions found in this same file while making the pass.
- [x] **MR-2** Added 2026-07-20: routing entries for portfolio audit, timing/cutover-risk MCP limitation, creative artwork tracker, and the daily PD recap.

**Phase 3 is now complete** except S5-5 (low priority, deferred) and a new finding below.

**RESOLVED 2026-07-20:** Alvin's call — no org-tier/brand-tier split needed for PD, just one router: `sjs-pd-system` under `sjs-master`. `ac-brands-pd-system` was a strictly older, less complete duplicate (6 skills vs. 7, numbered-style, missing everything added this session) — nothing worth preserving. It was also, unexpectedly, the *actual entry-point router* six live scheduled Routines used ("read this to confirm router state, then route through it") — not a dead file. Repointed all 6 Routines (`sjs-pd-morning-sweep`, `sjs-pd-midday-sweep`, `sjs-pd-eod-reconciliation`, `weekly-pd-update`, `pd-monthly-rollup`, `pd-quarterly-rollup`) plus `references/architecture/automations.md`, `ayesha-weekly-briefing/SKILL.md`, and `ac-brands-ops-system/SKILL.md` to `sjs-pd-system`, then removed `ac-brands-pd-system` entirely. No Routine recreation needed — these are scheduled-prompt content edits, not bootstrap-prompt changes, so the next fire picks up the new pointer automatically.

**2026-07-20 pass note:** Verified items above against current file state rather than trusting the April findings blindly — most had already been resolved in the 2026-05-17 modernization pass and just needed the checkbox updated. Two real bugs were introduced by the 2026-07-19 root-consolidation commit (dangling `sjs-master/*.md` references in `asana-pd-manager/references/cross-skill-handoffs.md` and `suppliers.md` — files outside `SKILL.md` that the original verification grep missed) and are now fixed; a broader repo-wide sweep afterward confirmed no other dangling references remain. A separate mistake — wrongly claiming no PD HTML dashboard exists — was caught by Alvin and corrected after actually checking the `acb-thelanding` hub repo instead of just the skill's own docs.

**New finding, out of scope for this pass:** `sjs-ingredient-lookup` (a Utility skill, not part of this PD tracker) also has a stale "13 products" claim in its SKILL.md. Worth checking against the live PLM product count next time that skill comes up.

---

## Phase 4 — Cross-system wiring (after PD refactor)

- [ ] **X-1** PD → Margin: Concept approval should fire `sjs-margin-archetype-advisory` + `sjs-margin-pressure-test`. Wire in Skill 1.
- [ ] **X-2** PD → Margin: Pressure-test fail routes to `sjs-margin-walk-away`. Wire path.
- [ ] **X-3** PD → Margin: Quarterly portfolio review pulls from PD signed-off SKUs. Wire timing.
- [ ] **X-4** PD → Retail intel: UBM-bound SKU should run through `sjs-retail-intel` for cohort + ladder. Wire trigger.
- [ ] **X-5** Quality → PD: Complaint trends + CAPA formulation root cause should reverse-flow to PD. Wire placeholder.
- [ ] **X-6** Comp intel → PD: Monthly trend digests should land in front of Nicole/Soraya as pipeline input. Wire reporting path.
- [ ] **X-7** Skill 5 (Status Reporter) should pull from `sjs-retail-intel` for Launch Readiness benchmarks.
- [ ] **X-8** Ayesha briefing pulls from PD Portfolio — Skill 1 documents this dependency. Slide 6 co-ownership with Nicole noted.
- [ ] **X-9** All output-producing skills defer to `sweet-july-skin-brand` for fonts/colors/voice.

---

## Phase 5 — Margin + Intel pass

- [ ] Same `_shared/` migration applied to 6 margin skills + 2 intel skills.
- [ ] Verify each reads from PLM via SELECT, not hardcoded data.
- [ ] Cross-system triggers wired both directions.

---

## Phase 6 — Lint script

- [ ] `_shared/lint.py` — quick mode (structural), full mode (PLM round-trip), migration mode (one-shot).
- [ ] Markdown report output — drops into this tracker as next-session pickup.

---

## Phase 7 — Test scenario

- [ ] Run a real cross-system scenario through the architecture (e.g., Soursop launch touching PD + Ops + Margin + Retail + Brand) to validate routing.

---

## Phase 8 — Defer to follow-on sessions

- [ ] Ops sub-skills migration
- [ ] Quality skills migration (complaint-and-event-handler, capa-coordinator)
- [ ] Ayesha briefing migration
- [ ] Holiday comms migration

---

## Working notes

- Skill files at `/mnt/skills/user/[skill]/SKILL.md` are not directly writable from this environment. Build everything in `/home/claude/skills-v2/`, validate, copy to `/mnt/user-data/outputs/`, then deploy via the Anthropic skills UI.
- Persistence pattern between sessions: this tracker file. Keep it as the working doc. Each session starts by reading the latest copy.

---

## Phase 1 / 2 — File consolidations (2026-04-29 session)

Some files from the original Phase 1 plan were rolled into others rather than created standalone:

- `team.md` — rolled into `senders.md` (internal team is the first section)
- `terminology.md` — split: vendor terms in `suppliers.md`, banned-word and format rules in `style_rules.md`
- `build_patterns.md` — rolled into `tool_patterns.md`

Files added beyond the original plan:

- `daily_pd_recap.md` — the reverse-engineered prompt spec for the 2 PM PT automation. Pulled from 8 actual recap comments on running log task `1214208955674591`.

Final `_shared/` file list (8 files):
- `senders.md` — internal team + external partners
- `suppliers.md` — manufacturer + component scope + lip program logic + banned terminology
- `products.md` — Asana → PLM name mapping + PLM live-read pattern
- `gids.md` — full GID reference incl. all 20 portfolio custom fields
- `style_rules.md` — banned words, formatting, status update titles
- `tool_patterns.md` — Fireflies/Outlook/Asana/PLM patterns + build pattern
- `automations.md` — index of recurring automations
- `system_map.md` — every skill, every system, cross-system handoff list
- `daily_pd_recap.md` — full prompt spec for the 2 PM PT recap



## Monday Briefing reverse-engineering (2026-04-29 session, continued)

- [x] `monday_weekly_briefing.md` — reverse-engineered from Week 17 + Week 18 comments
- [x] `automations.md` updated with the Monday briefing pointer

Final `_shared/` file list now 10 files:
- `senders.md`
- `suppliers.md`
- `products.md`
- `gids.md`
- `style_rules.md`
- `tool_patterns.md`
- `automations.md` (index)
- `system_map.md`
- `daily_pd_recap.md`
- `monday_weekly_briefing.md`

**Note on Monday briefing data:** Only two historical samples exist (the running log task started Apr 22). The spec is solid for the structural pattern but interpretation may need revisiting once 4-6 more Monday briefings have posted. The richer Apr 22 sections (immovable dates, top 5 moved, top 5 to watch, named overdue, stale, new projects) are documented as opt-in additions rather than required.


## Orchestration correction (2026-04-29 session, late)

Prompt specs for the daily recap and Monday briefing were initially written as
direct tool-pull instructions (Fireflies → Outlook → Asana → PLM, each pulled
inline). Corrected to skill-composition orchestration:

- Daily PD recap → activates Skills 1, 2, 3, 5, 6
- Monday briefing → activates Skills 1, 2, 3, 4, 5, 6
- Ayesha founder briefing → composition of PD + Ops skills (when refactored)

Each skill encapsulates its tool pattern. The recap orchestrates the skills
and composes the output. New principle added to `_shared/system_map.md` at the
top of the file.

Files revised:
- [x] `daily_pd_recap.md` — rewritten as orchestration spec
- [x] `monday_weekly_briefing.md` — rewritten as orchestration spec
- [x] `system_map.md` — orchestration principle added near top
