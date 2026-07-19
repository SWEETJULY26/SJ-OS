# Scheduled task: pd-quarterly-rollup

Remote routine. Operate in America/Los_Angeles time. The skills repo is cloned at `/home/user/sj-os`.

## Skills to read and FOLLOW (plain files, not auto-registered — read them as instructions)
- `/home/user/sj-os/.claude/skills/sjs-status-reporter/SKILL.md`
- `/home/user/sj-os/.claude/skills/asana-pd-manager/SKILL.md`
- `/home/user/sj-os/.claude/skills/ac-brands-pd-system/SKILL.md`
Also read any reference files these cite under their skill dirs (e.g. `references/*.md`).

## Connectors
Use only the attached connectors: Asana, Asana(sse), Supabase. Discover the tools they expose; never reference local mcp tool ids (no `mcp__<uuid>__...`).

## Secret
When a step publishes to landing-hub (`acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish`), send the `x-hub-secret` header read from the `HUB_FUNCTION_SECRET` environment variable. If it is unset, skip the publish/archive step, still post the Asana update, and note the skip in your completion report.

## No local persistence
Do not write any local files or logs — the container is ephemeral.

## Task
# PD Quarterly Rollup — First Business Day of Q, 7:45 AM PT

You are running the Sweet July Skin PD Quarterly Rollup. Audience: Nicole, Danielle, Soraya, Perrine. Ayesha enters via the `ayesha-weekly-briefing` handoff.

## §0 — First-business-day validation

Today's date must be the first business day of Jan / Apr / Jul / Oct. If today is a Saturday, Sunday, or US federal holiday and an earlier day of the month was the first business day, exit silently — no Asana writes, no hub push, no inline draft.

## §1 — Reference

Recent context to anchor the preamble:
- The prior three `pd-monthly-rollup` outputs (last three months of the quarter).
- The latest `weekly-pd-update` and `sjs-pd-eod-reconciliation` on running log task GID `1214208955674591`.

The quarter opens by acknowledging the prior quarter's close-out as the starting line for this quarterly view.

## §2 — Input composition

Window: prior calendar quarter (e.g., if running Apr 1, window = Jan 1 → Mar 31 inclusive).

Pull from all five PD circular skills:
1. `asana-pd-manager` — every task touched in SJS PD projects across the quarter.
2. `fireflies-asana-bridge` — meeting fan-outs into PD across the quarter.
3. `outlook-asana-bridge` — supplier and internal email-driven PD signals.
4. `asana-plm-bridge` — financial signal sweep for the quarter: cost shifts, MOQ changes, allowance updates, margin-impact flags.
5. `outlook-plm-bridge` — PLM writes from Outlook this quarter (PO acks, COAs, stability/compat/RIPT/PET, compliance docs, BOM specs).

Enumerate portfolio members at run time: call `asana_get_items_for_portfolio` on portfolio GID `1208854258418250` ("2026-2028 Product Development Roadmap") to get the current list of project GIDs.

## §3 — Per-project payload

For each project in the portfolio, compose:
- Health rating (RAG: green / amber / red)
- Phase and due date
- Active blockers (count + summary)
- Quarter's progress narrative
- Quarter-over-quarter deltas — all six:
  - RAG shift
  - Due date slip in days
  - Blocker count change
  - Phase advance or regress
  - Milestones completed this quarter
  - New milestones added this quarter

This payload feeds both the per-project Asana status update and the HTML render.

## §4 — Render

Compose via `sjs-status-reporter`.

**Inline preview (Cowork chat):** Five-section narrative at quarterly granularity —
1. Portfolio Snapshot (counts, phase mix, momentum direction)
2. Per-Project Narrative (paragraph per active project; function-tag each milestone — Formula, Pack, Reg, Margin, Logistics)
3. Functional Area Roll-up (cross-project view)
4. Decisions Needed Across the Group
5. Look-ahead (next quarter's milestones)

**HTML output (PD Portfolio Dashboard):** Render the quarterly snapshot from the template structure at `pd-portfolio/_template.html` (read via the live URL or GitHub Contents API). Four-tab structure matching the existing PD Dashboard format:
- Tab 1 — Overall: KPI summary row (active projects, in-dev no-Asana, on track, at risk, off track, no status yet), "This Quarter — Priority Actions" callout, RAG cards per project
- Tab 2 — By Supplier: same projects grouped by supplier (KDC/One, AMR Labs, Vegelabs, IKS, etc.)
- Tab 3 — By Launch Window: projects sorted by due date, grouped into launch quarters
- Tab 4 — Creative: creative-track status (artwork, packaging design, photoshoot, copy)

Title: "SJ SKIN — PD Portfolio Status — Q[N] [YYYY]" (e.g., Q1 2026).

Strict zero-activity quiet threshold for §2 Per-Project Narrative: a project appears only if at least one input skill surfaced activity in the quarter.

## §5 — HITL gate

Draft inline in Cowork chat. Wait for Alvin's "go" before committing anything.

## §6 — Post-go write sequence

When Alvin says "go":

1. **Compose the archive page.** Render the quarterly snapshot HTML, targeted at path `pd-portfolio/[YYYY]-Q[N].html` (e.g., `pd-portfolio/2026-Q2.html`). Structure clones `pd-portfolio/_template.html`. Read the template via the live URL or GitHub Contents API; no local file IO.

2. **Compose the updated index.** Read the current `pd-portfolio.html` via the live URL or GitHub Contents API. Add a new entry at the top of the archive list linking to the page from step 1. Include quarter + one-line summary pulled from §1 Portfolio Snapshot.

3. **Publish both files via landing-hub-publish.** POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with header `x-hub-secret`. Resolve the secret from the `HUB_FUNCTION_SECRET` environment variable. Body:
   ```json
   {
     "files": [
       { "path": "pd-portfolio/[YYYY]-Q[N].html", "content": "<full HTML>" },
       { "path": "pd-portfolio.html",             "content": "<updated index HTML>" }
     ],
     "commit_message": "PD quarterly rollup — [YYYY] Q[N]"
   }
   ```
   The function commits to main via the GitHub API; Netlify auto-deploys. No local clone, no local git.

4. **Attach HTML to running log.** POST to `pd-asana-attach` with header `x-hub-secret` (same secret, resolved the same way) and body: `{ "html": "<full HTML payload>", "taskGid": "1214208955674591", "filename": "pd-quarterly-rollup-[YYYY]-Q[N].html" }`.

5. **Fan out `asana_create_project_status` across the portfolio.** For every project GID enumerated in §2 from portfolio `1208854258418250`, post a project status update with that project's per-project payload from §3. Use color codes: green = on_track, amber = at_risk, red = off_track.

6. **Post the 5-section narrative comment** on running log task GID `1214208955674591`. Append at the bottom: live link to `https://acb-thelanding.netlify.app/pd-portfolio/[YYYY]-Q[N].html`.

7. **Stage handoff to `sjs-status-reporter`.** Post a comment on running log task GID `1214208955674591` tagged `[Handoff → sjs-status-reporter]` requesting branded executive output for the quarter — concise leadership-facing version of the quarterly findings.

8. **Stage handoff to `ayesha-weekly-briefing`.** Post a comment on running log task GID `1214208955674591` tagged `[Handoff → ayesha-weekly-briefing]` flagging the quarterly findings for founder integration in the next Friday briefing.

## §7 — Failure handling

- If `landing-hub-publish` returns `ok: false`: surface the `error` + `detail` fields. `unauthorized` means the resolved secret doesn't match Netlify (re-check the `HUB_FUNCTION_SECRET` environment variable); `github_commit_failed` means the function's GitHub PAT has lost access. Both require the operator. Don't retry on a loop.
- If the `pd-asana-attach` call fails: still post the 5-section narrative comment with the live archive URL, then follow up with a comment containing the `commit_url` from step 3 as the source-of-truth link.
- If any individual `asana_create_project_status` call fails: continue the fan-out for the remaining projects, then post a follow-up running log comment listing the project GIDs that failed for manual retry.
- If a handoff comment fails to post: retry once, then surface the failure in the running log so Alvin can stage the handoff manually.

## §8 — Constraints

- Audience: Nicole, Danielle, Soraya, Perrine. Ayesha integrates via the briefing handoff.
- HITL gate: nothing commits until Alvin says "go."
- AC Brands writing rules — no banned words (delve, leverage, utilize, facilitate, streamline, empower, harness, unlock, foster, robust, seamless, comprehensive, vital, crucial, pivotal, multifaceted, nuanced, ever-evolving, cutting-edge, state-of-the-art, innovative, dynamic, holistic, paradigm, journey, ecosystem-metaphor, landscape-metaphor, tapestry, realm). No vibe emojis. Paragraphs default.
- Hub pages use `Hub.renderHeader/renderNav/renderFooter` inside `<div class="page">` — match existing pattern.
