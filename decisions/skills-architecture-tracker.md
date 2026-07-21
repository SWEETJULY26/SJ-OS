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
- [x] **S5-5** Fixed 2026-07-20 — replaced the two "comprehensive" instances (both internal meta-language) with "complete"/"full" per org writing-style rules.
- [x] **S5-6** Skill 6 (outlook-plm-bridge) already referenced as a data source.

### Skill 6 — outlook-plm-bridge

- [x] **S6-1** Added 2026-07-20, based on Alvin's clarification: the same vendor thread carries three distinct signal types that touch different tables — (1) SKU assignment (tube SKU usually named; carton SKU often separate, don't wait for both) → `UPDATE components.sku`; (2) artwork proof once approved → `INSERT public.attachments` (`entity_type='component'`, `category='Artwork'` — verified this is already a real, in-use convention, not invented); (3) everything else stays the original cost/spec Flow G pattern. Written up in `references/flows.md`.
- [x] **S6-2** `references/flows.md` exists and is current. `references/senders.md` intentionally absent — retired 2026-05-26 in favor of live Supabase wiki reads (see `references/architecture/system_map.md`).

### Master router — sjs-pd-system

- [x] **MR-1** Added 2026-07-20: the two missing text output types (portfolio audit/health-check, creative artwork tracker), the three real HTML dashboards + daily recap automation, and fixed a stale "13 active" SKU count and stale Barlow/Nunito font mentions found in this same file while making the pass.
- [x] **MR-2** Added 2026-07-20: routing entries for portfolio audit, timing/cutover-risk MCP limitation, creative artwork tracker, and the daily PD recap.

**Phase 3 is now fully complete.**

**RESOLVED 2026-07-20:** Alvin's call — no org-tier/brand-tier split needed for PD, just one router: `sjs-pd-system` under `sjs-master`. `ac-brands-pd-system` was a strictly older, less complete duplicate (6 skills vs. 7, numbered-style, missing everything added this session) — nothing worth preserving. It was also, unexpectedly, the *actual entry-point router* six live scheduled Routines used ("read this to confirm router state, then route through it") — not a dead file. Repointed all 6 Routines (`sjs-pd-morning-sweep`, `sjs-pd-midday-sweep`, `sjs-pd-eod-reconciliation`, `weekly-pd-update`, `pd-monthly-rollup`, `pd-quarterly-rollup`) plus `references/architecture/automations.md`, `ayesha-weekly-briefing/SKILL.md`, and `ac-brands-ops-system/SKILL.md` to `sjs-pd-system`, then removed `ac-brands-pd-system` entirely. No Routine recreation needed — these are scheduled-prompt content edits, not bootstrap-prompt changes, so the next fire picks up the new pointer automatically.

**2026-07-20 pass note:** Verified items above against current file state rather than trusting the April findings blindly — most had already been resolved in the 2026-05-17 modernization pass and just needed the checkbox updated. Two real bugs were introduced by the 2026-07-19 root-consolidation commit (dangling `sjs-master/*.md` references in `asana-pd-manager/references/cross-skill-handoffs.md` and `suppliers.md` — files outside `SKILL.md` that the original verification grep missed) and are now fixed; a broader repo-wide sweep afterward confirmed no other dangling references remain. A separate mistake — wrongly claiming no PD HTML dashboard exists — was caught by Alvin and corrected after actually checking the `acb-thelanding` hub repo instead of just the skill's own docs.

**New finding, out of scope for this pass:** `sjs-ingredient-lookup` (a Utility skill, not part of this PD tracker) also has a stale "13 products" claim in its SKILL.md. Worth checking against the live PLM product count next time that skill comes up.

---

## Phase 4a — Real agent candidates (backlog, not yet built)

Zero `.claude/agents/*.md` exist in this repo today — every skill so far is prose the same assistant reads inline. Alvin wants to incorporate real agents as a result of Phase 4 wiring. Candidates identified 2026-07-20, ranked by how much isolated judgment / multi-step reasoning they involve (the actual bar for "this deserves an agent, not just router prose"):

1. **`pd-margin-handoff`** — PD concept approval → archetype-advisory → pressure-test → walk-away if it fails (X-1/X-2/X-3, already fully specified in `system_map.md`).
2. **`quality-pd-reverse-flow`** — complaint trend / CAPA root cause = formulation → decide whether to open a PD reformulation task (X-5).
3. **`il-review-gate`** — fires on every Signed Approvals stage move (SKN-OPS-008); real judgment call currently just prose in `asana-pd-manager` Job 3.
4. **`sae-recall-triage`** — adverse event / recall classification with statutory clocks; high-stakes judgment currently inline in `complaint-and-event-handler`.
5. **`capa-root-cause-analyst`** — the 5 Whys / Fishbone phase of the CAPA lifecycle; currently a prose walkthrough in `capa-coordinator`.
6. **`vendor-scorecard-analyst`** — OOS/OOT signal → vendor flag thresholds → scorecard signal-back to `purchasing-manager`.
7. **`ubm-retail-readiness`** — UBM launch window → `sjs-retail-intel` cohort/price-ladder → feeds Launch Readiness Report (X-4/X-7).
8. **`comp-intel-digest-router`** — monthly competitive digest → decide what's pipeline-relevant → surface to the right people (X-6).
9. **`email-signal-classifier`** — the master classifier logic currently duplicated across `outlook-asana-bridge`, `fireflies-asana-bridge`, `outlook-plm-bridge`; one shared agent would remove the copy-paste.
10. **`margin-portfolio-quarterly-reviewer`** — reframe `sjs-margin-portfolio-review`'s quarterly sweep as an agent invoked at quarter-end rather than a skill Alvin has to remember to trigger.

Decision deferred: which to build and in what order. Revisit after Phase 4 wiring lands, since the wiring work will clarify which handoffs actually need isolated agent context vs. simple router prose.

---

## Phase 4 — Cross-system wiring (after PD refactor)

- [x] **X-1** Already wired — `asana-pd-manager` "Outbound handoffs" already documents "Concept approval → `sjs-margin-archetype-advisory` then `sjs-margin-pressure-test`."
- [x] **X-2** Already wired — same section: "Pressure-test fail → `sjs-margin-walk-away`."
- [x] **X-3** Reviewed 2026-07-20 — `sjs-margin-portfolio-review` sweeps **every active SKU from PLM** each quarter, not just PD signed-off ones from the last 90 days. Broader and more correct than the original ask; not a gap.
- [x] **X-4** Already wired — same `asana-pd-manager` section: "SKU heads to UBM listing → `sjs-retail-intel`."
- [x] **X-5** Fixed 2026-07-20 — the receiving side (`asana-pd-manager`) already expected this, but neither source skill fired it. Added: `capa-coordinator`'s root-cause phase now hands off a reformulation task when root cause = formulation (plus a margin-pressure-test re-run once reformulation completes); `complaint-and-event-handler`'s trend analysis now separately flags formulation-pattern trends to PD even before a CAPA opens. Both frontmatter "hands off to" lines updated.
- [x] **X-6** Fixed 2026-07-20 — added a PD handoff rule to `sjs-comp-intel`'s Cross-stream handoff rules: monthly digest category shifts stage as pipeline input via `sjs-status-reporter` to Perrine/Alvin/Soraya, Nicole consulting.
- [x] **X-7** Fixed 2026-07-20 — added `sjs-retail-intel` as a Launch Readiness Report data source in `sjs-status-reporter`, plus a new "Retail Benchmark" section in the template output.
- [x] **X-8** Already wired — `ayesha-weekly-briefing` explicitly documents its PD Portfolio pull for Slide 6.
- [x] **X-9** Reviewed 2026-07-20 — the three real branded-output skills (`sjs-status-reporter`, `quality-status-reporter`, `regulatory-status-reporter`) already defer to `sweet-july-skin-brand`. `ayesha-weekly-briefing` doesn't need to: it only writes text bullets into an existing, pre-designed Canva template — no font/color/layout choices happen in this skill's scope, and its own "Voice and Format" section is intentionally Alvin's operational voice, not Sweet July Skin's customer-facing Irie voice (this is an internal founder briefing, not a brand deliverable). Not a gap.

**Phase 4 is now fully wired** — 4 items were already correct on inspection, 3 needed real fixes, 2 were reviewed and found to be non-gaps (broader/different-but-correct design). Agent candidates from Phase 4a remain a deferred decision.

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

---

## Phase 5 — Deeper audit (2026-07-20, post Phase 3/4)

Alvin asked for a systematic repo-wide sweep before committing to the Phase 4a agent decision. Wrote a script to check every `references/X.md` mention across all 58 skills against what actually exists (resolving both repo-root-relative and skill-relative paths correctly — first pass had a path-resolution bug that produced 61 false positives, re-verified down to 12 real candidates, then checked each by hand).

**Findings:**
- [x] **Real gap, fixed:** `plm-assistant/references/database-schema.md` was referenced by `plm-assistant` itself and by `sjs-margin-architect` but never created. Generated it from the live schema (`information_schema.columns` + foreign keys) — full table-by-table reference including which tables are schema-ready but not yet operationally populated (`outbound_orders`, `shipments`, `retailer_compliance_specs`, `vendor_invoices`, etc.).
- [-] **Deprioritized 2026-07-21 (Alvin's call):** `sjs-retail-intel`'s own reference map promises `references/promo-calendars/ulta-annual.md` but the file (and the whole `promo-calendars/` directory) doesn't exist. Needs real Ulta promo calendar data, not something to fabricate — Alvin doesn't own this and it's out of scope for now. Pushed to the back of the backlog; revisit only if someone picks up retail-intel research ownership.
- **False positives, confirmed fine on inspection:** cross-skill references to `sjs-margin-architect/references/framework.md` (from walk-away/archetype-advisory/interactive-model/portfolio-review), `oc3pl-order-manager`↔`inventory-manager`'s mutual oos-file references, `outlook-asana-bridge`/`asana-pd-manager`'s historical "retired X on 2026-05-26" notes, `sjs-pd-system`'s informal (but locatable) reference to `asana-pd-manager/references/confirmation-protocol.md`.

**New backlog item — evals:** Zero of the 58 skills have run coverage (with-skill vs. baseline benchmark results), even though `acb-skill-builder` ships a full working eval harness (with-skill vs. baseline subagent runs, quantitative assertions, benchmark viewer — see its `references/running-evals.md`). This is real tooling sitting unused, not a build-from-scratch problem. Scope TBD — 58 skills is a lot to eval at once; likely start with the highest-traffic ones (asana-pd-manager, the four bridges, capa-coordinator, complaint-and-event-handler) rather than all at once.

**Correction found 2026-07-21:** the "zero eval coverage" claim above wasn't quite right — `capa-coordinator/evals/evals.json` and `complaint-and-event-handler/evals/evals.json` already existed (3 well-written test cases each, dated to the original 2026-07-19 repo-consolidation commit, predating this tracker entry). They'd just never been run — no workspace, no grading, no benchmark. Lesson matches the MEMORY.md standing one: verify against the actual file state, not a summary claim, before treating something as a from-scratch gap.

**Noted, not acted on:** Alvin mentioned "graph engineering" as a way of thinking about agent orchestration (graph-based vs. sequential-loop) — relevant framing for whenever the Phase 4a agent-build decision gets made, not an immediate action item.

---

## Phase 5a — First eval coverage (2026-07-20)

Alvin picked `outlook-asana-bridge` and `outlook-plm-bridge` as the first two skills to eval (of the six candidates proposed: asana-pd-manager, the four bridges, capa-coordinator, complaint-and-event-handler — the other four remain unscoped). Wrote `evals/evals.json` for each (2 test cases apiece, matching real workflows: a weekly triage/scan and a specific multi-system-routing scenario), ran with-skill vs. baseline subagent pairs against live Outlook/Asana/PLM reads (writes gated behind confirmation on both sides, so nothing was actually committed), graded against 5 assertions per eval, and built a benchmark + review viewer.

**Results:** with-skill passed 20/20 assertions across both skills; baseline passed 6/20 (7/20 counting the PLM PO-ack case, which scored 3/5 — closest to something a generic agent can infer unassisted). The gap is structural — baseline never applies the classification-label system, multi-system parent/child routing, or PLM cross-flagging that's the actual point of these skills existing. One assertion ("no write before confirmation") was flagged as non-discriminating — it passed in every run regardless of skill quality because both configurations were constrained not to write for the eval itself, not because of anything the skill did.

**Real bugs found from Alvin's review of live output** (not style nits — factual misses against his actual mailbox), fixed same session in both `outlook-plm-bridge/SKILL.md` (+ `references/flows.md` Flow A) and `outlook-asana-bridge/SKILL.md`:
- Dropped NetSuite-relay invoice recognition entirely from Flow I — not a real channel; the skill had been sweeping for it based on a stale assumption from the 2026-05-31 KAF migration note.
- Fixed OC3PL folder-sweep guidance in both bridges — it's a real folder sitting directly under Inbox, not nested; a `folderName` "not found" error is a lookup mismatch, not proof the folder is absent, so the skill was wrongly concluding the folder didn't exist and skipping it.
- Added Pedrero Regulatory to the topic-folder sweep list in both bridges — sender-domain matching alone (`pedreroregulatory.com`) misses forwards/CCs from other addresses; the folder is the backstop.
- Added a "read to the end of the thread before flagging still-open" rule to `outlook-plm-bridge` — a run reported HCT tube proofs as still awaiting signature when they'd actually already been signed and sent back later in the same thread.
- Rewrote Flow A (PO) recognition in `outlook-plm-bridge/references/flows.md` to match Alvin's actual workflow: POs go out as PDF attachments without the PO number in the subject/body, so a literal-number text search was the wrong tool. A vendor reply that reads as a receipt confirmation is now sufficient to set `status = 'Acknowledged'` on its own, and the outbound send itself is sufficient to set `status = 'Sent'` — neither needs to wait for the PO number to be restated.

**Not yet done:** re-run these two evals against the fixed skills to confirm the corrections hold (iteration-2). Remaining four skills from the original candidate list (asana-pd-manager, fireflies-asana-bridge, capa-coordinator, complaint-and-event-handler) still have zero eval coverage — Alvin explicitly deferred them this pass, not a gap that was missed.

**Update — iteration-2 re-run (2026-07-20, same session):** re-ran the with-skill side of all four evals against the fixed skills. All four v1.2 fixes confirmed against live data: NetSuite sweep not attempted; the HCT tube-proof thread was read to the end and correctly showed proofs already signed/returned (a real behavior change vs. iteration-1, which had flagged them as still pending); the new Flow A PO recognition rule found a genuine receipt-confirmation on PO #100336 buried in a shared punch-list email that the old literal-number search had missed entirely (a `status: Sent → Acknowledged` update now stages correctly).

The OC3PL/Pedrero fix surfaced a sharper root cause than what got written into v1.2: two independent runs found that `outlook_email_search`'s `folderName` parameter reliably returns `NOT_FOUND` on both folders — not intermittently, and retrying the same call doesn't help. Both are real, populated, non-nested Inbox subfolders; the actual working fallback is listing folders via `read_resource` on `mail:///folders/` to get the folder ID and reading directly by ID, or a sender-domain backstop search. Rewrote the guidance in both bridges (now v1.3) to specify that fallback instead of just "retry the exact name."
