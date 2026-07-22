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

## 2026-07-22 — Wire direct Shopify MCP reads into inventory-manager and supply-demand-planner

**Decision:** Both skills now call Shopify directly via MCP instead of relying on PLM or manual upload for Shopify-sourced data. `inventory-manager` calls `mcp__Shopify__get-inventory-levels` for Job 1 (position keeping) and Job 4 (three-way reconciliation) — previously the Shopify side of that math had no defined live source at all. `supply-demand-planner` calls `mcp__Shopify__run-analytics-query` / `list-orders` for DTC actuals in Step 1 of the monthly S&OP run — previously "Shopify" was named as a source but the only concretely wired mechanism was manual CSV upload; CSV now drops to a fallback used only when the MCP read fails, and the run summary must flag it whenever that happens.

**Why:** Alvin scoped this as the two skills where Shopify data actually feeds live decisions (inventory position/reconciliation, demand forecasting) — as opposed to oc3pl-order-manager (Logiwa is already authoritative there) or sjs-status-reporter (PD-only, inherits inventory data downstream instead). S&OP was the sharper gap of the two: a monthly forecast that drives buy recommendations was running on whatever CSV got uploaded, not on live sales data.

**Alternatives considered:** Leaving supply-demand-planner on CSV-primary (rejected — no reason to prefer a manual upload over a live MCP read now that one exists); routing the new reads through PLM's existing Shopify sync instead of a direct MCP call (deferred — see open question below).

**Owner:** Alvin.

**Open question raised during this work (not resolved, needs its own scoping pass):** PLM currently syncs to Shopify via a separate API integration, which feeds the landing hub's inventory dashboard. Now that Shopify has a direct MCP connector into Claude, does the PLM↔Shopify API sync still pull its weight, or should some/all of that data path move to direct MCP reads instead? This is a bigger build than the two-skill wiring above — touches the landing hub's data pipeline, not just a skill's read source — and needs its own scoping conversation before any change. For now, both syncs coexist: PLM's API sync keeps feeding the landing hub unchanged, and the two skills above read Shopify directly and separately. Flagged in both skills' SKILL.md so the duplication is visible until this resolves.

---
