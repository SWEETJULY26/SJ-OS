---
name: quality-status-reporter
description: Generate the branded HTML quality dashboard for Sweet July Skin from quality-manager's rollup. Three-tab live page (Weekly default, Monthly, Quarterly) refreshed on cadence. Use for dashboard refresh, weekly digest push, monthly tab refresh, quarterly tab refresh, or branded quality output. Triggers include "quality dashboard", "regenerate quality dashboard", "push the quality dashboard", "push weekly quality digest", "refresh monthly quality tab", "refresh quarterly quality tab", "quality update for the team". Reads quality-manager's rollup (Jobs 6, 7, 8 cadence payloads). Writes to Asana in SJS Quality Management (gid 1214660401644163) and the AC Brands landing hub at acb-thelanding.netlify.app/quality-dashboard.html via the GitHub repo at /Users/alvinbelt/Downloads/acb-thelanding/. Reuses Hub shell pattern. Never opens tasks, never writes to sub-skills. v5.7. Sister to sjs-status-reporter and regulatory-status-reporter.
---

# Quality Status Reporter

The rendering layer for System B quality. Takes quality-manager's composed rollup and turns it into a three-tab live HTML dashboard on the AC Brands landing hub (Weekly default, Monthly, Quarterly). Read-only on data, output-only on writes.

## Why this exists

quality-manager (v5.6) composes the System B rollup across four cadences — weekly digest, monthly operational rollup, quarterly operational rollup, plus the existing on-demand rollup. Without a rendering layer, that data lives only in Asana project status updates and on-demand chat replies — neither suits the team's broader visibility need or the retailer/regulatory context that wants something to look at, not read in chat. This skill is the publish step: a three-tab live page anyone with hub access can scan, refreshed on cadence.

The skill is intentionally narrow at v5.7: HTML dashboard only, on-demand + scheduled cadence pushes. PDF, PPTX, and DOCX outputs are explicitly out of scope. The Word docs we ship for SOP filings (SKN-OPS-006, SKN-OPS-007) are one-off and live in their authoring skills.

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**Single source of truth: quality-manager rollup.** The skill never reads sub-skills directly, never duplicates aggregation logic, never invents counts. If quality-manager rollup is unavailable or stale, the live page surfaces a "rollup unavailable" banner rather than falling back to direct sub-skill reads. Cleanest boundary; prevents v5.7 divergence from the canonical rollup.

**Output-only.** Never opens tasks, never writes to sub-skill projects, never modifies PLM. Two write destinations only: Asana writes in SJS Quality Management (Job 1 attachment on the triggering task; breadcrumb comments to the Quality Sweep Running Log for Jobs 2/5/6; staged handoff comments for Job 5's quarterly) and the GitHub repo at `/Users/alvinbelt/Downloads/acb-thelanding/`. No third destination at v5.7.

**Hub patterns are non-negotiable.** Per the project memory: pages must reuse `Hub.renderHeader` / `renderNav` / `renderFooter`, must call `Hub.bindNav()` and `Hub.bindEditMode()` after injecting renderShell, and the shared header lives at `assets/includes/site-header.html`. Asana references on hub pages pull live via Netlify Functions (project pagination + completed_since + PT timezone + mirror chart filters). Pages on `acb-thelanding.netlify.app` deploy via GitHub commit-and-push to main, never directly to Netlify.

**Three-tab live dashboard.** As of v5.7, the live page (`quality-dashboard.html`) carries three tabs: Weekly (default — live Function call on every load), Monthly, and Quarterly. The Monthly and Quarterly tabs read static JSON snapshots (`data/quality-monthly-snapshot.json`, `data/quality-quarterly-snapshot.json`) that the cadence jobs refresh. No frozen archive pages.

**Brand scope.** Sweet July Skin only at v5.7. Cross-system (PD + Quality + Ops) reporting is a separate concern handled by ac-brands-leadership-dashboard.

**Scope → plan → approve → build.** Operations' working rule. Any change to the dashboard sections, archive cadence, or write destinations goes through the user, not committed unilaterally.

## Publishing — authoritative override

All landing-hub writes from this skill go through the `landing-hub-publish` Netlify Function. Any later text in this SKILL that says "write file X to `/Users/alvinbelt/Downloads/acb-thelanding/...`" or "git add / commit / push from the local repo" is **deprecated**. Interpret all such instructions as: "include the file in the next `landing-hub-publish` call." Skills are environment-portable now — no local clone, no local filesystem, no local git required. Works identically from Cowork on a dedicated runner, from Claude Code on any machine, from claude.ai chat with MCPs.

### How to publish

POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret: <HUB_FUNCTION_SECRET>` (env var on the runner; same secret used by `pd-asana-attach`) and body:

```json
{
  "files": [
    { "path": "quality-dashboard.html",                "content": "<!doctype html>..." },
    { "path": "data/quality-monthly-snapshot.json",    "content": "{...}\n" }
  ],
  "commit_message": "quality dashboard: monthly tab refresh May 2026"
}
```

Constraints: up to 20 files per call, 5 MB total body, no absolute paths, no `..` traversal. Each file is its own GitHub commit; Netlify auto-deploys on each. For a multi-file refresh, the deploys are sequential and the final live page settles ~60–90s after the last commit.

Returns `{ ok: true, commit_sha, commit_url, file_count, deploy_url_hint }` on success. On failure, the response has `ok: false` with `error` and `detail` — surface those to the operator. Do not retry on a loop.

### What this means for the operator HITL

The operator approval gate still applies before publish — render the narratives, surface the proposed file contents (and a diff against the current published version if useful), wait for "go." On approval, fire the `landing-hub-publish` POST. The function performs the commit; Netlify deploys; the operator gets the commit URL back to verify. Same gate the local-git workflow had, just executed through HTTPS instead of a shell.

## The six core jobs

### 1. Generate the live dashboard (Job 1)

On-demand operator trigger. The skill regenerates `quality-dashboard.html` from the current Asana state and commits to the GitHub repo. Use cases: layout edits, new section adds, mid-month forced refresh, debugging a render issue.

As of v5.7 the dashboard is a three-tab live page. Job 1 renders into the Weekly tab (default) — the same on-demand entry point operators have used since v5.6. The Monthly and Quarterly tabs are refreshed on cadence by Jobs 2 and 5; Job 6 is the named scheduled trigger for the weekly tab.

- *Trigger:* "regenerate quality dashboard", "rebuild the quality dashboard", "push the quality dashboard", "publish the quality dashboard", initial build at first-run setup
- *Action:*
  1. Confirm the operator wants to commit and push (HITL gate — every commit goes to main and triggers a Netlify deploy).
  2. Read the dashboard spec at `references/dashboard-spec.md` for sections, layout, and data shape.
  3. Write or rewrite three files in `/Users/alvinbelt/Downloads/acb-thelanding/`:
     - `quality-dashboard.html` (page entry shell)
     - `assets/js/quality-dashboard.js` (page module)
     - `assets/css/quality-dashboard.css` (page styles)
  4. Write or update the Netlify Function at `netlify/functions/sjs-quality-rollup.js` per `references/netlify-function-spec.md`.
  5. Update `data/links.json` to include the Quality Management section under `product-development` per `references/hub-integration.md` §1.
  6. Run a syntax check on the function (Node) and the page (HTML/CSS validation if available).
  7. Commit and push to main.
- *HITL:* **Operator approves the commit before push.** Per memory: never commit without confirmation.

### 2. Monthly tab refresh (Job 2)

Auto-fire on the first business day of each month at 7:00 AM PT. Refreshes the Monthly tab in place — no frozen archive page, no archive folder additions. The dashboard is the artifact.

- *Trigger:* `sjs-quality-monthly-snapshot` scheduled task (first business day of month, 7:00 AM PT — registered via the `schedule` skill at first-run); on-demand "refresh monthly quality tab"
- *Action:*
  1. Call `quality-manager` Job 7 (monthly operational rollup). Receive payload per `quality-manager/references/cadence-composition-spec.md` §2.
  2. Render the payload into the Monthly tab data store on `quality-dashboard.html`. The Function exposes the payload at `?window=monthly`.
  3. Update `data/quality-monthly-snapshot.json` in `acb-thelanding` with the rendered payload — this is the static fallback if the Function is down.
  4. Commit and push to main. Commit message: `quality dashboard: monthly tab refresh <Month YYYY>`.
  5. Post a breadcrumb comment to the Quality Sweep Running Log task per `references/tab-refresh-spec.md` (Monthly format). Includes RAG, headline, and the top 3–5 deltas vs. prior month.
- *HITL:* **Operator approves the commit before push.** Breadcrumb posts automatically after commit confirmation.
- *No attachment, no new Asana task.*

### 3. Read-only summary on demand (Job 3)

The simplest path. Operator asks for a quality update; skill returns a chat-formatted summary by reading quality-manager's rollup. No file writes, no Asana writes.

- *Trigger:* "what's open in quality" (also fires quality-manager Job 2 directly), "quality update for the team", "quality summary", "give me the quality rollup", "quality status now"
- *Action:* Read quality-manager's rollup. Return summary in chat. Optionally post as an Asana comment on a specified task.
- *HITL:* none for the read; if posting as Asana comment, confirm target task before posting.

### 4. Asana attachment (Job 4)

Narrowed at v5.7 to Job 1 only. The Monthly (Job 2), Quarterly (Job 5), and Weekly digest (Job 6) cadences do NOT attach files anywhere — the dashboard is the artifact and the breadcrumb comment on the Quality Sweep Running Log task is the only Asana write.

**On-demand (Job 1):** comment on the triggering query task (or a `[Quality Dashboard Generated] YYYY-MM-DD HH:MM` task in Cross-cutting Tasks if no triggering task exists). Attach the rendered HTML file.

- *Trigger:* fires automatically as part of Job 1.
- *Action:* Asana attachment via direct API. Comment captures generation timestamp, source rollup state, GitHub commit SHA, live page URL.
- *HITL:* none — this is the post-commit recording step.

### 5. Quarterly tab refresh (Job 5)

Auto-fire on the first business day of Jan/Apr/Jul/Oct at 7:00 AM PT. Refreshes the Quarterly tab in place from the `quality-manager` Job 8 payload, then stages the two handoff comments the quarterly payload carries.

- *Trigger:* `sjs-quality-quarterly-rollup` scheduled task (first business day of Jan/Apr/Jul/Oct, 7:00 AM PT); on-demand "refresh quarterly quality tab"
- *Action:*
  1. Call `quality-manager` Job 8 (quarterly operational rollup). Receive payload per `quality-manager/references/cadence-composition-spec.md` §3.
  2. Render the payload into the Quarterly tab data store. The Function exposes the payload at `?window=quarterly`.
  3. Update `data/quality-quarterly-snapshot.json` with the rendered payload.
  4. Commit and push to main. Commit message: `quality dashboard: quarterly tab refresh <Quarter YYYY>`.
  5. Post a breadcrumb comment to the Quality Sweep Running Log task per `references/tab-refresh-spec.md` (Quarterly format). Includes RAG, headline, quarter recap (first 2 sentences), trends emerging (first sentence), and whether a founder signal staged for Ayesha.
  6. Post the two staged handoff comments from the §3 payload — one to `sjs-status-reporter` running log, one to the `ayesha-weekly-briefing` source pool. Both stay in draft state until Operator approves.
- *HITL:* **Operator approves the commit before push. Operator approves the two handoff comments separately** before they post.
- *No attachment, no new Asana task.*

### 6. Weekly digest push (Job 6)

The named, scheduled version of Job 1. Fires Monday 7:30 AM PT and pushes the week's digest into the Weekly tab so the cadence has a labeled, scheduled entry point. Job 1 stays the on-demand path; Job 6 is the cron path.

- *Trigger:* `sjs-quality-weekly-digest` scheduled task (Monday 7:30 AM PT); on-demand "push weekly quality digest"
- *Action:*
  1. Call `quality-manager` Job 6 (weekly digest composition). Receive payload per `quality-manager/references/cadence-composition-spec.md` §1.
  2. Render the payload into the Weekly tab (default) on `quality-dashboard.html`. The Function exposes the payload at `?window=weekly` (default if omitted).
  3. Commit and push to main. Commit message: `quality dashboard: weekly digest push <YYYY-MM-DD>`.
  4. Post a breadcrumb comment to the Quality Sweep Running Log task per `references/tab-refresh-spec.md` (Weekly format). Includes RAG, headline, and top 3–5 priorities.
- *HITL:* **Operator approves the commit before push.** Breadcrumb posts automatically after commit confirmation.
- *No attachment, no new Asana task.*

## Asana surface

- *Project:* **SJS Quality Management** (gid `1214660401644163`).
- *Task home:* Cross-cutting Tasks section (added at v5.5).
- *No new sections at v5.7.*
- *Breadcrumb target:* the Quality Sweep Running Log task in Cross-cutting Tasks. Jobs 2, 5, and 6 comment on this single running task — they do not open new tasks per run.
- *Custom field reuse:* `Cross-cutting Type` continues to host "Quality Dashboard Generated" for Job 1 on-demand attachments. No new field options at v5.7.
- *No new custom fields.*

## Hub integration

- *Repo:* `/Users/alvinbelt/Downloads/acb-thelanding/` (GitHub `SWEETJULY26/acb-thelanding`).
- *Live page URL:* `https://acb-thelanding.netlify.app/quality-dashboard.html`.
- *Tab anchors:* `#weekly` (default), `#monthly`, `#quarterly`. Breadcrumb comments deep-link via these anchors.
- *Nav placement:* Product Development function → **Quality Management** section.
- *Files this skill writes:*
  - `quality-dashboard.html` (page entry — three-tab shell)
  - `assets/js/quality-dashboard.js` (page module — tab nav + per-tab render)
  - `assets/css/quality-dashboard.css` (page styles — tab nav, MoM/QoQ layouts)
  - `netlify/functions/sjs-quality-rollup.js` (live data Function — `window` param dispatch)
  - `data/quality-monthly-snapshot.json` (Monthly tab static payload, refreshed by Job 2)
  - `data/quality-quarterly-snapshot.json` (Quarterly tab static payload, refreshed by Job 5)
  - `data/links.json` (one section addition under product-development)

See `references/hub-integration.md` for exact patterns and `references/netlify-function-spec.md` for the Function spec.

## Calls and integrations

**Reads via:**
- quality-manager — primary rollup source (Asana SJS Quality Management state, project status updates, SOP catalog task, cross-cutting tasks, QoS signals)
- Asana — direct read via the Netlify Function (server-side using ASANA_PAT env var)
- sweet-july-skin-brand — CSS tokens for hub-page brand styling

**Writes via:**
- Asana — direct (attachments and comments only on Cross-cutting Tasks tasks)
- GitHub repo at `/Users/alvinbelt/Downloads/acb-thelanding/` — via local git commit and push to main

**Called by:**
- Operator on-demand (Job 1, Job 3)
- `schedule` skill on monthly cadence (Job 2)
- ac-brands-quality-system (v5.7 router) — routes any "quality dashboard" / "branded quality output" intent here

**Never duplicates:**
- quality-manager (owns the rollup composition; this skill only renders it)
- Sub-skill reads (this skill never goes around quality-manager)
- sjs-status-reporter (PD-side rollup; sister skill, not this scope)
- Future ops-status-reporter (Operations-side rollup; sister skill, not this scope)
- ac-brands-leadership-dashboard (cross-system / cross-function dashboards; out of System B scope)

## Out of scope (v5.7)

- PDF, PPTX, DOCX output (HTML only at v5.7)
- Standalone quarterly review artifacts (the Quarterly tab is the artifact; no separate file is generated)
- Sub-pages on the hub (quality-capa.html, quality-batches.html, etc.) — single page only
- Direct sub-skill reads (always go through quality-manager rollup)
- PLM writes
- Cross-system reporting (PD + Quality + Ops combined) — that's ac-brands-leadership-dashboard concern
- Brand application beyond CSS tokens (rich styling, typography, full design system) — sweet-july-skin-brand may need a v2 to support this
- Working procedure / SOP — output generation is infrastructure, not a workflow that needs a documented procedure

## First-run setup

On first invocation at v5.7 (or first run after the four-cadence build):

1. Confirm `/Users/alvinbelt/Downloads/acb-thelanding/` is reachable and on a clean working tree.
2. Confirm the SJS Quality Management Asana project responds (gid `1214660401644163`).
3. Confirm `ASANA_PAT` env var is set in the Netlify dashboard (read-only — surface to operator if missing).
4. **Confirm the Quality Sweep Running Log task exists in SJS Quality Management → Cross-cutting Tasks section.** Jobs 2, 5, and 6 post breadcrumb comments to this task. If missing, surface to the operator and stop — the cadence breadcrumbs depend on it.
5. Confirm the three scheduled tasks are registered via the `schedule` skill:
   - `sjs-quality-weekly-digest` — Monday 7:30 AM PT
   - `sjs-quality-monthly-snapshot` — first business day of month, 7:00 AM PT
   - `sjs-quality-quarterly-rollup` — first business day of Jan/Apr/Jul/Oct, 7:00 AM PT
6. Confirm `data/quality-monthly-snapshot.json` and `data/quality-quarterly-snapshot.json` exist in `acb-thelanding`. OK if empty on first run — Jobs 2 and 5 write them on first fire.
7. Read existing patterns (one-time, cached for the session):
   - `inventory-dashboard.html` (page entry pattern)
   - `assets/js/inventory-dashboard.js` (page module pattern)
   - `netlify/functions/sjs-pd-stats.js` (Function pattern)
   - `assets/includes/site-header.html` (header partial pattern)
   - `data/links.json` (hub data structure)
   - `regulatory-dashboard.html` + `assets/js/regulatory-dashboard.js` (multi-tab pattern reference from regulatory-status-reporter v6.6.2)
8. Confirm with operator → commit and push to main.
9. Verify Netlify deploys cleanly (check the deploy in the Netlify dashboard if available).

If any check fails, surface to the operator and stop — the skill does not modify the repo unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/dashboard-spec.md` — page sections, three-tab layout, per-tab data shape
- `references/netlify-function-spec.md` — `sjs-quality-rollup.js` Function spec (response shape, Asana queries, error handling, `window` param dispatch)
- `references/tab-refresh-spec.md` — tab layout intent, breadcrumb comment formats, Function `window` param contract for Jobs 2, 5, 6
- `references/hub-integration.md` — page chrome integration, links.json section addition, deploy pattern
- `references/trigger-phrases.md` — grouped triggers by intent
