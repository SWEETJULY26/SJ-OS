# S&OP one-pager brief

This is what the skill hands sjs-status-reporter at the end of each monthly
run. sjs-status-reporter wraps the content in Sweet July Skin brand
(Pava Brown / Bone / Soursop, GT America Expanded + Adrianna, warm Irie tone)
and produces the final one-pager.

The brief is structured input for sjs-status-reporter, not the final output.

## Brief shape

```yaml
report_type: s_and_op_one_pager
run_id: [UUID]
run_period: [YYYY-MM]
generated_at: [ISO timestamp]
brand: sweet-july-skin
intended_audience: [internal | leadership]

headline:
  text: [one-sentence run summary]
  rag_status: [green | yellow | red]

forecast_snapshot:
  total_dtc_units: [N]
  total_ubm_units: [N]
  total_amazon_units: [N]
  vs_prior_run_pct: [+/-N%]
  active_skus: [N]

major_movements:
  - sku: [name]
    channel: [dtc | ubm | amazon]
    direction: [up | down]
    magnitude_units: [N]
    magnitude_pct: [N]
    reason: [one line]
  # 3 to 5 entries max — only the meaningful movers

upcoming_buys:
  total_estimated_spend: $[N]
  finished_good_count: [N]
  component_count: [N]
  notable_items:
    - [vendor, qty, target_ship_by, why it matters]
  # 3 to 5 highlights, not full list

filler_calendar:
  kdc_one_runs: [N]
  vegelabs_runs: [N]
  notable_runs:
    - [filler, sku, target_month, why noteworthy]
  # 2 to 3 highlights

risks:
  - type: [stockout | overstock | vendor_transition | lead_time | other]
    description: [one line]
    affected_skus: [list]
    mitigation: [one line]
  # all open risks; one line each

approvals_pending:
  exception_count: [N]
  bulk_approval_status: [pending | clear]
  reviewer_count: [N — distinct reviewers needed]

links:
  asana_run_task: [URL]
  plm_plan_a: [UUID]
  plm_plan_b: [UUID]

confidence_notes:
  - [any signals that are stale, any forecasts particularly thin on data]
```

## How sjs-status-reporter wraps this

sjs-status-reporter takes the YAML brief and:
1. Generates a one-page document (markdown or PPTX, configurable per request)
2. Applies Sweet July Skin brand (palette, typography, header art, tone)
3. Uses warm voice for narrative sections (headline, why-it-matters)
4. Uses crisp tabular voice for data sections (snapshot, calendar, buys)
5. Adds an executive header note when intended_audience = leadership

## When the brief generates

After bulk approval clears (all exceptions resolved, all writes committed
via plm-assistant). The brief is the final artifact of the run.

## What the brief does NOT contain

- Row-by-row forecast data (lives in PLM)
- Full buy recommendation list (lives in Asana)
- Full filler schedule (lives in Asana)
- Run-level math and adjustment trail (lives in monthly run summary task)

The brief is a digest. sjs-status-reporter produces a digest output. People
who want detail follow the links into Asana or PLM.

## Sample brief

```yaml
report_type: s_and_op_one_pager
run_id: 8a3f-...
run_period: 2026-05
generated_at: 2026-05-01T08:00:00Z
brand: sweet-july-skin
intended_audience: leadership

headline:
  text: May S&OP locked. UBM pre-launch buffer build is on track for June 2026 go-live.
  rag_status: green

forecast_snapshot:
  total_dtc_units: 18,500
  total_ubm_units: 24,000
  total_amazon_units: 4,200
  vs_prior_run_pct: +8
  active_skus: 7

major_movements:
  - sku: Pava Toner
    channel: ubm
    direction: down
    magnitude_units: -800
    magnitude_pct: -10
    reason: Rhode toner launch — direct comp auto-adjustment
  - sku: Castaway Cream
    channel: dtc
    direction: up
    magnitude_units: +1,200
    magnitude_pct: +15
    reason: Manual override for August PR push

upcoming_buys:
  total_estimated_spend: $142,500
  finished_good_count: 3
  component_count: 11
  notable_items:
    - [Element Packaging, 14,500 jars, 2026-06-30, Anchors Castaway Aug fill]
    - [HCT, 8,500 bottles, 2026-06-15, Anchors Pava Toner UBM launch]
    - [KDC-One, 12,000 units fill, 2026-08-15, August UBM ship-in]

filler_calendar:
  kdc_one_runs: 3
  vegelabs_runs: 1
  notable_runs:
    - [KDC-One, Castaway Cream, 2026-05, Drives August UBM pipe]
    - [Vegelabs, Soursop Cleanser, 2026-05, Drives August UBM launch SKU]

risks:
  - type: vendor_transition
    description: Element to Impress secondary transition starts 2026-09-01
    affected_skus: Castaway Cream, Pava Toner secondary cartons
    mitigation: All Q3 buys placed before transition; first transition order is October
  - type: lead_time
    description: Pava Toner first KDC-One run is tight against June launch
    affected_skus: Pava Toner
    mitigation: Confirmed expedited bulk transfer; status weekly until launch

approvals_pending:
  exception_count: 0
  bulk_approval_status: clear
  reviewer_count: 0

links:
  asana_run_task: https://app.asana.com/...
  plm_plan_a: 1f...
  plm_plan_b: 2a...

confidence_notes:
  - UBM pre-launch forecast is fully manual (per scope). Confidence is medium.
  - sjs-comp-intel last refresh: 2026-04-22 (8 days old, current).
  - sjs-retail-intel benchmark: not yet active (UBM pre-launch).
```
