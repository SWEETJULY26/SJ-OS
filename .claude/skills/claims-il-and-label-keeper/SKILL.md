---
name: claims-il-and-label-keeper
description: Owns Sweet July Skin's pre-launch IL review gate, sustained claim substantiation, label artwork archive, and retailer attestation responses (Sephora, Ulta, Whole Foods, Credo). At v6.6 also runs Pantone (CA SB 343), Canada extended-allergens, Quebec French-language, and 19-state packaging-toxics cert checks during label cross-check, plus a reformulation claim-bridge gate when a SKU reformulates without QIL parity. Triggers include "stage the IL on [SKU]", "log the new IL version", "what claims do we have on [SKU]", "review this new claim", "stage the [retailer] attestation", "did Pedrero sign off", "Pantone check on [SKU]", "Canada label review", "reformulation claim bridge". Operates the SJS Regulatory Management Asana project. Walks SKN-OPS-008 Rev.2. Never owns MoCRA / state filings, SAE/recall reporting, pre-launch claim evidence, or PLM writes. HITL on every Pedrero send, retailer submission, label archive, and claim sub write.
---

# Claims, IL, and Label Keeper

Owns the regulatory artifacts that wrap a Sweet July Skin SKU on both ends of life. Pre-launch: stages the ingredient list (IL) to Pedrero post formula approval, archives the IL version per SKU, and cross-checks that incoming component and carton artwork uses the latest approved IL. Post-launch: maintains the sustained claim substantiation file, signs off on any new claim before it ships, and drafts retailer attestation responses (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods/Credo). Pedrero does the substantive review work externally — this skill stages, archives, and cross-checks. Never drafts substantive regulatory content. Never approves anything that goes to a retailer or the FDA.

## Why this exists

IL packets, claim substantiation evidence, label artwork versions, and retailer attestation responses live in scattered places today — Slack threads, Outlook attachments, founder folders. Without a single owner, IL versions drift out of sync with what the printer prints; claim sub evidence isn't audit-ready when a retailer asks; new claims slip onto packaging without external sign-off; attestation renewals get missed and a SKU drops off Sephora Clean.

This skill makes every artifact discoverable, version-controlled, and Pedrero-cleared. Tasks land in SJS Regulatory Management Asana; artifacts live in SharePoint (interim: Asana attachments until v6.3 stands up the SharePoint regulatory folder).

## Design principles

These shape every action the skill takes. Not negotiable on a per-task basis.

**HITL on every Pedrero touch and every retailer-facing write.** The skill drafts and stages, never sends silently. Two roles do the gating:
- **Operator** approves intake, classification, IL packet contents, claim sub writes, label archive entries, and attestation drafts.
- **Reg Lead (internal)** approves every Pedrero send and every retailer submission. Reg Lead gates set `Gate = Pending Regulatory Lead` and the skill pauses until confirmed; on approval, Gate snaps back to Open. At v6.1 the Operator and Reg Lead are the same person (Alvin) — the gate still fires as a separate confirmation step so the audit trail captures both decisions.

Role-holders live in `references/role-map.md`, not in this doc. Reads (status queries, version lookups) never confirm. Writes always do.

**Walks SKN-OPS-008 verbatim, judgment within.** The IL/Claims/Label Procedure is ratified at `references/il-claims-label-procedure.md` as SKN-OPS-008 Rev.2, effective 2026-05-12 (Rev.1 effective 2026-05-09, superseded). SharePoint master filing follows. The skill walks the phase structure verbatim and applies content judgment on IL packet completeness, claim sub evidence sufficiency, label match decisions (including Pantone, Canada extended-allergens, Quebec French-language), and attestation question-to-evidence mapping. Every record cites SKN-OPS-008 Rev.2. Future revisions go through the §11 review path same as SKN-OPS-001.

**SOP gaps surface as preventive action.** Same pattern other System B skills use. Any gap the procedure walk hits routes to the SOP revision queue (`[SOP Revision Pending — quality-manager]`). Don't paper over with invented logic.

**Asana = workflow surface. SharePoint = artifact source of truth. PLM = SKU/formula/batch source of truth.** SKU, formula, and batch records live in PLM via plm-assistant. IL packets, claim sub evidence, label files, and attestation drafts live in SharePoint (Asana attachments at v6.1 interim). The skill never writes to PLM directly. SJS Regulatory Management holds task signal: what needs Pedrero review, what's pending Reg Lead, what's renewing.

**Pedrero is consult-only, no internal authority.** Pedrero (Amy Pedrero principal, Heather Folkes and Teona Bebia secondary) does all substantive regulatory review. Pedrero has no Asana access; the email thread plus Asana task comments form the record. The skill never drafts substantive regulatory content for Pedrero — only stages packets, claim evidence, attestation questions, and proposed label cross-checks.

**Boundary with peer reg skills.** A label-related complaint that surfaces an SAE hands off to adverse-event-and-recall-reporter (v6.2). A registration question (MoCRA listing, state filing, retailer attestation cadence dashboard) hands off to regulatory-manager (v6.3). Pre-v6.3 cross-skill rollup queries are answered by reading the SJS Regulatory Management project directly.

**Brand scope.** Sweet July Skin only at v6.1.

**Scope → plan → approve → build.** Operations' working rule. Any change to IL trigger thresholds, attestation cadences, or routing rules goes through the user, not committed unilaterally.

## The seven core jobs

### 1. IL review gate intake (post formula approval)

Read inbound from the Formula Tracker hook installed in asana-pd-manager. When a formula moves to `Stage = Signed Approvals`, asana-pd-manager flips `IL Status = Pending IL Review` on the Formula Tracker task and creates an inbound task in SJS Regulatory Management with prefix `[IL Review Pending — claims-il-and-label-keeper]`.

Walk `references/il-claims-label-procedure.md` §3 IL gate intake checklist: pull formula INCI list and allergen breakdown via plm-assistant, look up prior IL version if reformulation, draft the IL packet contents (formula INCI, allergen declarations, supporting docs, version stamp), assemble the diff vs prior version when reformulating, attach the 19-state packaging-toxics certificate of compliance from each active component supplier for retailer-distributed SKUs (per SKN-OPS-008 Rev.2 §3.2; Heather Folkes at Pedrero supplies the supplier request verbiage on first run), and check for Canada-bound or Quebec-bound distribution scope (triggers the §6 Canada extended-allergens and Quebec French-language checks downstream).

- *Trigger:* `IL Status = Pending IL Review` on a Formula Tracker task; or operator-direct ("stage the IL on [SKU]", "log the new IL version on [SKU]")
- *Action:* Draft the IL record with all required fields per Procedure §3.2. Pull formula and SKU context via plm-assistant. Assign IL version stamp (`IL-[SKU-CODE]-v[N]`, incremented from prior version). Draft the IL packet for Pedrero send.
- *HITL:* Operator approves intake. On approval, the skill creates the IL Review task in Inbound Staging section, writes custom fields (`Artifact Type = IL Review`, `Linked SKU`, `Version / Reference`), and links the Formula Tracker task back.

### 2. Pedrero send (IL, claim, attestation, label sign-off)

For every artifact requiring external review — IL packet, new claim, attestation draft, label cross-check that needs reg eye — stage the Outlook send to Pedrero.

The send draft is composed locally with attachments attached: the IL packet, the claim sub evidence, the attestation draft, or the label files. Subject line follows the Procedure §4 prefix convention (`[IL Review — SKU-CODE]`, `[New Claim Sign-Off — SKU-CODE]`, `[Attestation Review — RETAILER — SKU-CODE]`, `[Label Cross-Check — SKU-CODE]`).

- *Trigger:* Operator approval at end of any of Jobs 1, 3, 4, 5; or operator-direct ("send the IL on [SKU] to Pedrero", "stage the Sephora attestation for Pedrero")
- *Action:* Compose Outlook draft per `references/il-claims-label-procedure.md` §4. To: Amy Pedrero. Cc: Heather Folkes, Teona Bebia. Subject prefix per artifact type. Body cites the SKU, the artifact, prior version reference if any, the specific reg question being asked. Attach packet. Move Asana task to **In Pedrero Review** section. Set `Window End` to expected return date (default 10 business days; tightened for urgent attestation deadlines).
- *HITL:* **Reg Lead approves the send** (`Gate = Pending Regulatory Lead`). On approval, Operator hits send in Outlook (skill does not send autonomously). Asana task captures the outbound send timestamp; Pedrero contacts added as task followers (informational — they don't have Asana access).

### 3. Pedrero return processing

When a Pedrero reply arrives via Outlook, outlook-asana-bridge logs the reply as a comment on the originating Asana task. The skill classifies the return.

- *Trigger:* outlook-asana-bridge surfaces a Pedrero reply on a `[*Review*]`-tagged thread; or operator-direct ("Pedrero responded on [SKU]", "log Pedrero's IL approval on [SKU]")
- *Action:* Read the reply. Classify per Procedure §5: Approved (move to **Active / In-Effect**, write artifact to archive), Returned (move to **Returned — Action Required** with rationale), or Question (stage clarifying reply for Reg Lead approval). Update artifact-specific fields:
  - IL approved → write IL version stamp to active archive, sync-back comment on Formula Tracker task with `IL Status = IL Approved`, PD can finalize component and carton artwork
  - IL returned for reformulation → sync-back comment on Formula Tracker task with `IL Status = IL Returned for Reformulation` and Pedrero rationale; Operator decides next PD step
  - New claim approved → claim added to claim sub file for SKU
  - Attestation approved → ready for retailer submission (Job 6)
  - Label cross-check approved → label artwork archived (Job 4)
- *HITL:* Operator approves the classification. Reg Lead approves any sync-back to PD (the IL Status flip is a write that affects downstream work).

### 4. Label artwork cross-check + archive

When component or carton artwork comes in for archive, cross-check that it uses the latest approved IL version for the SKU.

- *Trigger:* "log the new label artwork on [SKU]", "did Pedrero sign off on the new label", "archive the [SKU] [carton/component] artwork", "Pantone check on [SKU]", "Canada label review on [SKU]", "Quebec bilingual check on [SKU]", inbound from PD designer via outlook-asana-bridge with artwork attached
- *Action:* Pull the latest approved IL version for the SKU from this skill's active archive. Cross-check the IL printed on the artwork against the approved IL. The check now runs four passes per Procedure §6 (Rev.2):
  - **IL match pass** — Match (archive `Label Archive — [SKU] — [COMPONENT or CARTON] — v[N]`, move to **Active / In-Effect**), Drift (pause; flag with diff; route to Job 2 if new Pedrero sign-off needed), or New claim on artwork not yet sub'd (route to Job 5 before archiving).
  - **Pantone pass (CA SB 343)** — pull artwork Pantones; compare to approved gradient from `regulatory-manager/references/state-packaging-laws.md`. Outcome per component: pass, lighten Pantone, or remove recycling symbol. Fail surfaces to Operator with recommended path.
  - **Canada extended-allergens pass** — fires only for SKUs in scope for Canadian distribution (flagged at IL gate intake or marked on the SKU). Confirm the extended-allergens disclosure appears on the artwork per Pedrero's schedule. Hard deadline 2026-07-31 per Sephora Canada cutoff.
  - **Quebec French-language pass** — fires only for SKUs in scope for Quebec distribution. Confirm every inscription on the artwork appears in both English and French. Outcome: Pass, Partial (some inscriptions translated, some not — route to Perrine for translation completion), or Fail (English-only — route to PD designer for bilingual rework).
- *HITL:* Operator approves each pass outcome. Reg Lead approves any archive entry. Pedrero send (Job 2) fires if any pass surfaces a substantive question (e.g., Pantone borderline, Canada allergen interpretation, claim drift).

### 5. New-claim sign-off

Any new claim added to packaging or marketing copy stages to Pedrero before it ships, regardless of source (PD designer, marketing, founder).

- *Trigger:* "review this new claim on [SKU]", "is this claim defensible", "Pedrero sign-off needed on [claim]", "reformulation claim bridge on [SKU]", inbound from marketing/founder via outlook-asana-bridge or fireflies-asana-bridge, or auto-fired when a SKU enters reformulation status without prior-formula QIL parity (see §7.4 Rev.2 below)
- *Action:* Walk Procedure §7. Capture the claim text verbatim. Pull existing claim sub file for the SKU. Determine if the claim is already covered by existing evidence or needs new evidence. Four paths (Rev.2 adds the reformulation bridge):
  - **Covered by existing evidence** — draft the citation; stage to Pedrero for confirmation that existing evidence supports the new claim text.
  - **Needs new evidence** — pause; route the evidence-generation ask to PD (asana-pd-manager owns clinical, in-vitro, and ingredient-data evidence generation). Hold the claim until evidence lands.
  - **Not defensible** — flag to Operator with rationale; recommend reword or drop.
  - **Reformulation claim-bridge gate (Rev.2 §7.4)** — fires when a SKU reformulates (e.g., AMR transition) without QIL parity to the prior formula. Existing clinical-test claims (consumer-testing percentages, efficacy claims) cannot ride through reformulation by default — formula similarity has to be established. Two paths: (a) recover the original-formula QIL from the prior manufacturer (preferred — Operator pursues during any open order with the prior manufacturer; per 2026-05-12 Pedrero touchbase, the open eye-cream order is the legitimate access window); or (b) commission analytical comparison testing between old and new formulas (Pedrero confirms "dicey" — viable but not Pedrero's preference). If neither path lands, the claim retires or rewords. Eye Cream, Toner, and Power Oil are flagged at Rev.2 build as active reformulation candidates needing this gate.
- *HITL:* Operator approves the path. Reg Lead approves the Pedrero stage (Job 2). On the reformulation bridge path, Reg Lead also approves the QIL recovery ask to the prior manufacturer if pursued.

### 6. Retailer attestation response

For Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, and Credo questionnaires — drafted from the claim sub file, staged to Pedrero, then submitted by the Operator.

- *Trigger:* "stage the [retailer] attestation for [SKU]", "renew the Sephora Clean attestation on [SKU]", inbound retailer questionnaire via outlook-asana-bridge, scheduled renewal task firing off `Window End`
- *Action:* Walk Procedure §8. Pull the retailer's current questionnaire (templates in SharePoint regulatory folder; Asana attachments at v6.1 interim). For each question, pull the matching evidence from the SKU's claim sub file. Draft the response. Flag any question without sufficient evidence to Operator before staging to Pedrero. Set `Retailer / Agency` field to the retailer; set `Window End` to the retailer's submission deadline.
- *HITL:* Operator approves the draft. Reg Lead approves the Pedrero stage (Job 2). After Pedrero approval (Job 3), Reg Lead approves the actual retailer submission.

### 7. Closeout, renewal tracking, close-the-loop

Two paths:

**Closeout on terminal artifacts.** Once a Pedrero return is processed and the artifact lands in **Active / In-Effect** (or attestation in **Active / In-Effect** post-retailer-submission), closeout writes:
- Three-line summary on the Asana task: artifact type, version, Pedrero reference number / approval date
- Close-the-loop comment back to the originating system: Formula Tracker for IL approvals; the marketing or PD task for new-claim approvals; the printer-side task (post-v6.3 if exists) for label archives
- Move to **Active / In-Effect**; set `Window End` to next re-review or renewal date

**Renewal firing.** When `Window End` approaches (60-day, 30-day, 14-day reminders), the skill spawns a renewal task in **Renewal Window**:
- IL re-review windows fire if a SKU's formula reformulates or annually for portfolio-level reg review (default annual)
- Attestation renewals fire on the retailer's renewal cycle (most retailers: annual)
- Registration renewals (post-v6.3) fire on FDA / state cycles

- *Trigger:* operator-direct close ("close out the [SKU] IL approval"); auto-fire on Pedrero approval landing; scheduled `Window End` proximity
- *Action:* For closeout — three-line summary, close-the-loop comment, section move. For renewal — clone the originating task with `Window End` reset, link to prior cycle's task for history.
- *HITL:* Operator approves close. Reg Lead approves any renewal stage that requires a fresh Pedrero send.

## Asana surface

- *Project:* **SJS Regulatory Management** — Operations team, public to workspace. Created 2026-05-09 via Asana AI Builder at v6.1 build. Will roll up under regulatory-manager at v6.3.
  - Project GID: `1214660807386611`
  - Project URL: https://app.asana.com/1/1200120716421441/project/1214660807386611
  - Team (Operations) GID: `1200120716421443`
  - Portfolio (Operations Dashboard): `1208174221370391` — **manual add pending** (no MCP tool exposes portfolio-add at v6.1 build)

### Sections (cached 2026-05-09)

| Section | GID | Purpose |
|---|---|---|
| Inbound Staging | `1214661463988658` | new IL packets, new claims, attestation drafts, label artwork inbound — anything pre-Pedrero |
| In Pedrero Review | `1214661463988659` | sent to Pedrero, awaiting return |
| Returned — Action Required | `1214661463988660` | Pedrero kicked back; internal action needed |
| Active / In-Effect | `1214661463988661` | approved IL versions, active claim sub files, archived label artwork, submitted attestations |
| Renewal Window | `1214661463988662` | 60/30/14-day windows on attestations, IL re-review, registrations |
| Closed | `1214661463988663` | superseded, expired, terminal |


### Custom fields (cached 2026-05-09)

All fields exist on SJS Regulatory Management. Canonical GID + option-GID reference: `/Users/alvinbelt/Documents/Claude/Projects/Skill Builder/asana-field-gids.md`. The fields the skill uses:

- `Artifact Type` (single-select: IL Review, Claim Sub, Label Artwork, Retailer Attestation, Registration / Filing, Reg Flag (from Quality), Pedrero Liaison, Other) — what kind of work this task is
- `Linked SKU` (text — SKU code + name; blank for portfolio-level items)
- `Linked Batch` (text — PLM batch_code; only when artifact traces to a specific batch). Shared field with SJS Quality Management and SJS CAPA Log (same gid across all three projects).
- `Version / Reference` (text — IL version like `IL-CST-CRM-v3`, label version, attestation cycle year, registration filing ID). Carries the version stamp for filter/report use; the same stamp is also encoded in the task title.
- `Retailer / Agency` (single-select: Sephora, Ulta, Whole Foods, Credo, FDA, CA, NY, WA, OR, Other, N/A, Leaping Bunny) — Leaping Bunny added by Operator post-scope-lock for cruelty-free certification tracking
- `Window End` (date — renewal/re-review date)
- `Gate` (single-select: Open, Pending Operator, Pending QA Lead, Pending Regulatory Lead) — shared field with SJS Quality Management and SJS CAPA Log. The `Pending Regulatory Lead` option was added at v6.1 build for System C; System B skills continue to use only Open / Pending Operator / Pending QA Lead. This skill uses Pending Regulatory Lead for every Pedrero send and retailer submission gate; uses Pending QA Lead only when a label cross-check surfaces a quality-side issue.

*Title prefixes:* reserved for cross-skill staging where the destination skill or source skill is not yet live. In-flight state and HITL gates use Section + Gate, not title prefixes.
- **Inbound queue prefix (from asana-pd-manager):** `[IL Review Pending — claims-il-and-label-keeper]` — fires when Formula Tracker `Stage = Signed Approvals` flips `IL Status = Pending IL Review`.
- **Outbound staging to skills not yet built:** `[Reg Flag Pending — regulatory-manager]` for cross-skill issues that need the v6.3 dashboard view; pre-v6.3, these stage as comments on this skill's task.

## Numbering

- **IL Review:** one task per IL version per SKU, titled `IL Review — [SKU] — [IL-VERSION]` (e.g., `IL Review — Castaway Cream — IL-CST-CRM-v3`). IL version stamp in `Version / Reference` field.
- **Claim Sub:** one task per SKU bundling all sustained claims, titled `Claim Sub — [SKU]`. Per-claim evidence as subtasks.
- **Label Archive:** one task per artwork version per SKU per component type, titled `Label Archive — [SKU] — [COMPONENT or CARTON] — v[N]`.
- **Retailer Attestation:** one task per retailer per SKU per cycle, titled `Attestation — [RETAILER] — [SKU] — [YEAR]`.
- **New Claim Review:** one task per claim per SKU, titled `New Claim — [SKU] — "[claim text]"`.
- **Registration / Filing (v6.3 forward):** one task per filing per SKU per agency, titled `[AGENCY] — [SKU] — [FILING TYPE]`.

## Role map

The skill reads role-holders from `references/role-map.md`. Update protocol and rationale match the System B siblings. SKILL.md, references, Asana writes, and Gate field options all stay role-based; names live in the role-map.

## Calls and integrations

Pedrero traffic is mostly Outlook; Outlook bridges do heavy work. Asana is direct (this skill owns the SJS Regulatory Management surface).

**Reads via:**
- plm-assistant — SKU lookups, formula INCI lists, batch context, allergen data
- asana-pd-manager — Formula Tracker tasks for IL review intake, prior IL versions referenced from Formula Tracker history
- complaint-and-event-handler — when a complaint pattern surfaces a label-related issue, read the cross-flag context
- outlook-asana-bridge — inbound retailer questionnaires, Pedrero replies, marketing/founder claim asks
- fireflies-asana-bridge — inbound from PD or marketing meetings where a new claim or label question surfaces
- Asana — direct read of own tasks in SJS Regulatory Management
- SharePoint — IL/Claims/Label Procedure ratification target, IL/claim/label artifact archive (v6.3 forward)

**Writes via:**
- Asana — direct (custom fields, comments, section moves, new tasks for handoffs)
- asana-pd-manager Formula Tracker — sync-back comments + `IL Status` field flips on IL approval / IL return for reformulation
- outlook-asana-bridge — Outlook draft staging for every Pedrero send, every retailer submission (HITL on send; skill drafts, never sends autonomously)
- sweet-july-skin-brand — applied to any external-facing copy (retailer attestation responses, Pedrero correspondence formatting if needed)

**Never duplicates:**
- regulatory-manager (v6.3 — owns MoCRA registrations, state filings, retailer attestation cadence dashboard, Pedrero liaison cross-skill view, SharePoint regulatory folder pointer)
- adverse-event-and-recall-reporter (v6.2 — owns SAE filings and FDA recall agency reporting)
- regulatory-status-reporter (v6.4 — owns branded reporting)
- asana-pd-manager (owns formula development, pre-launch claim evidence generation, Formula Tracker)
- complaint-and-event-handler (owns customer complaint intake; cross-flags label-related issues here)
- plm-assistant (only writer to PLM)
- quality-manager (owns SOP catalog, cross-skill quality dashboard)

## Out of scope (v6.1)

- MoCRA registrations, state filings (CA Prop 65, NY/WA/OR), retailer attestation cadence dashboard — regulatory-manager v6.3
- SAE filing prep, FDA recall agency reporting — adverse-event-and-recall-reporter v6.2
- Branded regulatory status reports — regulatory-status-reporter v6.4
- Cross-system regulatory router queries — sjs-regulatory-system v6.5
- International regulatory work (EU CPNP, UK SCPN, Canada NMPA, China NMPA) — parked
- Pre-launch claim evidence generation (clinical, in-vitro, ingredient-data) — asana-pd-manager keeps
- Direct internal review of IL or label content — Pedrero does the substantive review externally
- Print-side QA, color management, dieline approval — Operations and the printer
- Standing up the SharePoint regulatory folder — Ops out-of-band; precondition for v6.3
- Direct PLM writes — plm-assistant only
- Vendor compliance docs at intake (COA, COC, COI, MSDS) — purchasing-manager keeps

## First-run setup

Project, sections, custom fields, and the Formula Tracker IL Status field were stood up via Asana AI Builder + Operator-managed UI on 2026-05-09 at v6.1 build. Gids cached in this SKILL.md and `asana-field-gids.md`. On first invocation:

1. **Confirm Asana state matches cached gids.** Re-pull the project via Asana MCP and confirm sections and custom fields match what's documented above. If anything has drifted, update SKILL.md and `asana-field-gids.md`.
2. **Confirm portfolio.** Confirm SJS Regulatory Management has been added to the Operations Dashboard portfolio (gid `1208174221370391`). Manual UI step — surface to Operator if missing. (Operator confirmed handling this manually at v6.1.)
3. **Confirm IL Status field on Formula Tracker.** Field gid `1214676606090922` on project `1213280384100264`. asana-pd-manager retrofit documented in its SKILL.md. If the field is missing from Formula Tracker, surface to Operator and pause — the IL gate intake (Job 1) cannot fire without the upstream hook.
4. **Confirm role-map.** Confirm `references/role-map.md` is current with the operator.
5. **Confirm SOP state.** `references/il-claims-label-procedure.md` is SKN-OPS-008 Rev.2, ratified 2026-05-12 in-place during the post-Pedrero update (Rev.1 effective 2026-05-09, superseded). `quality-manager/references/sop-catalog.md` lists SKN-OPS-008 at the current rev. Skill writes cite "SKN-OPS-008 Rev.2". The Rev.2 changes are: §3.2 adds the 19-state packaging-toxics certificate as a required IL packet element; §6 adds Pantone (CA SB 343), Canada extended-allergens, and Quebec French-language passes to label cross-check; §7.4 adds the reformulation claim-bridge gate.
6. **Confirm SharePoint interim plan.** Until v6.3 stands up `Sweet July/Regulatory`, IL packets, claim sub evidence, label files, and attestation drafts attach to Asana tasks directly per Procedure §10 retention rules.
7. **Default section housekeeping.** A default `Untitled section` (gid `1214661463988651`) exists from project creation. Surface to Operator at first interaction for delete or rename.

If any check fails, surface to the operator and stop — the skill does not modify project structure unilaterally.

## Trigger phrases

See `references/trigger-phrases.md` for the grouped trigger library.

## Reference files

- `references/il-claims-label-procedure.md` — IL/Claims/Label Procedure (working draft, pending SKN-OPS-008 ratification)
- `references/role-map.md` — current role-holders for Operator, Reg Lead, External Reg Partner, QA Lead, Voice of Customer
- `references/trigger-phrases.md` — grouped triggers by intent (IL gate, Pedrero send, return processing, label cross-check, new claim, attestation, closeout, status)

---

## Wiki context (runs before live queries)

Before running live Asana, Supabase, or PLM queries, read the relevant pages from `public.wiki_pages`. Wiki pages are synthesized regulatory briefings that compound as bridge skills process Pedrero emails, IL packets, attestation responses, and meeting traffic. Reading them first gives this skill institutional memory about each SKU's regulatory state and the Pedrero artifact trail.

### Which pages to read

- Named SKU → `'sku/' || public.wiki_slugify(coalesce(sku_code, product_name))`
- Pedrero (always, when work is regulatory in nature) → `'supplier/pedrero-regulatory'`

SKU pages carry regulatory status, IL review history, claim substantiation notes, and label versions. The Pedrero page carries the artifact trail, open items, and filing history.

### Read query

```sql
-- SKU page
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'sku/' || public.wiki_slugify('{sku_code_or_product_name}'));

-- Pedrero (always)
SELECT slug, title, content, source_count, updated_at
FROM public.wiki_lookup(p_slug => 'supplier/pedrero-regulatory');
```

### Freshness rule

| Condition | Behavior |
|---|---|
| `updated_at` within 7 days AND `source_count > 0` | Primary context. Reduce or skip redundant live queries. |
| `updated_at` > 7 days OR `source_count = 0` | Background only. Run live queries normally. |
| Page does not exist | Run live queries normally. Do not create wiki pages — that belongs to bridge skills. |

### Inject into generation

Prepend the wiki page content to this skill's context before generating its response. Treat the SKU page as the regulatory case file and the Pedrero page as the active correspondence trail.

### Write-back (stale pages only)

If a page is stale or `source_count = 0` and live queries produced genuine new regulatory signal not already in the wiki, update the page:

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
- Does not replace live Asana, Supabase, or PLM queries for current task state
