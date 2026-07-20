---
name: ayesha-weekly-briefing
description: >
  Produce Alvin's weekly Operations briefing for Ayesha Curry. Use this skill whenever
  Alvin asks to "run the weekly briefing," "update Slide 5 for Ayesha," "update Slide 6
  for Ayesha," "do my Ayesha update," "what do I send Ayesha this week," "prep the founder
  briefing," or references the Canva weekly briefing template, Slide 5, Slide 6, or
  Business Operations / PD-Ops updates for the founder. Alvin owns both Slide 5 (Business
  Operations — HR, logistics, purchasing, finance, S&OP, regulatory, fulfillment) and
  Slide 6 (Product Development — PD-Ops angle: landing hub and dashboards, AI/IT-side PD
  work, packaging readiness, supply chain risk affecting product). Nicole co-authors
  Slide 6 with her core PD content. Sweeps Asana (Ops Dashboard, OC3PL, SJ Shipping, PD
  Portfolio), Outlook, Fireflies, and PLM Supabase, filters for founder-level signal,
  drafts 5–7 bullets in Ayesha's language, and writes directly to the current week's
  Canva deck ("AC Weekly Briefing" series).
---

<!--
================================================================================
AC BRANDS WRITING STYLE — NO AI JARGON
================================================================================
This skill follows the AC Brands organization-wide writing rules. Full rules are
in the AC Brands Claude organization instructions. Key points, in brief:

  • BANNED WORDS: delve, leverage, utilize, facilitate, optimize, implement,
    streamline, empower, harness, unlock, unleash, foster, elevate, showcase,
    robust, seamless, comprehensive, navigate (metaphor), cutting-edge,
    innovative, dynamic, holistic, meticulous, tapestry, realm, landscape,
    ecosystem, paradigm, synergy, methodology, journey, voyage, etc.
  • BANNED OPENERS: "In today's fast-paced world," "When it comes to," etc.
  • BANNED TRANSITIONS: furthermore, moreover, additionally, notably, etc.
  • BANNED CLOSINGS: "In conclusion," "Ultimately," "At its core," etc.
  • BANNED PATTERNS: "It's not X — it's Y" reframes, self-posed rhetorical
    questions, three back-to-back tricolons.
  • FORMATTING: Paragraphs over bullets unless genuinely listy. No bolded lead
    words. No headers on short docs.
  • HYPHENS: Never use hyphens in anything written for Alvin. Em dashes or
    rewrite the sentence.
  • TONE: No flattery, no over-hedging, no false profundity. Write like a smart
    colleague talking to another smart colleague.
  • PUNCTUATION: For external-facing copy (including anything going to Ayesha),
    lean on commas and periods. Heavy em dash use is the strongest visible AI
    tell, so use them sparingly when Ayesha is the audience.
================================================================================
-->

# Ayesha Weekly Briefing

Alvin (VP of Operations) owns Slide 5 (Business Operations) of the weekly briefing Danielle (President) sends
to Ayesha (Founder). This skill runs the data gathering, drafting, and Canva write every
week, so Alvin doesn't have to rebuild the process from scratch.

Ayesha is the founder. She is not in the weeds. Every bullet that lands on
Slide 5 has to earn its place with her as the reader — not as a status update
for Nicole (PD consult) or Danielle.

---

## The Ask (Danielle's Framing)

From Danielle's email of Friday, April 10, 2026, subject "Re: Weekly Briefings Ayesha":

> Ayesha has requested a weekly briefing. I set up a template in Canva that we'll
> use moving forward. @Alvin Belt — Can you please provide 5–7 quick bullets on
> Slide 5? And add anything I missed to Slide 6 along with Nicole's additions?

**Slide ownership:**
| Slide | Section | Owner |
|---|---|---|
| 4 | Marketing/Creative | Soraya (Marketing Manager) — supported by Erin (Creative Director), Ivy (creative / design coordinator), Kate (Social Media Coordinator) |
| 5 | Business Operations | **Alvin (VP of Operations)** |
| 6 | Product Development (shared) | **Alvin (VP Operations)** owns PD-Ops content (landing hub, AI/IT, packaging readiness, supply chain risk affecting product); Nicole (Sr. Director, Consumer Strategy & Operations) owns core PD. Underlying PD ownership: Perrine (Milinyc Beauty contractor — PD owner). |
| 7 | Retail/Sales | Soraya (Marketing Manager) |
| 8 | AC/Non-SJS | Nicole (Sr. Director, Consumer Strategy & Operations) |

Alvin's deliverable: **5–7 bullets on Slide 5 (true ops) and 1–3 bullets on Slide 6
(PD-Ops angle), written every week regardless of Nicole's status on Slide 6.**

---

## Canva Design

Ayesha uses **one persistent deck**, not a new one each week. Danielle updates
the title/date each week, but the underlying design is the same file.

- **Series:** "AC Weekly Briefing"
- **Active design ID:** `DAHGewVQYFo` (title pattern: `AC Weekly Briefing [date]`)
- **Page count:** 13 slides (7 content + appendix)
- **Slide 5:** Business Operations (Alvin writes here)
- **Slide 6:** Product Development (shared with Nicole; Alvin writes PD-Ops content below hers)

**Default behavior:** use design ID `DAHGewVQYFo` every week unless Alvin says
otherwise. Do not search for a new deck each run — this is one file that gets
refreshed in place.

**Verify before writing each week:**
1. Call `Canva:get-design` with `DAHGewVQYFo` and check the title — it should
   reflect the current week (e.g. "AC Weekly Briefing 4/27"). If the title
   still shows an older week, Alvin should nudge Danielle to update it, but
   do not block on this — proceed with the write.
2. Call `Canva:get-design-content` on pages 5 and 6 to see what's currently
   there. If Slide 5 still has last week's content, that's the signal to
   overwrite. If Slide 5 has fresh placeholder text, write in.

**If Alvin says the design ID has changed:** update this skill's stored ID.
Do not assume the newest "AC Weekly Briefing" search result is correct —
Danielle may have older test decks ranked above the live one.

---

## Data Sources (Past 7 Days)

Sweep these every week. Not every source produces a bullet — they produce
candidate items that the founder filter then narrows down.

### 1. Asana — Operations Dashboard (GID `1208174221370391`)
- Tasks completed in last 7 days
- Status changes on parent projects
- Newly added milestones or high-priority tasks
- Tool: `asana_get_tasks` scoped to the project, filter by `modified_at` and `completed_at`

### 2. Asana — OC3PL Order Management (GID `1214235522292179`)
- Weekly fulfillment stats if Ciarra logged a weekly review
- Any flagged escalations
- Tool: `asana_get_tasks` with section filters

### 3. Asana — SJ Shipping Dashboard (GID `1206266539116267`)
- Shipping/carrier milestones
- Any inventory-to-3PL transitions in progress

### 4. Asana — 2026–2028 PD Portfolio (for Slide 6 contributions)
- Ops-flavored milestones inside PD projects (tooling, packaging readiness,
  3PL prep for a launch, supply chain risk)
- This is the lens for Slide 6 — not full PD status, just where ops intersects

### 5. Outlook — past 7 days
- Emails from OC3PL (`@oc3pl.com`), FWS, Element Packaging, HCT logistics
- Cross-functional ops threads where Alvin is sender or key decision point
- Tool: `outlook_email_search` with `afterDateTime: "7 days ago"`

### 6. Fireflies — past 7 days
- Any ops meetings (3PL reviews, weekly team syncs, supplier logistics calls)
- Tool: `fireflies_search` with `from:` filter

### 7. PLM Supabase (project `ujkabbffvhpewpbttmmy`)
- POs placed, received, or delayed in past 7 days
- Inventory adjustments worth surfacing
- Use `plm-assistant` skill for reads, do not bypass it

### 8. Regulatory rollup — via `regulatory-manager` (System C umbrella, v6.3+)
Read regulatory-manager's cross-skill rollup for founder-level signals across IL/claim/label work, retailer attestations, MoCRA/state filings, Leaping Bunny, SAE filings, and FDA recall reporting. Pull what the founder filter needs — see Founder Filter rule #5.
- MoCRA SAE filing in flight or recent (within 30 days)
- FDA recall in flight or recent (within 60 days)
- Statutory clock breach risk (any filing >80% of clock without Pedrero return)
- Retailer attestation overdue or imminent (within 30 days of renewal window)
- Pedrero engagement issues (overdue retainer, scope change, contract renewal)
- New regulatory landscape change (MoCRA implementation update, new state cosmetic regulation, retailer attestation criteria revision, Toxic-Free Cosmetics Act enforcement update)
- Tool: invoke `regulatory-manager` with "any founder-level regulatory items this week" or read SJS Regulatory Management (gid `1214660807386611`) and SJS Reportable Events (gid `1214660834583706`) directly via Asana

---

## The Founder Filter

This is what separates a Slide 5 bullet from internal ops noise. An item earns
a bullet only if it clears **at least one** of these:

1. **Decision made or milestone hit** that unblocks the business
   ↳ Example: "3PL transition from FWS to OC3PL completed Tuesday."

2. **Risk or material change** to timing, cost, or a launch
   ↳ Example: "Castaway Cleansing Oil deco tooling slipped two weeks; Jan is pushing Element for recovery."

3. **Cross-functional impact** — changes what marketing, creative, PD, or sales has to do
   ↳ Example: "Ulta Marketplace inventory locked for June Week 3 launch; creative has green light to schedule photography."

4. **Founder-relevance** — something Ayesha would want to reference if asked publicly, on a call, or by a board member
   ↳ Example: "Completed disposition plan for remaining Sweet July Home product; all donations by EOQ."

5. **Regulatory** — any founder-level regulatory signal from regulatory-manager (System C umbrella) per Data Source #8. Specifically: SAE filing in flight or recent (30 days), recall in flight or recent (60 days), statutory clock breach risk, retailer attestation overdue or imminent, Pedrero engagement issues, regulatory landscape change. These are founder-level by default — Ayesha needs visibility.
   ↳ Example: "Sephora Clean attestation for Castaway Cream renews 2026-06-30; evidence package staged with Pedrero."
   ↳ Example: "Leaping Bunny annual renewal due 2026-07-10; supplier attestation chain on track."

### What does NOT earn a bullet

- Internal task hygiene ("updated the Asana board")
- Supplier back and forth that didn't resolve anything
- Individual emails sent or received
- Routine PO placements or standard inventory moves
- Meetings that happened but produced no decision

If the week is genuinely quiet, **produce 3 tight bullets, not 7 padded ones**.
Ayesha will trust the signal more if Alvin doesn't pad.

---

## Voice and Format

### Sentence shape
Past tense action plus outcome, or forward look with owner and timing.

Good:
- Visit to FWS Tuesday to analyze Sweet July Home and deep storage items; plan for complete disposition by EOQ.
- OC3PL transition hit its Week 3 milestones; all SKUs fulfilling from OC3PL as of Monday.
- Ulta Marketplace inventory locked for June Week 3 launch.

Bad:
- We are working on optimizing our 3PL transition to leverage the new warehouse.  (banned words, vague)
- The team is doing a great job on the fulfillment side.  (no substance)
- Had meetings about the 3PL.  (no outcome)

### Acronyms and supplier names
Ayesha may not remember every acronym. Translate internally:
- "OC3PL" → "our 3PL" (at least on first mention in the deck)
- "FWS" → "our previous 3PL" (fine to shorten after)
- "UBMP" → "Ulta Beauty Marketplace"
- "HCT" → fine as is, she knows HCT
- "KDC" → "KDC-One" or "our contract manufacturer"

After first mention in the deck, the acronym is fine.

### Length
Each bullet: one sentence. Two sentences maximum, and only if the second
sentence adds the "so what." Never three sentences.

### Hyphen rule (Alvin's standing preference)
No hyphens. Em dashes or rewrite. Note: for Ayesha-facing copy, lean on
commas and periods over em dashes (em dashes are the strongest AI tell in
external copy). A few em dashes across a deck is fine; a bullet with two of
them is not.

### Banned phrases (quick reference)
Anything in the AC Brands org writing rules is out. The worst offenders for
ops-style copy:
- "streamline," "optimize," "leverage," "implement"
- "robust," "seamless," "comprehensive"
- "ecosystem," "landscape," "methodology"
- "journey," "roadmap" (as metaphor — fine as a literal noun)

---

## Workflow

### Step 1 — Open the persistent deck
Use design ID `DAHGewVQYFo`. Call `Canva:get-design` to confirm it still
exists and check the current title (which reflects the week Danielle last
updated it to).

### Step 2 — Read current Slide 5 and Slide 6
Use `Canva:get-design-content` with `pages: [5, 6]`. This tells us:
- Whether the deck is freshly templated or already has content
- Whether Nicole has added her Slide 6 content yet (drives Step 6)

### Step 3 — Gather the past 7 days of data
Run the 7 sweeps listed in Data Sources. Produce a raw candidate list
with source attribution for each item, e.g.:
- `[Asana Ops Dash]` Completed: 3PL transition Phase 2 milestone
- `[Outlook/OC3PL]` Discussion on bubble mailer shipping surcharge
- `[Fireflies]` Weekly ops sync covered SJ Home disposition plan

### Step 4 — Apply the founder filter
Score each candidate against the four criteria. Cut anything that doesn't clear
at least one. If the remaining list is under 3, tell Alvin the week is quiet
and let him decide whether to pad or keep it short.

### Step 5 — Draft bullets in chat for Alvin's review
Always draft in chat first. Never write to Canva before Alvin has seen the bullets.
Format as a clean markdown list so he can scan fast. Include a short note on
any judgment calls:
- "Dropped the KDC PO acknowledgment — routine."
- "Surfaced the FWS disposition plan because EOQ is close."

### Step 6 — Draft Slide 6 PD-Ops contribution
Alvin writes Slide 6 every week, not just when Nicole has refreshed. Slide 6 is for
PD-Ops content: landing hub progress, AI/IT-side PD work, packaging readiness, supply
chain risk affecting product. Draft 1–3 bullets at the bottom of Slide 6's body, below
Nicole's PD content. Never overwrite Nicole's content — append below it.

If Nicole's Slide 6 content is stale (last week), append Alvin's bullets anyway and
flag to Alvin in the completion report that Nicole hasn't refreshed.

### Step 7 — Write to Canva on Alvin's go
Once Alvin approves:
- Write Slide 5 bullets replacing the template placeholder ("Business Operations" heading stays)
- Append Alvin's PD-Ops bullets to Slide 6 below Nicole's content (stale or fresh) once Alvin approves the draft
- Use `start-editing-transaction` + `perform-editing-operations` + `commit-editing-transaction`

### Step 8 — Confirm and hand back to Alvin
Respond with:
- Short confirmation that Slide 5 and Slide 6 are written
- Link to the Canva deck
- Suggested reply-all text for Danielle's thread: "Done on Slide 5 and Slide 6."

### Step 9 — Draft and post the Asana running-log comment
After the Canva write is confirmed, draft a comment for the running-log task in
Asana (Leadership Dashboard project, GID `1210917729477334` — task "Weekly
Briefing Log — Ayesha", GID `1214848731815764`). The comment captures what
landed in Canva that week.

**Comment body format:**

```
Week of [YYYY-MM-DD]

Slide 5 — Business Operations
• [bullet 1]
• [bullet 2]
...

Slide 6 — Product Development (PD-Ops)
• [bullet 1]
• [bullet 2]
...

[Flags, if any — e.g., "Nicole's Slide 6 content hadn't refreshed; bullets
appended below stale content." or "Deck title not updated yet."]
```

Show the drafted comment to Alvin in chat. **Hold the post until Alvin explicitly
says go.** Never auto-post. Once Alvin approves, post with `asana_create_task_story`
on task GID `1214848731815764`.

Same weekend rule applies: if Alvin says go on a Saturday or Sunday, hold the
post until Monday alongside the Canva write.

---

## Cadence and Timing

The skill is on-demand, not auto-scheduled. Alvin runs it when ready — usually
Thursday or Friday to land before Danielle's Friday ping.

**Do not run on the weekend** per Alvin's standing rule about no Asana
activity on weekends. If Alvin triggers this on a Saturday or Sunday, draft
in chat but hold both the Canva write and the Asana log post until Monday.

---

## Edge Cases

### The deck title still shows last week
Fine — Danielle updates the title when she sends. Proceed with the write.
Optionally flag to Alvin that the title hasn't been refreshed yet in case he
wants to ping Danielle.

### The deck content hasn't been reset from last week
Overwrite Slide 5 anyway — this is Alvin's slide and last week's content is
stale. Append Alvin's PD-Ops bullets to Slide 6 below Nicole's content regardless
of whether it's current; flag in the completion report if Nicole's content looks
stale.

### The design ID has changed (Danielle made a new file)
Ask Alvin for the new design ID and update the stored ID in the "Active
design ID" field above. Do not rely on search — Danielle may have multiple
decks titled "AC Weekly Briefing."

### Nicole hasn't added her Slide 6 content
Write Alvin's PD-Ops bullets to Slide 6 anyway, appended below whatever Nicole has
there (even if stale). Flag in the completion report that Nicole's content hasn't
refreshed so Alvin can nudge her.

### The week is quiet
Produce 3 bullets, not 7. Tell Alvin honestly: "Quiet week on ops. Three real
items, no padding." Ayesha will trust the signal more over time.

### Something is sensitive (layoffs, legal, executive)
Flag to Alvin in chat before drafting. Ask whether to include, paraphrase,
or hold. Never put sensitive content on a founder slide without explicit
confirmation.

### Canva API can't reach the deck
If `Canva:get-design` on `DAHGewVQYFo` fails, confirm the ID with Alvin
directly. Do not search — fall straight to asking him for the link.

### Asana log task is missing or unreachable
If `asana_get_task` on GID `1214848731815764` fails (task deleted, moved, or
permissioned out), do not auto-create a replacement. Tell Alvin the log task
isn't reachable, show the drafted comment in chat, and let him decide whether
to skip the log this week or point the skill at a new task. Update the GID in
this file once he confirms a replacement.

### Alvin declines to post the log comment
If Alvin says no or doesn't approve the comment, treat the briefing run as
complete without the log entry. Don't retry on the next run — each week stands
on its own.

---

## Reference: Sample Slide 5 Output

From the 4/20 template (Alvin's own prior entry, already on-brand):

> **Business Operations**
>
> Visit to FWS Tuesday to analyze the Sweet July Home and deep storage items
> that are remaining. Plan for complete disposition of remaining Sweet July
> Home product/donations by EOQ.

This is the target voice. One bullet there, five to seven in a normal week,
each as tight.

---

## Related Skills

- `oc3pl-order-manager` — source of OC3PL weekly fulfillment data
- `asana-pd-manager` — source of PD portfolio read for Slide 6 contributions
- `plm-assistant` — source of PLM Supabase reads
- `sjs-status-reporter` — different audience (brand team, not founder); do not
  confuse the two
- `sjs-pd-system` — master router; points here for Ayesha briefings

---

## Wiki context (runs before live queries)

Before composing the weekly briefing, sweep the most recently updated wiki pages from `public.wiki_pages`. Wiki pages are synthesized briefings that compound as bridge skills process emails and meetings — they capture what's changed in the last week more efficiently than re-scanning Asana, Fireflies, and Outlook from scratch.

### Which pages to read

- 5 most recently updated supplier pages
- 5 most recently updated SKU pages
- Pull specific pages by slug (`supplier/{slug}`, `sku/{slug}`, `contact/{slug}`, `topic/{slug}`) when a thread surfaces in the live sweep

### Read query

```sql
-- 5 freshest supplier pages
SELECT slug, title, content, updated_at
FROM public.wiki_lookup(p_page_type => 'supplier', p_limit => 5);

-- 5 freshest SKU pages
SELECT slug, title, content, updated_at
FROM public.wiki_lookup(p_page_type => 'sku', p_limit => 5);

-- Drill into a specific entity when needed
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/' || public.wiki_slugify('{vendor_name}'));
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context for that thread. Reduce redundant Asana/Fireflies re-scans. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live sweeps normally. |
| Page does not exist | Run live sweeps normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

The 10 most-recent pages are the founder-briefing pre-read. Compose Ayesha's update from the wiki signal first, then layer in anything from the live sweep that hasn't yet hit a wiki page. The wiki + live combination is what produces the 5–7 bullets.

### Write-back (stale pages only)

If the briefing surfaced genuine new signal not already in a referenced wiki page and the page is stale, update it:

```sql
UPDATE wiki_pages
SET content = '{updated synthesized content}',
    source_count = source_count + 1,
    last_source = 'manual',
    last_source_ref = 'retrieval-skill-writeback',
    updated_at = now()
WHERE slug = '{slug}';
```

Only on genuine new signal. Never on every read.

### What this skill does NOT do

- Does not create new wiki pages (bridge skills own all wiki writes)
- Does not write to wiki on every invocation — only on genuine stale updates
- Does not replace the live Asana, Fireflies, and Outlook sweeps — the wiki layer accelerates them, not substitutes them
