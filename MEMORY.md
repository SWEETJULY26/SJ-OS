# Memory

Running context that shouldn't live only in chat history. Append entries; don't delete old ones unless they're fully superseded — mark superseded entries rather than removing them, so the reasoning trail survives.

---

## 2026-07-20 — SJ-OS architecture consolidation, Phase 3 + 4 complete

**What happened:** Consolidated the previously-separate `SWEETJULY26/Skills` repo and the full locally-installed skill set (59 skills) into this repo under `.claude/skills/` and `references/architecture/`. Closed the entire Phase 3 backlog (stale docs, dangling references, wrong fonts, wrong SKU counts across ~10 files) and all 9 Phase 4 cross-system handoffs (PD↔Margin, Quality↔PD, comp-intel↔PD, retail-intel↔status-reporter). Retired `ac-brands-pd-system` — `sjs-pd-system` is now the single PD router; 6 live scheduled Routines were repointed accordingly.

**Key lesson learned the hard way:** I (Claude) initially claimed "no PD HTML dashboard exists" — wrong. Three real ones exist (`pd-portfolio.html`, `pd-weekly.html`, `pd-readiness-tracker.html` on the `acb-thelanding` hub), fed by scheduled Routines. I'd only checked skill files, not the actual target repo. Alvin caught it. **Lesson for future sessions: verify against the actual system (the hub repo, the live Asana data, the live PLM schema), not just what a skill's own documentation claims.**

**Open decision, not yet made:** 10 candidate real agents (`.claude/agents/*.md` — zero exist today) are scoped in `decisions/skills-architecture-tracker.md` Phase 4a. Top candidate: `pd-margin-handoff` (PD concept approval → archetype-advisory → pressure-test → walk-away if it fails). Waiting on Alvin to pick which to build first.

**Also flagged, not yet fixed:** `sjs-ingredient-lookup` has its own stale "13 products" claim — different skill, deferred by Alvin to a later pass.

## 2026-07-20 — Reference guides + this file added

Closed the two highest-leverage gaps from the second `/audit` (80/100): wrote `references/{asana,supabase-plm,microsoft-365,fireflies,shopify}-api.md` covering all 7 connected tool domains, and created this file. First audit (2026-07-19) scored 75/100 with an empty decisions log as the #1 gap — that's now fixed too (see decisions/log.md).

---

## Standing facts worth not re-deriving every session

- **Two PLM-adjacent Supabase projects exist** — `ujkabbffvhpewpbttmmy` (PLM, the one that matters everywhere) and `ndxatsnrnlbdesridwfq` (Amazon-only Business Dashboard). Don't confuse them.
- **Two Asana MCP connector instances** are present in this environment (`Asana` and `Asana-c313a468`) — scheduled Routines reference both explicitly in places. Not a bug, just how the environment is wired.
- **iMessage is the one connections.md domain still marked "not yet connected."**
- **`sjs-ingredient-lookup`'s stale count** (deferred, see above) is the one known-but-unfixed doc issue left in the skill set as of 2026-07-20.
