# Scheduled task: weekly-pd-update

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
# Weekly PD Update — Monday 7 AM PT

You are running the Sweet July Skin Weekly PD Update. Audience: Nicole, Danielle, Soraya, Perrine.

## Reference

Friday's `sjs-pd-eod-reconciliation` scheduled-task output is the baseline. Pull its summary block from running log task GID 1214208955674591 and reference it in the preamble — the week opens by acknowledging Friday's close-out as the starting line.

## Input composition

Pull from all five PD circular skills for the window Last Monday 7 AM PT → Today 7 AM PT:

1. **asana-pd-manager** — every task touched in SJS PD projects (created, updated, status changed, commented, completed). Group by project.
2. **fireflies-asana-bridge** — meeting fan-outs into PD from the past week. Action items, decisions, blockers.
3. **outlook-asana-bridge** — supplier/internal email-driven PD signals. New tasks, follow-ups, commitments.
4. **asana-plm-bridge** — weekly financial signal sweep. Cost shifts, MOQ changes, allowance updates, margin-impact flags surfaced via the bridge. The financial-signal angle on PD movement.
5. **outlook-plm-bridge** — PLM writes from Outlook this week (PO acks, COAs, stability/compat/RIPT/PET, compliance docs, BOM specs).

Strict zero-activity quiet threshold for §2: a project appears in Per-Project Narrative only if at least one input skill surfaced activity. No filler entries.

## Render

Compose the five-section update via `sjs-status-reporter`. Sections:

1. **Portfolio Snapshot** — top-line state of every active SJS PD project (counts, phase mix, momentum direction).
2. **Per-Project Narrative** — paragraph per active project with movement. Function tag per milestone (Formula, Pack, Reg, Margin, Logistics, etc.).
3. **Functional Area Roll-up** — cross-project view by function area.
4. **Decisions Needed Across the Group** — items requiring Nicole/Danielle/Soraya/Perrine input this week.
5. **Look-ahead** — next 2 weeks of milestones, function-tagged.

Draft inline in Cowork chat. Wait for "go" before committing anything.

## After "go" — write sequence

When Alvin says "go":

1. **Generate the 6-tab HTML dashboard** via `sjs-status-reporter`. Tabs: Tab 1 §1 Portfolio Snapshot, Tab 2 §2 Per-Project Narrative, Tab 3 §3 Functional Area Roll-up, Tab 4 §4 Decisions Needed, Tab 5 §5 Look-ahead, Tab 6 Financial Signal Sweep (Skill 4 detail consolidated). Mirror the structure of `/pd-weekly/_template.html` in the repo.

2. **Read the current archive index** via GitHub Contents API or the published URL: fetch `https://acb-thelanding.netlify.app/data/pd-weekly-index.json` (or the GitHub raw URL). It's an array of `{ "date": "YYYY-MM-DD", "slug": "YYYY-MM-DD", "summary": "..." }` objects, newest first.

3. **Prepend this week's entry** to the index array. Build the new entry from §1 Portfolio Snapshot: `{ "date": "<today>", "slug": "<today>", "summary": "<one-line summary>" }`.

4. **Publish via the landing hub function.** POST to `https://acb-thelanding.netlify.app/.netlify/functions/landing-hub-publish` with the `x-hub-secret` header. Resolve the secret from the `HUB_FUNCTION_SECRET` environment variable (process env first, then `Skill Builder/.secrets/hub-secret`). On unresolved, follow the failure message in §Failure message of that file and stop. Body:

   ```json
   {
     "files": [
       { "path": "pd-weekly/[YYYY-MM-DD].html", "content": "<!doctype html>..." },
       { "path": "data/pd-weekly-index.json",    "content": "[ ... updated array ... ]\n" }
     ],
     "commit_message": "weekly PD update — [YYYY-MM-DD]"
   }
   ```

   On 200 `{ ok: true, commit_sha, commit_url, file_count: 2, deploy_url_hint }`: GitHub commit landed, Netlify auto-deploys within ~60 seconds. The live URL is `https://acb-thelanding.netlify.app/pd-weekly/[YYYY-MM-DD].html`.

   No local filesystem, no local git, no clone required. The function holds the GitHub PAT in Netlify env vars.

5. **Attach to Asana via Netlify Function.** POST to `https://acb-thelanding.netlify.app/.netlify/functions/pd-asana-attach` with the `x-hub-secret` header (same secret, resolved the same way as in step 4) and body: `{ "html": "<full HTML payload>", "taskGid": "1214208955674591", "filename": "pd-weekly-[YYYY-MM-DD].html" }`. On success, the HTML lands as an attachment on the running log task.

6. **Post the 5-section narrative as a comment** on Asana task GID 1214208955674591 (running log, running comments pattern). Append a live link at the bottom: `https://acb-thelanding.netlify.app/pd-weekly/[YYYY-MM-DD].html`.

## Failure handling

- If the `landing-hub-publish` call returns `ok: false`: surface the `error` + `detail` fields. `unauthorized` means the resolved secret doesn't match Netlify (re-check the `HUB_FUNCTION_SECRET` environment variable); `github_commit_failed` means the GitHub PAT held by the function has lost access. Both require the operator. Don't retry on a loop.
- If `pd-asana-attach` fails: post the 5-section narrative comment with the live archive URL anyway, then post a follow-up comment with the commit URL from step 4 as a fallback link to the source.

## Constraints

- Audience: Nicole, Danielle, Soraya, Perrine (Skin PD meeting circle).
- HITL gate: nothing commits until Alvin says "go."
- AC Brands writing rules — no banned words, no vibe emojis, paragraphs default.
