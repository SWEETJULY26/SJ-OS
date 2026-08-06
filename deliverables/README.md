# Deliverables

Outputs built from this repo that are meant to leave it. Committed so they survive
the session that produced them and so the next person can see how they were derived.

## AC Brands RACI: v8, 2026-08-06

Org-wide RACI. **94 activities across eleven functions, led by position with names
cross-referenced.** Built for the resource-needs conversation with Danielle and
Nicole, and updated to reflect the 2026-07-30 leadership review and Alvin's own pass over
the matrix on the page on 2026-08-06.

Three artifacts, one dataset:

- **`AC-Brands-RACI.html`**: the team-facing version, and since v7 an editing surface
  as well. Position-led columns with status chips, collapsible function sections,
  click-a-position filtering, and the two open seats shown as columns with transition
  arrows on the rows they absorb. Clicking an activity opens a breakdown of what the work
  is, with an example and the source. Self-contained: brand fonts and all styling are
  inlined, no external requests. See Activity breakdowns and Editing below.
- **`AC-Brands-RACI.xlsx`**: the working tool. `RACI` carries a two-row header
  (position code, then holder) plus `Transitions to`, `Source` and `Notes`.
  `Analysis` has live COUNTIF formulas over Sheet 1 including projected A and R
  books once both seats are filled. `Gaps` lists open seats with salary bands,
  unowned functions, single points of failure and open items.
- **`AC-Brands-RACI-summary.md`**: the one-pager for Danielle and Nicole.

### Activity breakdowns

Clicking an activity opens a side drawer with five things: a plain description of what
the work actually is, a worked example using real SKUs and vendors, who holds each
letter with names and titles, why it sits where it does, and the `file:line` source.
On mobile the same panel arrives as a bottom sheet. Escape, the scrim and the Close
button all dismiss it, and focus returns to the activity you came from.

The text lives in `activity_notes.py`, keyed by exact activity string, with a `what`
and an `example` per row. All 94 rows are covered and `verify.py` fails the build if
any row loses its breakdown or if a breakdown exists with no matching row. A row added
on the page has no entry, so its drawer says so rather than showing an empty section.

This replaced the per-row source disclosure, which showed a file path and nothing else.
The matrix says who owns a thing; the drawer is what makes it legible to somebody who
was not in the meeting where it was named.

### The round trip

v8 is the first version where the data came back from the page instead of only going out
to it. Alvin edited the published page, hit **Export JSON**, and the file folded back into
`raci_rows.py`. The steps, in case it happens again:

1. Diff the export against the published payload rather than trusting it wholesale. What
   matters is which rows changed letters, which were deleted, and whether anything was
   added on the page (an added row has no breakdown, so it needs one written).
2. Check the invariants before writing anything: at least one A, exactly one R, no open
   seat or partner org holding A, no position holding two letters on one row.
3. Rewrite the rationale notes on rows whose letters moved. This is the part that cannot
   be automated. A note reading "PD Lead owns the technical call outright" on a row whose
   A is now the President is worse than no note, because it reads as sourced.
4. Prune `activity_notes.py` for deleted rows or check 2b fails.
5. Bump `PUB["version"]`. The localStorage key is version-scoped, so the bump retires
   every viewer's local copy and the new baseline becomes what they see. Do this only when
   the published data has caught up with the edits, never mid-round.

What is deliberately not automated: the role-map runtime config under `.claude/skills/`.
Those files decide where a live approval routes. If an edit on the page moves A on a
quality or regulatory row, the matrix and the automation disagree until Alvin says which
one is right. Flag it, do not reconcile it.

### Editing

The page renders the matrix from a JSON payload rather than from baked-in markup, so
it can be changed in the browser. Press **Edit** and every cell becomes a button that
cycles through blank, C, I, A, A/R and R and back. Shift-click steps backwards. Activity names
and function names become editable text, rows can be reordered within a function, moved
to another function, added or deleted, and a whole function can be added.

**A can be shared, R cannot.** An activity may have several positions accountable, so
taking A displaces nobody. This replaced the original one-A rule on 2026-08-05 at Alvin's
instruction.

R is single, and the two states that claim it, **A/R** and **R**, sit at the end of the
cycle for a reason: clicking through a cell must never rewrite a different one. If R is
already held on that activity, cycling skips past both and names the holder, so the only
way to move R is to clear their cell first. That is two clicks rather than one, and it is
the whole reason a click can no longer disturb a cell you were not looking at. A/R and a
separate A can sit on the same activity: one position both answers and does the work,
another only answers.

Two restrictions still hold, and `verify.py` enforces both on the data. An open seat can
only receive the transition arrow, because a vacancy cannot be accountable. A partner
organisation can hold R but never A, because accountability does not leave the company.
An activity with no A at all, or with nobody doing the work, is flagged in the margin and
counted in the banner rather than silently accepted.

Edits live in the viewer's own browser via `localStorage`, keyed to the payload
version. They survive a reload, they are not shared with anyone else opening the link,
and **Revert to published** discards them. There is no shared-state capability
available to this account, so a genuinely multi-editor page is not currently possible.
The round trip is **Export JSON**, which uses the `downloads` runtime capability and
falls back to a blob link, then hand the file back so `raci_rows.py` can be updated and
everything regenerated. **Copy for Excel** puts the whole matrix on the clipboard as
tab-separated text. **Import JSON** loads an export back in.

**No browser modals.** The artifact frame is sandboxed without `allow-modals`, so
`confirm()` and `prompt()` are ignored by the browser: `confirm()` returns false and
`prompt()` returns null, with only a console warning. Any control built on them fails
silently. Delete, Revert to published and Add function all did until 2026-08-05. Delete
and Revert now act immediately and offer Undo on the toast, and Add function uses an
inline text field. Do not reintroduce `confirm`, `prompt` or `alert` in `build_html.py`:
test in a sandboxed iframe, not just a local file, because a bare `file://` open has
modals enabled and hides the bug.

Bumping `PUB["version"]` in `build_html.py` changes the storage key, which retires every
viewer's local edits. Do that when the published data moves far enough that stale local
copies would mislead, and not otherwise.

### What v7 changed

The HTML page became editable, and the page is now client-rendered from the payload
rather than server-rendered as static rows. No data changed: same 102 activities, same
owners, same counts.

The A column widened from one holder to many. `raci_rows.py` still carries a single code
per row because that is what the data says today, but `build_raci.py` accepts either a
code or a list of codes, and `verify.py` now checks for **at least one** A and exactly one
R, reporting how many rows carry more than one. So an export with shared accountability
folds straight back in without another schema change.

### What v6 changed

**Coastal Interactive** added as the managed IT service provider: back-end infrastructure,
identity and endpoint management, equipment procurement and onboarding, asset lifecycle.
Alvin is the liaison and accountable; Coastal is responsible. Distinct from Teknologics:
Coastal is the back end, Teknologics is the storefront. Nine external parties now.

**Perrine and Soraya are never blank on a Product Development row.** Perrine was blank on
one, Soraya on all eight. Both Informed at minimum now. A blank cell is ambiguous in a way
Informed is not.

### What v5 changed

Real Marketing, Retail & Wholesale and Web activities, sourced from the **AC Brands landing
hub** rather than the skill suite. `data/links.json` in the `acb-thelanding` repo defines the
eleven business functions with an explicit `lead` each, and three read "Owned by TBD."

That file is the answer to a problem the earlier versions had: extracting ownership from the
skill suite is right for what the system automates and wrong as a proxy for what the business
does. There are no skills for marketing, wholesale or the website, so none of it was on the
matrix. Marketing went from 9 rows to 15, Retail & Wholesale from 2 to 5.

- **Soraya accountable for Marketing**: editorial calendar, Klaviyo email, paid media, social
  content, influencer and earned media, product copy, and the WITHIN relationship. 1 → 8 A rows.
- **Nicole accountable for all channels**: DTC, Amazon and wholesale together.
- **Danielle accountable for web**, with Nicole as systems and tech owner.
- **WITHIN** (digital marketing) and **Teknologics** (web development) added as partners.

**Every row now has a sourced owner.** No inferred owners remain. `verify.py` resolves
citations against both repos.

### What v4 changed

The three external partner organisations are now columns: **Pedrero Regulatory**,
**Ironclad Finance** (Dan Bender) and **Calm HR** (PEO and co-employer). Partners hold
R (they do the work) but never A, which stays with an employee. `verify.py` enforces
that.

This resolved two false negatives. Finance and People & Admin were reported as unowned
functions on the first pass because Ironclad and Calm HR appeared nowhere in this repo,
not because the work had no owner. `references/external-partners.md` now records all
six external parties (three organisations plus Erin, Jan and Perrine) and did not
exist before. Shopify revenue is now the only genuinely unowned row.

Finance accountability splits: Danielle on reporting, Alvin on cost. HR sits with Alvin
as liaison with Danielle co-approving.

### What v3 changed

Role corrections from Alvin on 2026-07-31, on top of v2:

- **Erin Hover is a contractor and the lead technical authority on packaging and
  artwork.** Packaging development, artwork execution and the label artwork archive
  answer to her; Jan executes under her; Perrine consults on formula contact.
- **Danielle holds brand guideline custody and campaign direction**, and is consulted
  across all Creative and Marketing rows. Campaign direction is a new row. It was
  missing entirely, which is why the President had no Marketing presence.
- **Ayesha is consulted wherever the brand carries her name** and keeps sole
  accountability for brand-line moves.

Three of the four holders in the packaging and creative chain are contractors, and
between them they hold 11 activities. On the `Gaps` sheet.

### What v2 changed

Per the 2026-07-30 leadership review (see `decisions/log.md`):

- **Nicole holds the quality gate.** 10 of 13 Quality rows are accountable to her,
  up from 2. Her total book goes from 8 rows to 21.
- **Perrine moves to technical advisor.** Retains A on the 8 rows where judgment is
  formula or testing; consult-only on process gates. Down from 11.
- **Alvin owns the framework**: quality management system, SOP framework, this RACI.
- **Two open seats are columns.** Ops Specialist recruiting now, PD Specialist phased
  in after. 32 rows transition on hire, 16 each; 29 come off Alvin, 3 off Nicole.
  His R book drops from 55 to 26, and rows with no second pair of eyes drop from
  42 to 25.

No job titles changed. What changed is who holds which gate. The corresponding
role-label changes in the skill role-maps *are* real, because those are runtime
config that decides where a skill routes an approval. See the History sections in
`quality-manager`, `asana-pd-manager` and `regulatory-manager` role-maps.

### House style

No em dashes anywhere in these deliverables, per Alvin's instruction on 2026-08-03.
Commas, colons, semicolons and full stops instead. The HTML page also has no
"What changed" section; version history lives in this README, not on the page the
team reads. Keep both rules when editing `raci_rows.py` or either build script.

### How it was built

Ownership was extracted from this repo rather than assumed, from `.claude/skills/` (SKILL.md
plus every `references/` file), `references/architecture/`, `decisions/`,
`context/`, `connections.md`, `MEMORY.md` and `scheduled-prompts/`. Roles resolve
to people only through the three canonical role-maps:

- `.claude/skills/asana-pd-manager/references/role-map.md`: PD
- `.claude/skills/quality-manager/references/role-map.md`: Quality (System B)
- `.claude/skills/regulatory-manager/references/role-map.md`: Regulatory (System C)

The roster was cross-checked against live Asana workspace users, per the standing
lesson in `MEMORY.md` about verifying against the actual system rather than what a
skill's own documentation claims.

Beyond the repo, v2 also draws on four primary sources: the Leadership Business
Review of 2026-07-30 (Fireflies `01KYN0DNAB4M7WY99VEEP5CGSV`), the 2026-07-27 email
to Danielle titled "Proposed Ops Positions - PD Specialist & Ops Specialist," and
the two job descriptions attached to it. Eleven rows rest on those rather than on
anything in this repo; `verify.py` reports them separately so the distinction stays
visible.

- `activity_notes.py`: the per-activity `what` and `example` shown in the drawer,
  keyed by exact activity string. Edit here when an activity is renamed, or the
  breakdown stops matching its row and `verify.py` will say so.
- `raci_rows.py`: the row data and the position roster. One tuple per activity:
  function, activity, A, R, consulted, informed, transition, source, notes. Edit
  here, not in the spreadsheet or the HTML.
- `build_raci.py`: renders the three xlsx sheets from `raci_rows.py`.
- `build_html.py`: renders the team-facing editable page from the same data. The row
  data goes in as a JSON payload and the matrix is built in the browser, so the CSS
  and the JS in this file are the page. Expects the
  base64 font payloads alongside it; regenerate them from
  `.claude/skills/sweet-july-skin-brand/assets/fonts/`.
- `transform_v2.py` through `transform_v6.py`: the migration chain. Kept for the audit trail, so it shows every
  A/R reassignment and which rows were added, rather than the v2 data appearing
  from nowhere.
- `verify.py`: eight checks. No departed-employee references in any cell of any
  sheet or in the summary or the HTML; exactly one A and one R per row; every cited
  `file:line` resolves in this repo; every repo citation carries ownership language;
  no open seat holds A or R and no partner organisation holds A, since a vacancy cannot be
  accountable and accountability does not leave the company; the nine
  role-maps and the decisions log match the matrix; and roster sanity. Run it after
  any edit to `raci_rows.py`.

```
python3 build_raci.py && python3 build_html.py && python3 verify.py
```

`build_html.py` needs `Adrianna-Regular.ttf.b64` and `Adrianna-Demibold.ttf.b64` in
its working directory:

```
python3 -c "import base64,pathlib;
d=pathlib.Path('../.claude/skills/sweet-july-skin-brand/assets/fonts');
[open(f.name+'.b64','w').write(base64.b64encode(f.read_bytes()).decode())
 for f in [d/'Adrianna-Regular.ttf', d/'Adrianna-Demibold.ttf']]"
```

Both scripts expect `~/Documents/` as the output directory and this repo at
`/home/user/SJ-OS`; adjust the paths at the top of each if that changes.

### Known limits

Nothing on the matrix is unowned. Across v1–v5 the unowned list went from three
functions to zero, and none of them were ever actually ownerless. Finance and HR needed
the partner organisations added; Marketing, wholesale and Shopify revenue needed the
landing hub. Absence from a source meant the source had a gap.

30 of the 99 rows cite something outside this repo: the leadership review, a job
description, the landing hub, or Alvin directly. `verify.py` reports those separately so
the distinction between extracted and stated stays visible.

Skill bodies and SOP text still say "QA Lead" and "Voice of Customer" in places.
That was deliberate. Rewriting nine skills' prose is a larger change than this one
warranted, and the role-maps are what the skills read at runtime. Each role-map
carries a resolution note: process gates resolve to Quality Gate (Nicole), technical
gates to Technical Advisor (Perrine). If a skill ever behaves as though Perrine
still holds a process gate, the role-map is right and the prose is stale.

Coverage is Sweet July Skin plus org-level work, which is what the sources
describe. Sweet July, the lifestyle brand, has no skill coverage in this repo, so
its merch, licensing and non-skincare retail functions are recorded on the `Gaps`
sheet as an uncovered brand rather than invented as rows.
