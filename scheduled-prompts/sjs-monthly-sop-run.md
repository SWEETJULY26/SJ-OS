# Scheduled task: sjs-monthly-sop-run

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/supply-demand-planner/SKILL.md`
- `/home/user/sj-os/.claude/skills/plm-assistant/SKILL.md`
- `/home/user/sj-os/.claude/skills/sjs-ops-system/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
Run the full monthly S&OP for Sweet July Skin using the supply-demand-planner skill (resolve the skill path at runtime; do not rely on a fixed /sessions/… path).

Objective: produce a complete monthly S&OP run — forecast, targets, buy recs, fill calendar, and exception flags — staged in Asana under HITL approval, then handed off to purchasing-manager, inventory-manager, and sjs-status-reporter.

STEP 0 — ALWAYS ASK FIRST. Before pulling any data or running anything, ask Alvin which forecast plan in PLM to reference for this run. Pull the list of active forecast_plans from PLM Supabase (project ujkabbffvhpewpbttmmy) via plm-assistant and present them. Default to the most recent ratified plan (currently H2 2026) but never assume — wait for his answer. If he doesn't respond within a reasonable window, do not proceed; surface the open question in the notification instead.

Steps to execute after Alvin confirms the forecast plan:

1. Invoke the supply-demand-planner skill. Read SKILL.md and any reference files under references/ that the skill calls for during the run.

2. Pull actuals — Shopify (DTC + UBM by sales-channel attribution: Web Store = DTC, UBM = UBM), Logiwa shipments, and Amazon. Manual CSV upload is the fault-tolerant fallback if either source is unavailable. Apply the sell-through to sell-in conversion per references/wholesale-conversion.md for UBM and Amazon.

3. Run the baseline forecast off the confirmed forecast_plan: trailing velocity × seasonality factor × manual overrides, SKU × channel × month. New launches use analogue method per references/analogue-selection.md — propose an analogue, request Nicole (PD lead) and Soraya (Brand lead) to ratify before the forecast commits.

4. Apply auto-adjustments. Read latest signals from sjs-comp-intel and sjs-retail-intel. Apply factors per references/auto-adjustment-rules.md. Every adjustment must surface in the run summary with signal source, signal date, math applied, and before/after numbers.

5. Compute targets — safety-stock days, reorder points, target DSI per SKU × channel. Preview, then commit to inventory_targets via plm-assistant (the only PLM writer).

6. Recommend buys — finished goods (vendor, target ship-by, qty, rationale) and components after BOM explosion per references/component-explosion-flow.md.

7. Lay out the fill calendar at KDC-One (skincare, 70-day lead time) and Vegelabs (cleansing/body, 60-day lead time). Component default lead time 105 days. Bulk-to-fill alignment notes per SKU × month.

8. Auto-flag exceptions per references/exception-thresholds.md: ≥20% forecast variance, post-launch <90 days, days-of-cover <60, or sitting inside a vendor transition window. These pull out of bulk approval for individual review.

9. Stage every write — forecast lines, target resets, auto-adjustments, buy recs. Bulk approval is the default; exceptions approve one at a time. plm-assistant commits all PLM writes.

10. Write outputs to Asana project Sweet July Skin S&OP (GID 1214347479282044, Team SJ Ops GID 1202786171817904):
   - Monthly run summary → Monthly run section (1214374670198667)
   - Buy recs → Buy Recommendations section (1214374670198668)
   - Filler calendar → Filler Schedule section (1214374670198669)
   - Exceptions → Exceptions section (1214374670198670)
   - Risk flags → Risk Watch section (1214374670198671)
   - Prior month's closed items → Archive section (1214374670198672)

11. Hand off — buy recs to purchasing-manager, targets to inventory-manager, one-pager brief to sjs-status-reporter for SJS-branded output per forms/s-and-op-one-pager-brief.md.

Confirmation rule: reads run without confirmation. Every write needs Alvin's approval. Never bypass plm-assistant for PLM writes.

Success criteria:
- Forecast plan confirmed by Alvin before any data pull
- All sections of the run summary populated
- Buy recs and targets staged, awaiting approval
- Exception list surfaced separately for individual review
- One-pager handed to sjs-status-reporter
- Notification to Alvin summarizing what's staged and what needs his decision

Context to preserve across runs:
- The forecast plan to reference is always the one Alvin confirms in Step 0 — never assume. H2 2026 is the current default and lives in PLM as the source of truth.
- UBM launches June 2026; sell-in conversion goes live then
- Brand scope: Sweet July Skin only
- Active channels: DTC, UBM, Amazon (Sephora not yet active)
- PLM Supabase project: ujkabbffvhpewpbttmmy
