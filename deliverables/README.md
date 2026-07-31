# Deliverables

Outputs built from this repo that are meant to leave it. Committed so they survive
the session that produced them and so the next person can see how they were derived.

## AC Brands RACI — v5, 2026-07-31

Org-wide RACI. **99 activities across eleven functions, led by position with names
cross-referenced.** Built for the resource-needs conversation with Danielle and
Nicole, and updated to reflect the 2026-07-30 leadership review.

Three artifacts, one dataset:

- **`AC-Brands-RACI.html`** — the team-facing version. Position-led columns with
  status chips, collapsible function sections, click-a-position filtering, and the
  two open seats shown as columns with transition arrows on the rows they absorb.
  Sources are behind a per-row disclosure so the team isn't reading file paths.
  Self-contained: brand fonts and all styling are inlined, no external requests.
- **`AC-Brands-RACI.xlsx`** — the working tool. `RACI` carries a two-row header
  (position code, then holder) plus `Transitions to`, `Source` and `Notes`.
  `Analysis` has live COUNTIF formulas over Sheet 1 including projected A and R
  books once both seats are filled. `Gaps` lists open seats with salary bands,
  unowned functions, single points of failure and open items.
- **`AC-Brands-RACI-summary.md`** — the one-pager for Danielle and Nicole.

### What v5 changed

Real Marketing, Retail & Wholesale and Web activities, sourced from the **AC Brands landing
hub** rather than the skill suite. `data/links.json` in the `acb-thelanding` repo defines the
eleven business functions with an explicit `lead` each, and three read "Owned by TBD."

That file is the answer to a problem the earlier versions had: extracting ownership from the
skill suite is right for what the system automates and wrong as a proxy for what the business
does. There are no skills for marketing, wholesale or the website, so none of it was on the
matrix. Marketing went from 9 rows to 15, Retail & Wholesale from 2 to 5.

- **Soraya accountable for Marketing** — editorial calendar, Klaviyo email, paid media, social
  content, influencer and earned media, product copy, and the WITHIN relationship. 1 → 8 A rows.
- **Nicole accountable for all channels** — DTC, Amazon and wholesale together.
- **Danielle accountable for web**, with Nicole as systems and tech owner.
- **WITHIN** (digital marketing) and **Teknologics** (web development) added as partners.

**Every row now has a sourced owner.** No inferred owners remain. `verify.py` resolves
citations against both repos.

### What v4 changed

The three external partner organisations are now columns: **Pedrero Regulatory**,
**Ironclad Finance** (Dan Bender) and **Calm HR** (PEO and co-employer). Partners hold
R — they do the work — but never A, which stays with an employee. `verify.py` enforces
that.

This resolved two false negatives. Finance and People & Admin were reported as unowned
functions on the first pass because Ironclad and Calm HR appeared nowhere in this repo,
not because the work had no owner. `references/external-partners.md` now records all
six external parties — three organisations plus Erin, Jan and Perrine — and did not
exist before. Shopify revenue is now the only genuinely unowned row.

Finance accountability splits: Danielle on reporting, Alvin on cost. HR sits with Alvin
as liaison with Danielle co-approving.

### What v3 changed

Role corrections from Alvin on 2026-07-31, on top of v2:

- **Erin Hover is a contractor and the lead technical authority on packaging and
  artwork.** Packaging development, artwork execution and the label artwork archive
  answer to her; Jan executes under her; Perrine consults on formula contact.
- **Danielle holds brand guideline custody and campaign direction**, and is consulted
  across all Creative and Marketing rows. Campaign direction is a new row — it was
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
- **Alvin owns the framework** — quality management system, SOP framework, this RACI.
- **Two open seats are columns.** Ops Specialist recruiting now, PD Specialist phased
  in after. 32 rows transition on hire, 16 each; 29 come off Alvin, 3 off Nicole.
  His R book drops from 55 to 26, and rows with no second pair of eyes drop from
  42 to 25.

No job titles changed. What changed is who holds which gate. The corresponding
role-label changes in the skill role-maps *are* real, because those are runtime
config that decides where a skill routes an approval — see the History sections in
`quality-manager`, `asana-pd-manager` and `regulatory-manager` role-maps.

### How it was built

Ownership was extracted from this repo, not assumed — `.claude/skills/` (SKILL.md
plus every `references/` file), `references/architecture/`, `decisions/`,
`context/`, `connections.md`, `MEMORY.md` and `scheduled-prompts/`. Roles resolve
to people only through the three canonical role-maps:

- `.claude/skills/asana-pd-manager/references/role-map.md` — PD
- `.claude/skills/quality-manager/references/role-map.md` — Quality (System B)
- `.claude/skills/regulatory-manager/references/role-map.md` — Regulatory (System C)

The roster was cross-checked against live Asana workspace users, per the standing
lesson in `MEMORY.md` about verifying against the actual system rather than what a
skill's own documentation claims.

Beyond the repo, v2 also draws on four primary sources: the Leadership Business
Review of 2026-07-30 (Fireflies `01KYN0DNAB4M7WY99VEEP5CGSV`), the 2026-07-27 email
to Danielle titled "Proposed Ops Positions - PD Specialist & Ops Specialist," and
the two job descriptions attached to it. Eleven rows rest on those rather than on
anything in this repo; `verify.py` reports them separately so the distinction stays
visible.

- `raci_rows.py` — the row data and the position roster. One tuple per activity:
  function, activity, A, R, consulted, informed, transition, source, notes. Edit
  here, not in the spreadsheet or the HTML.
- `build_raci.py` — renders the three xlsx sheets from `raci_rows.py`.
- `build_html.py` — renders the team-facing page from the same data. Expects the
  base64 font payloads alongside it; regenerate them from
  `.claude/skills/sweet-july-skin-brand/assets/fonts/`.
- `transform_v2.py` through `transform_v5.py` — the migration chain. Kept for the audit trail: it shows every
  A/R reassignment and which rows were added, rather than the v2 data appearing
  from nowhere.
- `verify.py` — seven checks: no departed-employee references in any cell of any
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
functions to zero — and none of them were ever actually ownerless. Finance and HR needed
the partner organisations added; Marketing, wholesale and Shopify revenue needed the
landing hub. Absence from a source meant the source had a gap.

30 of the 99 rows cite something outside this repo — the leadership review, a job
description, the landing hub, or Alvin directly. `verify.py` reports those separately so
the distinction between extracted and stated stays visible.

Skill bodies and SOP text still say "QA Lead" and "Voice of Customer" in places.
That was deliberate — rewriting nine skills' prose is a larger change than this one
warranted, and the role-maps are what the skills read at runtime. Each role-map
carries a resolution note: process gates resolve to Quality Gate (Nicole), technical
gates to Technical Advisor (Perrine). If a skill ever behaves as though Perrine
still holds a process gate, the role-map is right and the prose is stale.

Coverage is Sweet July Skin plus org-level work, which is what the sources
describe. Sweet July, the lifestyle brand, has no skill coverage in this repo, so
its merch, licensing and non-skincare retail functions are recorded on the `Gaps`
sheet as an uncovered brand rather than invented as rows.
