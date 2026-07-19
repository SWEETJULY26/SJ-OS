# Cadence Composition Spec — quality-manager Jobs 6, 7, 8

Defines the payload contract for each of the three new cadence composition jobs. `quality-status-reporter` consumes these payloads to render the live dashboard tabs.

## §1 — Weekly digest payload (Job 6)

Returns the standard System B rollup. Same data Job 2 already produces; the wrapper exists so cadence callers have a stable contract.

```json
{
  "as_of_iso": "2026-05-18T07:30:00-07:00",
  "window": "weekly",
  "rag": "green | yellow | red",
  "headline": "<one sentence>",
  "open_capa_count": 0,
  "open_ncr_count": 0,
  "pending_qa_lead_gates": 0,
  "open_complaints_count": 0,
  "complaints_with_trend_break": [],
  "open_sae_count": 0,
  "open_recall_count": 0,
  "open_oos_count": 0,
  "open_oot_count": 0,
  "vendor_flags_pending": 0,
  "active_batches_count": 0,
  "batches_on_hold": 0,
  "near_expiry_batches": [],
  "stability_tests_due_this_week": [],
  "qos_metrics": {
    "on_time_delivery_pct": null,
    "fulfillment_pct": null,
    "damage_rate_pct": null,
    "missing_rate_pct": null,
    "fulfillment_complaint_rate_pct": null
  },
  "qos_thresholds_crossed": [],
  "sops_pending_ratification": [],
  "sops_due_for_review_30_days": [],
  "cross_cutting_tasks_open": [],
  "top_priorities": [
    { "title": "", "section": "", "asana_gid": "" }
  ]
}
```

## §2 — Monthly operational rollup payload (Job 7)

Current month vs. prior month. All deltas signed (positive = increase from prior period). Trend direction is `up | down | flat` based on a 5% deadband.

```json
{
  "as_of_iso": "2026-06-01T07:00:00-07:00",
  "window": "monthly",
  "month_label": "May 2026",
  "prior_month_label": "April 2026",
  "rag": "green | yellow | red",
  "headline": "<one sentence>",
  "metrics": {
    "capa_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "capa_closed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "capa_aging_avg_days": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "ncr_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "ncr_closed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "complaints_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "complaint_rate_per_1000_orders": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "sae_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "recall_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "oos_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "oot_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "vendor_flags_raised": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "batches_released": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "batches_placed_on_hold": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "stability_tests_completed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "qos_on_time_delivery_pct_avg": { "current": null, "prior": null, "delta": null, "trend": "flat" },
    "qos_fulfillment_pct_avg": { "current": null, "prior": null, "delta": null, "trend": "flat" }
  },
  "narratives": {
    "what_drove_the_month": "",
    "notable_signals": "",
    "watch_items_for_next_month": ""
  }
}
```

Narratives are short prose (1–3 sentences each), composed from the highest-priority items in the month. Operator can override before push.

## §3 — Quarterly operational rollup payload (Job 8)

Current quarter vs. prior quarter. Same metric set as §2 but quarterly aggregation. Adds quarterly-only fields: SOP review cycle progress, audit prep state, retailer questionnaire activity.

```json
{
  "as_of_iso": "2026-07-01T07:00:00-07:00",
  "window": "quarterly",
  "quarter_label": "Q2 2026",
  "prior_quarter_label": "Q1 2026",
  "rag": "green | yellow | red",
  "headline": "<one sentence>",
  "metrics": {
    "capa_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "capa_closed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "capa_aging_avg_days": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "capa_closure_rate_pct": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "ncr_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "ncr_closed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "complaints_opened": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "complaint_rate_per_1000_orders": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "sae_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "recall_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "oos_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "oot_count": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "vendor_flags_raised": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "batches_released": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "batches_placed_on_hold": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "stability_tests_completed": { "current": 0, "prior": 0, "delta": 0, "trend": "flat" },
    "qos_on_time_delivery_pct_avg": { "current": null, "prior": null, "delta": null, "trend": "flat" },
    "qos_fulfillment_pct_avg": { "current": null, "prior": null, "delta": null, "trend": "flat" }
  },
  "quarterly_only": {
    "sop_annual_review_cycle_progress_pct": 0,
    "audits_completed_in_quarter": [],
    "audits_planned_next_quarter": [],
    "retailer_questionnaires_responded": 0,
    "retailer_questionnaires_pending": 0,
    "regulatory_inspections_in_quarter": []
  },
  "narratives": {
    "quarter_recap": "",
    "trends_emerging": "",
    "focus_for_next_quarter": "",
    "founder_signal_for_ayesha_briefing": ""
  },
  "handoffs": {
    "sjs_status_reporter_comment_draft": "",
    "ayesha_weekly_briefing_comment_draft": ""
  }
}
```

`founder_signal_for_ayesha_briefing` is a 1–2 sentence pull-out for the Ayesha briefing source pool. Empty string if no founder-level signal surfaced in the quarter.

`handoffs.*` are draft comments staged for Operator approval. They post only after explicit approval.

## Period boundaries

- Weekly: trailing 7 calendar days from `as_of_iso`.
- Monthly: calendar month preceding the run. Job 7 fires on first business day of the month — the month being rolled up is the prior calendar month.
- Quarterly: calendar quarter preceding the run. Job 8 fires on first business day of Jan/Apr/Jul/Oct — the quarter being rolled up is the prior calendar quarter.

## Trend deadband

`delta / max(abs(prior), 1) * 100`. If absolute value ≤ 5%, trend = `flat`. Otherwise `up` or `down` based on sign. Lower-is-better metrics (e.g., complaints, OOS, holds) flip the interpretation in narrative composition but the raw `trend` stays directional.

## RAG composition

Both monthly and quarterly use the same RAG logic as Job 2 today. No new logic — just applied to the new aggregation windows.
