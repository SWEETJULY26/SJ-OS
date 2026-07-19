# Tab Refresh Spec — quality-status-reporter Jobs 2, 5, 6

Defines what each cadence renders into the dashboard and the breadcrumb comment shape that posts to the Quality Sweep Running Log.

## Tab layout intent

The dashboard has three tabs after this build:

| Tab | Default | Refreshed by | Cadence | Data source |
|---|---|---|---|---|
| Weekly (default) | yes | Job 6 | Monday 7:30 AM PT | `quality-manager` Job 6 payload |
| Monthly | no | Job 2 | First business day of month, 7 AM PT | `quality-manager` Job 7 payload |
| Quarterly | no | Job 5 | First business day of Jan/Apr/Jul/Oct, 7 AM PT | `quality-manager` Job 8 payload |

All three tabs share the Hub shell pattern (header, nav, footer, brand styling). Tab content varies by cadence.

## Function param contract

`netlify/functions/sjs-quality-rollup.js` accepts a `window` query parameter:

- `?window=weekly` (default if omitted) — returns the live Asana-computed rollup. Job 6 also writes a digest snapshot to `data/quality-weekly-snapshot.json` so the most recent composed weekly digest is preserved on disk.
- `?window=monthly` — returns monthly rollup payload (latest snapshot at `data/quality-monthly-snapshot.json`)
- `?window=quarterly` — returns quarterly rollup payload (latest snapshot at `data/quality-quarterly-snapshot.json`)

The Function does not recompute monthly or quarterly on each load — it reads from the static JSON files that the cadence jobs write. Weekly is computed live by default; if the live computation fails (Asana unreachable, `ASANA_PAT` missing), the Function falls back to serving `data/quality-weekly-snapshot.json` so the page shows the most recent composed digest rather than an empty error state.

## Weekly tab layout (existing — minor adjustment)

No structural change. Today's dashboard becomes the Weekly tab content. Add a tab nav at the top, default to Weekly, but otherwise keep the existing layout.

## Monthly tab layout

Suggested sections — tune in Claude Code:

1. **Header** — Month label (e.g., "May 2026"), as-of timestamp, RAG indicator, one-sentence headline
2. **Month-over-month metric grid** — cards showing each metric's current value, prior value, delta, and trend arrow. Group cards by domain: CAPA/NCR, Complaints, Lab, Batches, QoS.
3. **Narratives** — three short prose blocks: what drove the month, notable signals, watch items for next month.
4. **Drill-down links** — links to relevant Asana sections for the highest-priority items.

Lower-is-better metrics (complaints, OOS, holds) should show a green arrow when trending down and red when trending up. Higher-is-better metrics (closures, QoS rates) show the reverse.

## Quarterly tab layout

Suggested sections — tune in Claude Code:

1. **Header** — Quarter label (e.g., "Q2 2026"), as-of timestamp, RAG indicator, one-sentence headline
2. **Quarter-over-quarter metric grid** — same metric set as Monthly, aggregated quarterly. Group by domain.
3. **Quarterly-only block** — SOP review cycle progress bar, audits completed, audits planned, retailer questionnaires summary, regulatory inspections list.
4. **Narratives** — quarter recap, trends emerging, focus for next quarter, founder signal callout (pulled into Ayesha briefing).
5. **Handoff status** — small indicator showing whether the `sjs-status-reporter` and `ayesha-weekly-briefing` handoff comments have been approved and posted.

## Breadcrumb comment format

Posts to the Quality Sweep Running Log task in SJS Quality Management → Cross-cutting Tasks section.

### Weekly digest breadcrumb (Job 6)

```
[Weekly Quality Digest — YYYY-MM-DD]

RAG: <green | yellow | red>
Headline: <one sentence>

Top priorities this week:
1. <title> (<section>)
2. <title> (<section>)
3. <title> (<section>)

View dashboard: https://acb-thelanding.netlify.app/quality-dashboard.html
```

### Monthly tab refresh breadcrumb (Job 2)

```
[Monthly Quality Tab Refreshed — <Month YYYY>]

RAG: <green | yellow | red>
Headline: <one sentence>

Top deltas vs. prior month:
- <metric>: <current> (<delta> vs prior, <trend>)
- <metric>: <current> (<delta> vs prior, <trend>)
- <metric>: <current> (<delta> vs prior, <trend>)
- <metric>: <current> (<delta> vs prior, <trend>)
- <metric>: <current> (<delta> vs prior, <trend>)

View Monthly tab: https://acb-thelanding.netlify.app/quality-dashboard.html#monthly
```

### Quarterly tab refresh breadcrumb (Job 5)

```
[Quarterly Quality Tab Refreshed — <Quarter YYYY>]

RAG: <green | yellow | red>
Headline: <one sentence>

Quarter recap: <quarter_recap narrative — first 2 sentences>

Trends emerging: <trends_emerging narrative — first sentence>

Founder signal staged for Ayesha briefing: <yes if non-empty, no otherwise>

View Quarterly tab: https://acb-thelanding.netlify.app/quality-dashboard.html#quarterly
```

## Tab anchor links

The dashboard supports URL anchors `#weekly`, `#monthly`, `#quarterly` to deep-link directly to a tab. The breadcrumb comments use these anchors.

## Static fallback

If the Function fails (Asana API down, env var missing, etc.) the dashboard falls back to the static JSON snapshot file for that tab. Show a small banner: "Showing last refresh at [timestamp]. Live data temporarily unavailable."

Snapshot files:
- Weekly: `data/quality-weekly-snapshot.json` — written by Job 6 on each weekly digest push (§1 payload shape)
- Monthly: `data/quality-monthly-snapshot.json` — written by Job 2 on each monthly refresh (§2 payload shape)
- Quarterly: `data/quality-quarterly-snapshot.json` — written by Job 5 on each quarterly refresh (§3 payload shape)

## Commit message convention

For each cadence push, the commit message follows:

- Weekly: `quality dashboard: weekly digest push <YYYY-MM-DD>`
- Monthly: `quality dashboard: monthly tab refresh <Month YYYY>`
- Quarterly: `quality dashboard: quarterly tab refresh <Quarter YYYY>`

Operator sees these commit messages in the HITL gate before push.
