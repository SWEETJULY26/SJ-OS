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
