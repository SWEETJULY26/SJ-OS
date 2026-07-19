---
name: regulatory-status-reporter
description: Generate the branded HTML regulatory dashboard for Sweet July Skin from regulatory-manager's rollup. Use for regulatory dashboard refresh, monthly snapshot, branded regulatory output, or v6.7 spend strip. Triggers include "regulatory dashboard", "regenerate regulatory dashboard", "branded regulatory update", "monthly regulatory snapshot", "regulatory spend strip", "regulatory update for the team". Reads SJS Regulatory Management (gid 1214660807386611) and SJS Reportable Events (gid 1214660834583706) via Netlify Function, plus regulatory-manager Jobs 8+9 cost rollup for spend strip. Writes Asana attachment in SJS Regulatory Management and the landing hub at acb-thelanding.netlify.app/regulatory-dashboard.html via /Users/alvinbelt/Downloads/acb-thelanding/. Reuses Hub shell (Hub.renderHeader/Nav/Footer in div.page) and Function pattern from sjs-quality-rollup. Never opens tasks, writes sub-skills, or outputs outside HTML. Sister to quality-status-reporter and sjs-status-reporter.
---

# Regulatory Status Reporter

The rendering layer for System C regulatory. Takes regulatory-manager's composed rollup and turns it into a single live HTML dashboard on the AC Brands landing hub plus a monthly snapshot archive. Read-only on data, output-only on writes.

**Post-build update — 2026-05-12 (Pedrero touchbase).** KPI sections expand from four to seven: adds State Packaging Laws, International Markets, and Reformulation Claim-Bridge Watch tiles. These read from new regulatory-manager registration types (CA SB 343, 19-state packaging toxics, EPR, Health Canada Notification, Quebec French-Language Compliance) plus the claims-il-and-label-keeper §7.4 reformulation gate.

**Render pattern lock — 2026-05-12 (v6.6.1 weekly digest landing).** Render pattern shifts from a linear scroll of anchored KPI sections to a single-page weekly digest with Hub shell + KPI row + 5 tabs. Dashboard is static-rendered weekly by `sjs-regulatory-sweep` rather than driven live by the Netlify Function. The Function (`netlify/functions/sjs-regulatory-rollup.js`) stays in the repo but is deprecated until a follow-up decides whether to keep it. This locks the new shape so the next weekly digest doesn't drift back to the linear render.

**Spend strip — 2026-05-12 (v6.7 vendor invoice cost capture).** A new spend strip lands between the KPI row and the tab nav. Reads from regulatory-manager Jobs 8 + 9 monthly + quarterly cost rollups (which read `vendor_invoices` via Supabase SELECT). The strip is rendered, not interactive; hover tooltips drill into the by-vendor and by-cost-category breakdown. Strip is included in monthly archive pages so each frozen snapshot keeps its month's spend state. The Netlify Function `netlify/functions/sjs-regulatory-rollup.js` is extended with a `spend` block; no new function. Brand chrome lock (v6.6.2) holds — strip uses `--surface`, `--rum-cake`, `--soursop`, `--good-youth` tokens from `main.css` and `rd-` prefixed component styles. See **Spend strip (v6.7)** section below for full layout and data shape.

**Chrome lock — 2026-05-12 (v6.6.2 hub chrome alignment).** The page no longer hand-rolls its own header. It uses the same three-file pattern every other hub dashboard uses (quality-dashboard, shipping-dashboard, inventory-dashboard):
- `regulatory-dashboard.html` — thin shell that loads `assets/css/main.css`, `assets/css/regulatory-dashboard.css`, `assets/js/hub.js`, and `assets/js/regulatory-dashboard.js`, with a single `<main id="page-root" class="wrap" data-page="regulatory-dashboard">` mount point.
- `assets/js/regulatory-dashboard.js` — calls `Hub.renderHeader(true)`, `Hub.renderNav('Regulatory Dashboard')`, `Hub.renderFooter()`, then renders the lede + KPI row + 5 tabs, then calls `Hub.bindNav()` and `Hub.bindEditMode()`.
- `assets/css/regulatory-dashboard.css` — scoped `rd-` styles only; brand tokens (`--good-youth`, `--rum-cake`, `--soursop`, `--surface`, etc.) come from `main.css`. No custom warm palette.

Canonical reference page is `quality-dashboard.html`. Canonical template lives at `references/dashboard-template.html` in this skill — every weekly regen starts from that template, swaps the data inside the 5 tabs, and keeps the HTML shell + JS chrome calls + CSS file structure untouched.

## Why this exists

regulatory-manager (v6.3) composes the System C rollup. Without a rendering layer, that rollup lives only in Asana project status updates and on-demand chat replies — neither suits the team's broader visibility need or the founder context that wants something to look at, not read in chat. This skill is the publish step: live HTML that anyone with hub access can scan, and a monthly archive that captures the state for the record.

The skill is intentionally narrow at v6.4: HTML dashboard only, on-demand + monthly auto. PDF, PPTX, and DOCX outputs are explicitly out of scope. The Word docs we ship for SOP filings (SKN-OPS-008, SKN-OPS-009) are one-off and live in their authoring skills.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**Single source of truth: regulatory-manager rollup.** The skill reads from both System C project gids via the Netlify Function but composes the same shape regulatory-manager Job 2 composes. Never reads sub-skills directly bypassing the rollup logic, never invents counts. If the rollup is unavailable or the projects are unreachable, the live page surfaces a "rollup unavailable" banner rather than rendering partial state.

**Output-only.** Never opens tasks, never writes to sub-skill projects, never modifies PLM. Two write destinations only: an Asana attachment in SJS Regulatory Management on the triggering task, and the GitHub repo at `/Users/alvinbelt/Downloads/acb-thelanding/`. No third destination at v6.4.

**Hub patterns are non-negotiable.** Per the project memory: hub dashboards use `Hub.renderHeader/Nav/Footer` inside `<div class="page">`, NOT the `site-header.html` partial. Must call `Hub.bindNav()` after injecting `renderShell`. Asana references on hub pages pull live via Netlify Functions (project pagination + completed_since + PT timezone). Pages on `acb-thelanding.netlify.app` deploy via GitHub commit-and-push to main, never directly to Netlify.

**Live + archive split.** The live page (`regulatory-dashboard.html`) calls a Netlify Function on every load and shows current Asana state. Monthly archives (`archive/regulatory-YYYY-MM.html`) are static — embedded data captured at month-end snapshot run.

**Brand scope.** Sweet July Skin only at v6.4. Cross-system (PD + Quality + Regulatory + Ops) reporting is a separate concern handled by a future leadership dashboard.

**Scope → plan → approve → build.** Operations' working rule. Any change to dashboard sections, archive cadence, or write destinations goes through the user, not committed unilaterally.

## Publishing — authoritative override

All landing-hub writes from this skill go through the `landing-hub-publish` Netlify Function. Any later text in this SKILL that says "write file X to `/Users/alvinbelt/Downloads/acb-thelanding/...`" or "git add / commit / push from the local repo" is **deprecated**. Interpret all such instructions as: "include the file in the next `landing-hub-publish` call." Skills are environment-portable now — no local clone, no local filesystem, no local git required. Works identically from Cowork on a dedicated runner, from Claude Code on any machine, from claude.ai chat with MCPs.

### How to publish

POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret: <HUB_FUNCTION_SECRET>` (env var on the runner; same secret used by `pd-asana-attach`) and body:

```json
{
  "files": [
    { "path": "regulatory-dashboard.html",                  "content": "<!doctype html>..." },
    { "path": "data/regulatory-monthly-snapshot.json",      "content": "{...}\n" },
    { "path": "archive/regulatory-2026-05.html",            "content": "<!doctype html>..." }
  ],
  "commit_message": "regulatory dashboard: monthly snapshot May 2026"
}
```

Constraints: up to 20 files per call, 5 MB total body, no absolute paths, no `..` traversal. Each file is its own GitHub commit; Netlify auto-deploys on each. For a multi-file refresh the deploys are sequential and the final live page settles ~60–90s after the last commit.

Returns `{ ok: true, commit_sha, commit_url, file_count, deploy_url_hint }` on success. On failure, the response has `ok: false` with `error` and `detail` — surface those to the operator. Do not retry on a loop.

### What this means for the operator HITL

The operator approval gate still applies before publish — render the narratives, surface the proposed file contents (and a diff against the current published version if useful), wait for "go." On approval, fire the `landing-hub-publish` POST. The function performs the commit; Netlify deploys; the operator gets the commit URL back to verify. Same gate the local-git workflow had, just executed through HTTPS instead of a shell.

## The four core jobs

### 1. Generate the live dashboard (Job 1)

On-demand operator trigger. The skill regenerates `regulatory-dashboard.html` from the current Asana state and commits to the GitHub repo. Use cases: layout edits, new section adds, mid-month forced refresh, debugging a render issue.

- *Trigger:* "regenerate regulatory dashboard", "rebuild the regulatory dashboard", "push the regulatory dashboard", "publish the regulatory dashboard", initial build at first-run setup
- *Action:*
  1. Confirm the operator wants to commit and push (HITL gate — every commit goes to main and triggers a Netlify deploy).
  2. Re-pull current Asana state to confirm sections, fields, and option gids match what the Netlify Function expects.
  3. Write or rewrite the four core files in `/Users/alvinbelt/Downloads/acb-thelanding/`:
     - `regulatory-dashboard.html` (page entry shell)
     - `assets/js/regulatory-dashboard.js` (page module)
     - `assets/css/regulatory-dashboard.css` (page styles)
     - `netlify/functions/sjs-regulatory-rollup.js` (live data Function)
  4. Update `data/links.json` to include the Regulatory Management section under `product-development` (mirrors Quality Management section pattern).
  5. Run a syntax check on the function (Node) and validate JSON for links.json.
  6. Commit and push to main.
- *HITL:* **Operator approves the commit before push.** Per memory: never commit without confirmation.

### 2. Monthly snapshot (Job 2)

Auto-fire on the first business day of each month at 9am PT. Snapshots the dashboard's current state to a frozen archive page; live page continues showing current state.

- *Trigger:* monthly schedule (first business day, 9am PT — registered via the `schedule` skill at first-run); "snapshot the regulatory dashboard", "create monthly regulatory archive"
- *Action:*
  1. Read current rollup via the Netlify Function (same source the live page uses).
  2. Render the captured rollup into a static HTML page at `/Users/alvinbelt/Downloads/acb-thelanding/archive/regulatory-YYYY-MM.html` (where YYYY-MM is the month being snapshotted).
  3. The archive page uses the same Hub shell, header, and CSS as the live page. Data is embedded inline — no Function call.
  4. The live `regulatory-dashboard.html` adds a link to the new archive in its "Recent snapshots" footer section.
  5. Stage a `[Monthly Regulatory Dashboard Snapshot] YYYY-MM` task in SJS Regulatory Management → Cross-Skill Dashboard section. Set `Artifact Type = Monthly Regulatory Dashboard Snapshot` (option add at first-run) or fall back to `Other` if the option doesn't exist yet. Attach the archive HTML file.
  6. Commit and push to main.
- *HITL:* **Operator approves the commit before push.** Even on monthly auto-fire, commit confirmation stays in place.

### 3. Read-only summary on demand (Job 3)

The simplest path. Operator asks for a regulatory update; skill returns a chat-formatted summary by reading regulatory-manager's rollup. No file writes, no Asana writes.

- *Trigger:* "what's open in regulatory" (also fires regulatory-manager Job 2 directly), "regulatory update for the team", "regulatory summary", "give me the regulatory rollup", "regulatory status now"
- *Action:* Read regulatory-manager's rollup. Return summary in chat. Optionally post as an Asana comment on a specified task.
- *HITL:* none for the read; if posting as Asana comment, confirm target task before posting.

### 4. Asana attachment (Job 4)

For every Job 1 or Job 2 generation, attach the resulting HTML file to a designated task.

**On-demand (Job 1):** comment on the triggering query task (or a `[Regulatory Dashboard Generated] YYYY-MM-DD HH:MM` task in Cross-Skill Dashboard if no triggering task exists).

**Monthly auto (Job 2):** dedicated `[Monthly Regulatory Dashboard Snapshot] YYYY-MM` task in Cross-Skill Dashboard section. Archive HTML attaches; comment captures the GitHub commit SHA and the live page URL.

- *Trigger:* fires automatically as part of Job 1 / Job 2.
- *Action:* Asana attachment via direct API. Comment captures generation timestamp, source rollup state, GitHub commit SHA, live page URL, archive URL (if Job 2).
- *HITL:* none — this is the post-commit recording step.

## Asana surface

- *Project:* **SJS Regulatory Management** (gid `1214660807386611`).
- *Task home:* Cross-Skill Dashboard section (gid `1214660230826189`, added at v6.3).
- *No new sections at v6.4.*
- *Custom field reuse:* `Artifact Type` (gid `1214661463988667`) gets a new option: `Monthly Regulatory Dashboard Snapshot`. Add via Asana UI at v6.4 first-run.
- *No new custom fields.*

## Hub integration

- *Repo:* `/Users/alvinbelt/Downloads/acb-thelanding/` (GitHub `SWEETJULY26/acb-thelanding`).
- *Live page URL:* `https://acb-thelanding.netlify.app/regulatory-dashboard.html`.
- *Archive URL pattern:* `https://acb-thelanding.netlify.app/archive/regulatory-YYYY-MM.html`.
- *Nav placement:* Product Development function → new **Regulatory Management** section, placed right after the existing Quality Management section.
- *Files this skill writes:*
  - `regulatory-dashboard.html` (page entry)
  - `assets/js/regulatory-dashboard.js` (page module)
  - `assets/css/regulatory-dashboard.css` (page styles, prefix `rd-`)
  - `netlify/functions/sjs-regulatory-rollup.js` (live data Function)
  - `archive/regulatory-YYYY-MM.html` (one per monthly snapshot)
  - `data/links.json` (one section addition under product-development)

## Render pattern (v6.7 — weekly digest, shared hub chrome, spend strip)

Single-page weekly digest. **Hub shell** (AC · Brands eyebrow, "The Landing." headline, FUNCTIONS dropdown nav) rendered via `Hub.renderHeader / renderNav / renderFooter` from `assets/js/hub.js` — never hand-rolled in the page. → **hero block** (page title + blurb + week stamp) → **lede strip** (headline state of the week) → **KPI row** (4 tiles) → **spend strip** (2 segments, v6.7) → **tab nav** → **5 tab panels**. Tabs are vanilla JS, no build step.

Three-file output, mirroring `quality-dashboard.html`:
- `regulatory-dashboard.html` — never edited content; only the chrome shell. Weekly regen does NOT overwrite this file.
- `assets/js/regulatory-dashboard.js` — weekly regen overwrites the inline tab content blocks inside the `mount()` function. Chrome calls (`Hub.renderHeader`, `Hub.renderNav('Regulatory Dashboard')`, `Hub.renderFooter`, `Hub.bindNav()`, `Hub.bindEditMode()`) stay untouched.
- `assets/css/regulatory-dashboard.css` — never overwritten on weekly regen unless a new component is added.

Every regen starts from `references/dashboard-template.html` (the locked thin-shell HTML). The page serves at `acb-thelanding.netlify.app/regulatory-dashboard.html`. No live Function call.

**KPI row** — 4 tiles up top, color-tinted by urgency band (alert / warn / ok / neutral):
- Pedrero queue depth (with capacity flag against the 5-item / 7-day touchbase rule)
- Items we owe Pedrero (next packet ladder)
- Statutory clocks at 80%+ count (SAE, recall, agency follow-up)
- Renewal window 30d count (attestations + registrations)

**Spend strip (v6.7)** — sits between the KPI row and the tab nav. Two horizontal segments, full container width on desktop, stacked on mobile:

*Segment A — Monthly headline.* Single tile, left side. Shows current-month regulatory spend (running) with three sub-figures: month-to-date total, last-month total for comparison, and a chevron (▲/▼/—) marking MoM direction. Background `--surface`, headline figure in `--good-youth`, MoM chevron tinted `--soursop` when up >15% (alert), `--rum-cake` when down >15% (under-spend flag), neutral otherwise.

*Segment B — Per-cost-category mini-bars.* Right side. Six stacked mini-bars (regulatory, quality, pd, ops, marketing, general), each rendered as a horizontal bar with width proportional to its share of total regulatory-driven spend (cost_category = 'regulatory' OR regulatory_driver = true). Bar fill `--good-youth` at full opacity for the dominant category, stepped opacity for smaller categories. Category label left, dollar amount right, share % in a chip.

*Data shape.* Reads from regulatory-manager Job 8 (current month) and Job 9 (quarterly context) via the extended Netlify Function `netlify/functions/sjs-regulatory-rollup.js` — same Function as the rest of the live page, with an added `spend` block:
```json
{
  "spend": {
    "current_month": { "label": "2026-05", "total": 47230.00, "mom_pct": 0.12 },
    "prior_month":   { "label": "2026-04", "total": 42150.00 },
    "by_category": [
      { "cost_category": "regulatory", "amount": 18500.00, "share": 0.39 },
      { "cost_category": "quality",    "amount": 14200.00, "share": 0.30 },
      { "cost_category": "pd",         "amount":  8730.00, "share": 0.18 },
      { "cost_category": "ops",        "amount":  3200.00, "share": 0.07 },
      { "cost_category": "marketing",  "amount":  1800.00, "share": 0.04 },
      { "cost_category": "general",    "amount":   800.00, "share": 0.02 }
    ],
    "regulatory_driver_share": 0.62
  }
}
```

*Hover tooltip drill-down.* Each mini-bar shows on hover a top-three vendor list inside that cost_category for the current month, with invoice counts and totals. Pure CSS + small JS — no live calls on hover (data ships inline with the page). Segment A's MoM chevron hover surfaces the dollar delta.

*Archive inclusion.* Each monthly snapshot page (`archive/regulatory-YYYY-MM.html`) freezes its own spend strip with that month's data baked in. The frozen snapshot uses the same `spend` block shape but reads the source month from Job 9's quarterly history rather than current Job 8.

*Responsive collapse rules.* ≥1024px: side-by-side. 768–1023px: stacked (A on top, B below) at full width. ≤767px: segment A stays, segment B collapses to a "tap to expand" accordion to keep mobile scroll lean.

*Brand chrome.* All tokens drawn from `main.css`: `--surface` (strip background), `--good-youth` (headline + dominant bar), `--rum-cake` (under-spend chevron), `--soursop` (alert chevron). Strip uses `rd-spend-strip` namespace in `regulatory-dashboard.css`. No new CSS variables.

**5 tabs:**

| Tab | What it shows | Sources |
|---|---|---|
| **Clocks & Deadlines** | Time-ordered table of every dated regulatory item: Pedrero sends pending, IL reviews scheduled, agency clocks ticking, statutory deadlines (Canada extended-allergens cutoff, EPR threshold trigger), retailer attestation renewal windows. Countdown chips color-banded red/orange/green/gray by urgency. | Both projects, Window End field, statutory clock derivation from SKN-OPS-009 §10.1 |
| **Pedrero** | Queue depth + capacity + ownership split. "What Pedrero owes us" vs "What we owe Pedrero" two-column view. Heather vs Amy load split. SB 343 packaging audit thread surfaced separately. RP partner section (Ecomundo for Canada, plus UK/South Africa Pending). | Both projects via Gate field + Artifact Type Pedrero Liaison; pedrero-contacts.md for ownership |
| **Clearance Matrix** | Per-SKU clearance grid: IL status / claim sub / label artwork / retailer attestations / Canada / Quebec / Pantone audit / 19-state toxics cert chain. Renders as a SKU × clearance-type matrix with pill states (cleared / pending / blocked / N/A). | SJS Regulatory Management — Artifact Type breakdown by Linked SKU |
| **Operational Signal** | SAE filings in flight with statutory clock bars, recall classification + reporting windows, batch-affected counts. Cross-flag inbox from Quality (`[Reg Flag Pending — regulatory-manager]`) with fan-out status. Reformulation claim-bridge per-SKU status (Eye Cream, Toner, Power Oil paths). | SJS Reportable Events + claims-il-and-label-keeper §7.4 tasks |
| **Strategic Horizon** | Forward-looking view — EPR threshold monitor (trailing-12 sales bar against $5M global / $1M CA), UBM Beauty Marketplace June 2026 launch dependencies, Pedrero scope-change watch, international market activation flags (UK / South Africa pending). Founder-level signals that feed ayesha-weekly-briefing. | SJS Regulatory Management — registrations queue + Pedrero Liaison engagement-level tasks |

**Visualization rules:**
- Statutory clock bars: green <60%, yellow 60–95%, red ≥95% (per SKN-OPS-009 §10.1)
- Canada extended-allergens countdown: green ≥60d to 2026-07-31, yellow 30–60d, red ≤30d
- EPR threshold: green <60% of $5M global / $1M CA, yellow 60–80%, red ≥80%
- Pedrero capacity flag: alert when queue ≥5 items or any single send sits >7 days

## Calls and integrations

**Reads via:**
- regulatory-manager — primary rollup source (Asana SJS Regulatory Management state, project status updates, registrations queue, Pedrero liaison, retailer attestation cadence)
- regulatory-manager Jobs 8 + 9 — monthly + quarterly cost rollup data for the spend strip (v6.7); reads `vendor_invoices` via Supabase SELECT inside the rollup composition
- adverse-event-and-recall-reporter (transitively via Netlify Function reading SJS Reportable Events) — SAE/recall state and statutory clocks
- claims-il-and-label-keeper (transitively via SJS Regulatory Management) — IL/claim/label/attestation state
- Asana — direct read via the Netlify Function (server-side using ASANA_PAT env var)
- sweet-july-skin-brand — CSS tokens for hub-page brand styling

**Writes via:**
- Asana — direct (attachments and comments only on Cross-Skill Dashboard section tasks)
- GitHub repo at `/Users/alvinbelt/Downloads/acb-thelanding/` — via local git commit and push to main

**Called by:**
- Operator on-demand (Job 1, Job 3)
- `schedule` skill on monthly cadence (Job 2)
- sjs-regulatory-system (v6.5 router) — routes any "regulatory dashboard" / "branded regulatory output" intent here

**Never duplicates:**
- regulatory-manager (owns the rollup composition; this skill renders it)
- Sub-skill reads bypassing the rollup logic
- quality-status-reporter (System B sister; not this scope)
- sjs-status-reporter (PD-side rollup; not this scope)
- Future ops-status-reporter (Operations-side rollup; not this scope)
- Future leadership-dashboard (cross-system / cross-function dashboards; out of System C scope)

## Out of scope (v6.4)

- PDF, PPTX, DOCX output (HTML only at v6.4)
- Audit-prep packet, retailer regulatory summary, monthly Pedrero review packet — defer until needed
- Quarterly review artifact generation
- Sub-pages on the hub (`regulatory-attestations.html`, `regulatory-registrations.html`, etc.) — single page only
- Direct sub-skill reads bypassing the rollup composition
- PLM writes
- Cross-system reporting (PD + Quality + Regulatory + Ops combined) — future leadership dashboard concern
- Brand application beyond CSS tokens — sweet-july-skin-brand may need a v2 to support richer styling
- Working procedure / SOP — output generation is infrastructure, not a workflow that needs a documented procedure

## First-run setup

The skill is new at v6.4. On first invocation:

1. Confirm `/Users/alvinbelt/Downloads/acb-thelanding/` is reachable and on a clean working tree.
2. Confirm the SJS Regulatory Management Asana project responds (gid `1214660807386611`).
3. Confirm the SJS Reportable Events Asana project responds (gid `1214660834583706`).
4. Confirm `ASANA_PAT` env var is set in the Netlify dashboard (read-only — surface to operator if missing).
5. Read existing patterns (one-time, cached for the session):
   - `quality-dashboard.html` (page entry pattern at v5.6)
   - `assets/js/quality-dashboard.js` (page module pattern at v5.6)
   - `netlify/functions/sjs-quality-rollup.js` (Function pattern at v5.6)
   - `data/links.json` (hub data structure)
6. Confirm `Monthly Regulatory Dashboard Snapshot` and `Quality Dashboard Generated`-equivalent options exist on `Artifact Type` field (gid `1214661463988667`); if missing, surface to operator and fall back to `Other` value temporarily.
7. Confirm Job 1 generated artifacts at v6.4 build are deployed (Operator-confirmed Netlify deploy success).
8. Schedule the monthly snapshot via the `schedule` skill: cron `0 9 1 * *` America/Los_Angeles.

If any check fails, surface to the operator and stop — the skill does not modify the repo unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/role-map.md` — current role-holders for Operator, Reg Lead, External Reg Partner, QA Lead, Voice of Customer; references regulatory-manager as canonical home
- `references/trigger-phrases.md` — grouped triggers by intent
