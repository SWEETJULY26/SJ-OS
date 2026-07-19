# Quality Dashboard — Page Spec

The HTML quality dashboard at `acb-thelanding.netlify.app/quality-dashboard.html`. Three-tab live page as of v5.7: Weekly (default) = live Function call (existing behavior); Monthly and Quarterly = static JSON snapshot, refreshed by Jobs 2 and 5. No frozen archive pages.

Tab layout intent, breadcrumb formats, and the Function `window` param contract live in `tab-refresh-spec.md`. This file covers per-tab data shape and existing page structure.

---

## 1. Page entry shell (HTML)

Tiny entry file. Same pattern as `inventory-dashboard.html`. Just CSS imports, root div, and three script tags.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Quality Dashboard — AC Brands Internal Hub</title>
  <link rel="stylesheet" href="assets/css/main.css" />
  <link rel="stylesheet" href="assets/css/quality-dashboard.css" />
  <link rel="stylesheet" href="assets/css/editor.css" />
</head>
<body>
  <main id="page-root" class="wrap" data-page="quality-dashboard">
    <div class="loading"><p style="padding:48px 0;">Loading…</p></div>
  </main>

  <script src="assets/js/hub.js" defer></script>
  <script type="module" src="assets/js/quality-dashboard.js" defer></script>
  <script src="assets/js/editor.js" defer></script>
</body>
</html>
```

The `data-page="quality-dashboard"` attribute is read by `hub.js` for chrome routing.

---

## 2. Page module (`assets/js/quality-dashboard.js`)

Module pattern matching `inventory-dashboard.js`. Public structure:

```javascript
const QUALITY = {
  rollup: null,        // composed rollup from sjs-quality-rollup function
  filters: { ... },    // section-specific filters as needed
  selectedSection: 'overview',

  async init() {
    await this.ensureReady();
    this.renderShell();
    try {
      await this.loadRollup();
      this.renderSections();
    } catch (err) {
      this.renderError(err.message || String(err));
    }
  },

  async ensureReady() { /* same pattern as inventory-dashboard ensureReady */ },

  async loadRollup() {
    const res = await fetch('/.netlify/functions/sjs-quality-rollup', { cache: 'no-store' });
    if (!res.ok) throw new Error(`Rollup function HTTP ${res.status}`);
    this.rollup = await res.json();
  },

  renderShell() { /* injects header partial via fetch + Hub chrome bindings */ },
  renderSections() { /* renders each of the 6 sections per §3 below */ },
  renderError(msg) { /* "rollup unavailable" banner with retry button */ },
};

document.addEventListener('DOMContentLoaded', () => QUALITY.init());
```

Per memory: call `Hub.bindNav()` and `Hub.bindEditMode()` after `renderShell` injects the header. Without that the Functions ▾ dropdown won't open.

---

## 3. Page sections (Weekly tab — default)

These sections render inside the Weekly tab. Anchor IDs are stable so users can deep-link within the tab.

**Data sources for the Weekly tab:**

1. Live: `/.netlify/functions/sjs-quality-rollup?window=weekly` (default if omitted) — returns the live Asana-composed rollup with the detailed sections below.
2. Fallback: `data/quality-weekly-snapshot.json` — the most recent §1 weekly digest payload written by Job 6 on each scheduled push. Served by the Function automatically when the live computation fails (Asana unreachable, env var missing). Dashboard shows a "showing last digest" banner when this path is used.

The §1 digest payload is a summary — counts plus top priorities — so the fallback render is simpler than the live render. Live render uses the full per-section detail; fallback render uses the digest summary.

### 3.1 Overview (`#overview`)

Top-of-page. RAG color, headline summary, last refresh timestamp. Sourced from quality-manager's most recent project status update.

- RAG: Green / Amber / Red badge
- Summary: 1-2 sentences from the latest project status
- Last refresh: ISO timestamp of the rollup function call
- "View latest project status" link to the underlying Asana project

### 3.2 CAPA & NCR (`#capa`)

From capa-coordinator (SJS CAPA Log).

- Open CAPAs by Status (Inbound, NCR Review, Investigation, Action Plan, Implementation, Verification & Effectiveness)
- Pending QA Lead gates (count + list of CAPA numbers)
- Overdue actions (count)
- Recent closes (last 30 days, count + list)
- Link to SJS CAPA Log Asana project

### 3.3 Lab Findings (`#lab`)

From quality-lab-coordinator (SJS Quality Management Lab Findings sections).

- Open LFs by Classification (OOS, OOT, Incoming Defect, Pattern, In-Spec Flag)
- Vendor flags pending QA Lead review
- Scorecard signals posted (last 30 days)
- Recent CAPA handoffs (last 30 days)
- Link to the Lab Findings Open section in SJS Quality Management

### 3.4 Batch Lifecycle (`#batches`)

From batch-lifecycle-tracker (SJS Quality Management Batch sections).

- Active batches in market (count)
- On Hold count by Hold Reason (Lab fail, Complaint trend, Vendor signal, Regulatory observation, Internal flag, Other)
- Hold/Release Review pending QA Lead
- Stability tests due in next 30 days
- Near-expiry batches at 90/60/30-day thresholds (cross-cut from inventory-manager)
- Link to the Batch — Active in Market section

### 3.5 Customer Complaints (`#complaints`)

From complaint-and-event-handler (SJ Skin Complaint Log).

- Open complaints by category
- Trend signals fired (last 30 days)
- SAE flags (count + flag indicator)
- Recall triggers (count + flag indicator if any)
- Link to SJ Skin Complaint Log

### 3.6 SOPs (`#sops`)

From quality-manager (SOP Catalog pinned task).

- Catalog table: SOP number, title, current revision, effective date, ratification status, next review due
- Pending ratifications (count + list)
- Annual reviews due in next 90 days
- Link to the SOP Catalog Asana task

### 3.7 QoS Signal (`#qos`)

From quality-manager Job 3 (QoS aggregation).

- Current metrics: On-Time Delivery Rate, Fulfillment Rate, Damage Rate, Missing/Incorrect Rate, Fulfillment Complaint Trend
- Each metric shows current value, threshold, status (within / crossed)
- Threshold-crossed tasks (count + list)
- Link to QoS Signal section

### 3.8 Cross-cutting (`#cross-cutting`)

From quality-manager Job 4 (cross-cutting tasks).

- Open tasks by Cross-cutting Type (SOP Annual Review, Audit Prep, Retailer Questionnaire, Regulatory Inspection, Quality System Review, QoS Threshold Crossed)
- Pending QA Lead approval count
- Upcoming due dates (next 30 days)
- Link to Cross-cutting Tasks section

### 3.9 Footer — Recent snapshots

Simple list of the last 12 monthly archive links. New month gets prepended at each Job 2 run.

```
Recent snapshots:
- April 2026 (link)
- March 2026 (link)
- February 2026 (link)
...
```

---

## 4. Monthly tab data shape

The Monthly tab consumes the `quality-manager` Job 7 payload defined in `quality-manager/references/cadence-composition-spec.md` §2. Refreshed by Job 2 in this skill.

**Data source priority on page load:**

1. Function: `/.netlify/functions/sjs-quality-rollup?window=monthly` — serves the latest `data/quality-monthly-snapshot.json` payload.
2. Static fallback: `data/quality-monthly-snapshot.json` (if the Function 5xx's, the page reads this directly).

**Payload shape (§2 summary — see canonical spec for full schema):**

- `as_of_iso`, `window: "monthly"`, `month_label`, `prior_month_label`
- `rag`, `headline`
- `metrics`: object keyed by metric name (capa_opened, capa_closed, complaints_opened, complaint_rate_per_1000_orders, sae_count, recall_count, oos_count, oot_count, vendor_flags_raised, batches_released, batches_placed_on_hold, stability_tests_completed, qos_on_time_delivery_pct_avg, qos_fulfillment_pct_avg, plus capa_aging_avg_days, ncr_opened, ncr_closed). Each metric: `{ current, prior, delta, trend: "up"|"down"|"flat" }`.
- `narratives`: `{ what_drove_the_month, notable_signals, watch_items_for_next_month }`

**First-run-with-no-priors behavior:** counts default to 0, percentage fields stay `null`, trend forced to `flat`. The dashboard renders normally with the "no prior data" implication baked into the flat trend arrows.

**Tab layout intent:** see `tab-refresh-spec.md` → Monthly tab layout. Lower-is-better metrics (complaints, OOS, OOT, holds) render trend arrows with reversed color semantics — green = down, red = up.

---

## 5. Quarterly tab data shape

The Quarterly tab consumes the `quality-manager` Job 8 payload defined in `quality-manager/references/cadence-composition-spec.md` §3. Refreshed by Job 5 in this skill.

**Data source priority on page load:**

1. Function: `/.netlify/functions/sjs-quality-rollup?window=quarterly` — serves the latest `data/quality-quarterly-snapshot.json` payload.
2. Static fallback: `data/quality-quarterly-snapshot.json`.

**Payload shape (§3 summary — see canonical spec for full schema):**

- `as_of_iso`, `window: "quarterly"`, `quarter_label`, `prior_quarter_label`
- `rag`, `headline`
- `metrics`: same metric set as Monthly, aggregated quarterly. Adds `capa_closure_rate_pct`.
- `quarterly_only`: `{ sop_annual_review_cycle_progress_pct, audits_completed_in_quarter: [], audits_planned_next_quarter: [], retailer_questionnaires_responded, retailer_questionnaires_pending, regulatory_inspections_in_quarter: [] }`
- `narratives`: `{ quarter_recap, trends_emerging, focus_for_next_quarter, founder_signal_for_ayesha_briefing }`
- `handoffs`: `{ sjs_status_reporter_comment_draft, ayesha_weekly_briefing_comment_draft }` — staged for Operator approval before posting

**Tab layout intent:** see `tab-refresh-spec.md` → Quarterly tab layout. Includes the SOP review cycle progress bar, audits list, retailer questionnaires summary, regulatory inspections list, four narratives, and a small handoff status indicator showing whether the two staged comments have been approved and posted.

---

## 6. CSS spec (`assets/css/quality-dashboard.css`)

Match the visual language of inventory-dashboard.css. Key elements:

- Section cards with rounded corners, subtle shadow
- RAG badges (Green / Amber / Red) — use main.css color tokens if defined, or define inline tokens here
- Number callouts for headline counts (e.g., open CAPAs)
- Tables for CAPA list, SOP catalog, threshold list — same table treatment as inventory-dashboard's batch table
- Loading skeleton for sections waiting on Function response
- Error banner styling for rollup-unavailable state

Mobile responsive: stack sections vertically on narrow viewports.

---

## 7. Loading and error states

**Loading:** skeleton boxes per section while the Function call is in flight. Shows the section headers immediately so users know what's coming.

**Error — rollup unavailable:** red banner at top of page, message: "Quality rollup is currently unavailable. Live data may be delayed. Try refreshing in a moment, or check the latest project status update on the [SJS Quality Management Asana project](URL)."

**Error — Function 5xx or timeout:** same banner, plus a "Retry" button that re-calls the Function.

**Error — Function returns partial data (some sub-skills failed to read):** soft banner ("Some sub-skill data is unavailable: [list]") above sections that have data; affected sections show their own "section unavailable" placeholder.

---

## 8. Refresh behavior

- Weekly tab (default): refreshes on every page load via Function call with `?window=weekly` (or no param). No client-side caching beyond the Function's own `Cache-Control: public, max-age=300, stale-while-revalidate=60`.
- Monthly tab: reads `?window=monthly` (Function serves the latest snapshot JSON). Refreshed by Job 2 first business day of month.
- Quarterly tab: reads `?window=quarterly`. Refreshed by Job 5 first business day of Jan/Apr/Jul/Oct.
- All tabs share the same cache headers. Static JSON snapshots serve as fallback when the Function 5xx's.

---

## 9. Edit mode

Per memory, `editor.js` self-initializes on hub pages and owns Cmd/Ctrl+Shift+E and `?edit=1`. The dashboard inherits this for free. No special edit-mode logic required for v5.7.
