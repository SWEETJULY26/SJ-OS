# Deliverables

Outputs built from this repo that are meant to leave it. Committed so they survive
the session that produced them and so the next person can see how they were derived.

## AC-Brands-RACI.xlsx — 2026-07-31

Org-wide RACI for AC Brands, built for the leadership business review with Danielle
and Nicole as input to a resource-needs conversation.

Three sheets. `RACI` holds 66 activities across eleven functions, one column per
person, with a `Source (file:line)` column pointing back into this repo for every
row. `Analysis` covers ownership concentration, rows with no second approver,
unowned functions, and what the interim split costs — with live COUNTIF formulas
over Sheet 1, so the counts move if a row changes. `Gaps` lists unowned functions,
vacant seats, single points of failure and open items, each with a suggested owner
and a rough monthly hours estimate.

`AC-Brands-RACI-summary.md` is the one-page version sent to Danielle and Nicole
ahead of the meeting.

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

- `raci_rows.py` — the row data. One tuple per activity: function, activity, A, R,
  consulted, informed, source, notes. Edit here, not in the spreadsheet.
- `build_raci.py` — renders the three sheets from `raci_rows.py`.
- `verify.py` — five checks: no departed-employee references in any cell, exactly
  one A and one R per row, every cited `file:line` still resolves in this repo,
  every citation carries ownership language, and roster sanity. Run it after any
  edit to `raci_rows.py`.

```
python3 build_raci.py && python3 verify.py
```

Both scripts expect `~/Documents/` as the output directory and this repo at
`/home/user/SJ-OS`; adjust the paths at the top of each if that changes.

### Known limits

One row has no source at all — accounts payable, bookkeeping and payroll. Finance
appears nowhere in this repo as owned work. Two further rows (Shopify revenue
ownership, employee onboarding and offboarding) cite context but no ownership
statement. All three are marked `INFERRED` in the Notes column, and A defaults to
Alvin because the work falls to him in practice rather than because a source says
so.

Coverage is Sweet July Skin plus org-level work, which is what the sources
describe. Sweet July, the lifestyle brand, has no skill coverage in this repo, so
its merch, licensing and non-skincare retail functions are recorded on the `Gaps`
sheet as an uncovered brand rather than invented as rows.
