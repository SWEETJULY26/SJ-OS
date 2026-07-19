# Netlify Function Spec — `sjs-quality-rollup.js`

The live data Function for the quality dashboard. Reads SJS Quality Management Asana state and composes a rollup JSON.

Path: `/Users/alvinbelt/Downloads/acb-thelanding/netlify/functions/sjs-quality-rollup.js`

Pattern reference: `netlify/functions/sjs-pd-stats.js` (the existing PD live stats function — same shape, fail-graceful).

---

## 0. `window` query parameter (v5.7 four-cadence dispatch)

The Function accepts a `window` query param to dispatch between the three dashboard tabs:

| Param value | Behavior | Auth required |
|---|---|---|
| `?window=weekly` (default if omitted) | Live computation against Asana. Returns the existing detailed rollup (overview / capa / lab / batches / complaints / cross-cutting / qos). On Asana failure, falls back to `data/quality-weekly-snapshot.json` (§1 digest payload) so the page shows the last composed digest instead of an empty error state. | `ASANA_PAT` for live path; none for fallback read |
| `?window=monthly` | Serves the static snapshot at `data/quality-monthly-snapshot.json`. No live Asana hit. Refreshed by Job 2 first business day of month. | None — static read |
| `?window=quarterly` | Serves the static snapshot at `data/quality-quarterly-snapshot.json`. No live Asana hit. Refreshed by Job 5 first business day of Jan/Apr/Jul/Oct. | None — static read |

**Dispatch rule:** read `event.queryStringParameters.window`. If missing, undefined, or any value other than `"monthly"` or `"quarterly"`, treat as `"weekly"` (default path, current live logic).

**Static read pattern (monthly + quarterly):**
- Read the JSON file from the build output. If it doesn't exist yet (first cadence run hasn't fired), return 200 with `rollup: null` and `error: "snapshot not yet generated"` so the dashboard shows a graceful empty-state banner.
- Cache headers stay `public, max-age=300, stale-while-revalidate=60` (same as weekly).
- No pagination, no Asana fetch, no `ASANA_PAT` dependency.

**Weekly fallback pattern:**
- The live path runs the existing rollup logic against Asana, untouched.
- If the live computation throws or returns `rollup: null` with an error (Asana unreachable, `ASANA_PAT` missing, etc.) AND `data/quality-weekly-snapshot.json` exists, return that snapshot payload (§1 shape) with a flag `source: "weekly-snapshot-fallback"` so the dashboard can show a "showing last digest" banner.
- If neither the live path nor the snapshot is available, return the existing 200 + `rollup: null` + `error` shape.

---

## 1. Required env vars

- `ASANA_PAT` — Asana Personal Access Token. Already set in Netlify; no change needed. If missing, the Function returns 200 with `error` populated and `rollup: null` so the page can show the error banner gracefully.

---

## 2. Constants (project + section GIDs)

```javascript
// SJS Quality Management project
const PROJECT_GID = '1214660401644163';

// Sections (cached 2026-05-09 — all 16 sections live)
const SECTION_GIDS = {
  // v5.3 — quality-lab-coordinator
  inboundStaging:           '1214660401653157',
  labFindingsOpen:          '1214660713569696',
  vendorFlagReview:         '1214661413440412',
  scorecardSignalPosted:    '1214660194909535',
  capaHandedOff:            '1214660401653221',
  watchList:                '1214660713569760',
  closed:                   '1214660716447873',
  // v5.4 — batch-lifecycle-tracker
  batchActiveInMarket:      '1214660393603698',
  batchStabilitySchedule:   '1214660393603699',
  batchHoldReleaseReview:   '1214660393603700',
  batchOnHold:              '1214660700812912',
  batchWatch:               '1214660700812911',
  batchClosed:              '1214660700812913',
  // v5.5 — quality-manager
  crossCuttingTasks:        '1214660700812914',
  sopCatalog:               '1214660700812917',
  qosSignal:                '1214660700812918',
};

// Cross-skill projects (read for cross-skill rollup)
const SJS_CAPA_LOG_GID    = '1214660784338465'; // capa-coordinator owns
const SJ_COMPLAINT_LOG_GID = '1204763097184846';
const AC_PURCHASING_GID    = '1214373717266702'; // for vendor flag context

// SOP Catalog pinned task (single source for SOP section)
const SOP_CATALOG_TASK_GID = '1214661441506629';
```

The Function maintains these as constants. Updates happen via skill regeneration when GIDs change.

---

## 3. Response shape

```javascript
{
  rollup: {
    overview: {
      rag: 'green' | 'amber' | 'red',
      summary: string,
      last_status_update: ISO string,
    },
    capa: {
      open_count: number,
      by_status: { 'Inbound': N, 'NCR Review': N, ... },
      pending_qa_lead: { count: number, items: [{ gid, name }] },
      overdue_actions: number,
      recent_closes_30d: { count: number, items: [{ gid, name, closed_at }] },
      project_url: string,
    },
    lab: {
      open_count: number,
      by_classification: { 'OOS': N, 'OOT': N, ... },
      vendor_flags_pending: { count: number, items: [...] },
      scorecard_signals_30d: number,
      capa_handoffs_30d: number,
      section_url: string,
    },
    batches: {
      active_count: number,
      on_hold_by_reason: { 'Lab fail': N, 'Complaint trend': N, ... },
      hold_release_pending: { count: number, items: [...] },
      stability_due_30d: { count: number, items: [...] },
      near_expiry: { '90d': N, '60d': N, '30d': N },
      section_url: string,
    },
    complaints: {
      open_count: number,
      by_category: { ... },
      trend_signals_30d: number,
      sae_flags: number,
      recall_triggers: number,
      project_url: string,
    },
    sops: {
      catalog: [
        { number, title, revision, effective, status, next_review_due, mirror_path },
        ...
      ],
      pending_ratifications: [...],
      annual_reviews_due_90d: [...],
      catalog_task_url: string,
    },
    qos: {
      metrics: {
        on_time_delivery: { value, threshold, status: 'within'|'crossed', window },
        fulfillment_rate: { ... },
        damage_rate: { ... },
        missing_incorrect_rate: { ... },
        fulfillment_complaint_trend: { ... },
      },
      threshold_crossed_tasks: { count: number, items: [...] },
      section_url: string,
    },
    cross_cutting: {
      open_count: number,
      by_type: { 'SOP Annual Review': N, 'Audit Prep': N, ... },
      pending_qa_lead: number,
      upcoming_30d: { count: number, items: [...] },
      section_url: string,
    },
  },
  last_updated: ISO string,
  source: 'asana',
  partial: {
    // Populated only if some sub-queries failed. Lists which sections have stale or missing data.
    // Page renders sections with data; flagged sections show "section unavailable".
    sections: ['lab', 'qos', ...],
    errors: { lab: 'Asana 503', ... },
  } | null,
}
```

On total failure: `{ rollup: null, error: string, last_updated: ISO string }` per the inventory-dashboard / sjs-pd-stats fail-graceful pattern.

---

## 4. Asana queries needed

| Section | Query | Notes |
|---|---|---|
| Overview | `GET /projects/{PROJECT_GID}/project_statuses?limit=1` | Latest project status update — pulls RAG color, title, text |
| CAPA | `GET /projects/{SJS_CAPA_LOG_GID}/tasks` filtered by `Status` field options | Counts by Status; filter for Pending QA Lead; overdue actions need due_on comparison |
| Lab | `GET /sections/{labFindingsOpen}/tasks` | Counts by `Classification` field |
| Lab vendor flags | `GET /sections/{vendorFlagReview}/tasks` | Pending QA Lead count |
| Lab scorecard signals | `GET /sections/{scorecardSignalPosted}/tasks?completed_since=NOW-30d` | Last 30 days |
| Lab CAPA handoffs | `GET /sections/{capaHandedOff}/tasks?completed_since=NOW-30d` | Last 30 days |
| Batches | `GET /sections/{batchActiveInMarket}/tasks`, `GET /sections/{batchOnHold}/tasks` (filter by Hold Reason custom field), `GET /sections/{batchHoldReleaseReview}/tasks` (filter by Pending QA Lead), `GET /sections/{batchStabilitySchedule}/tasks` (filter by due_on within 30 days), `GET /sections/{batchWatch}/tasks` | All section GIDs cached |
| Complaints | `GET /projects/{SJ_COMPLAINT_LOG_GID}/tasks` | By category custom field |
| SOPs | `GET /tasks/{SOP_CATALOG_TASK_GID}` | Parse the description for the catalog table |
| QoS metrics | Cross-call to oc3pl-order-manager OC3PL Order Management project + SJ Shipping Dashboard | See qos-thresholds.md in quality-manager for source-field mappings |
| Cross-cutting | `GET /sections/{crossCuttingTasks}/tasks` (filter by `Cross-cutting Type` and Pending QA Lead) | Section GID cached |

Pagination per memory: project pagination + completed_since + PT timezone + mirror chart filters. Use `limit=100` with offset paging where necessary.

---

## 5. Performance and caching

- `Cache-Control: public, max-age=300, stale-while-revalidate=60` (5-minute browser cache, 1-minute stale-while-revalidate). Same as sjs-pd-stats.
- Total query budget: under 10 Asana API calls per Function execution. Parallelize with `Promise.all` where queries are independent.
- Function timeout: Netlify Functions default is 10 seconds. Aim for under 5s.

---

## 6. Error handling pattern

Per the sjs-pd-stats / inventory-dashboard pattern: never return non-200. Always 200 with structured error.

```javascript
exports.handler = async () => {
  const pat = process.env.ASANA_PAT;
  if (!pat) {
    return json(200, { rollup: null, error: 'ASANA_PAT env var not set', last_updated: new Date().toISOString() });
  }
  try {
    // ... parallel Asana calls ...
    return json(200, { rollup, last_updated, source: 'asana', partial: partialOrNull }, 'public, max-age=300, stale-while-revalidate=60');
  } catch (err) {
    return json(200, { rollup: null, error: String((err && err.message) || err), last_updated: new Date().toISOString() });
  }
};
```

Per-section failures: catch inside the parallel batch, log to the `partial.errors` map, render the rest. The page handles partials gracefully per `dashboard-spec.md` §6.

---

## 7. Helper utilities

Same pattern as sjs-pd-stats:

```javascript
function json(status, body, cacheControl) {
  return {
    statusCode: status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': cacheControl || 'no-store',
    },
    body: JSON.stringify(body),
  };
}

async function asanaFetch(path, pat) {
  const url = `https://app.asana.com/api/1.0${path}`;
  const res = await fetch(url, {
    headers: { Authorization: `Bearer ${pat}`, Accept: 'application/json' },
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Asana ${res.status}: ${body.slice(0, 200)}`);
  }
  return res.json();
}
```

---

## 8. Open at first build

- ~~Batch and Cross-cutting section GIDs~~ **Resolved 2026-05-09** — all 16 section GIDs cached above.
- The QoS source-field mappings depend on oc3pl-order-manager Daily Report Log task structure. Confirm field paths before wiring the QoS pull.
- ~~The SJS CAPA Log project GID is unknown — capa-coordinator first-run setup creates it.~~ **Resolved 2026-05-09** — SJS CAPA Log project created at gid `1214660784338465`.
- ~~Custom field GIDs are still pending~~ **Resolved 2026-05-09** — all 30 fields cached. Canonical reference: `asana-field-gids.md` in the skill builder root. Function uses field GIDs to bucket Hold Reason, Cross-cutting Type, QoS Metric, and to count Pending QA Lead.
