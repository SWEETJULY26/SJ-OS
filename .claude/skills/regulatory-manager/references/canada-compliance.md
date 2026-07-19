---
name: Canada compliance reference
description: Canada-specific cosmetic compliance scope for Sweet July Skin — Health Canada cosmetic notification requirement, extended-allergens labeling deadline 2026-07-31 with Sephora Canada acceptance cutoff, Quebec French-language requirement, Canadian-entity / responsible-person requirement, and current customs-hold history. Used by regulatory-manager registrations tracker and by claims-il-and-label-keeper label cross-check. Added 2026-05-12 post-Pedrero touchbase.
last_updated: 2026-05-12
---

# Canada compliance reference

Canada is SJS's first non-US market. Distribution has happened (~50 C2C shipments per year since 2023 launch) without the regulatory infrastructure to support it. The 2026-05-12 Pedrero touchbase surfaced the gap and a hard deadline.

## Current distribution state

- **Mode:** C2C direct-to-consumer shipments from the US.
- **Volume:** ~50 shipments per year since 2023 launch.
- **Notifications filed:** zero. SJS is not registered with Health Canada for any SKU.
- **Customs incidents:** three customs holds experienced. Released after manual paperwork from Operator; no penalty.

## Compliance gaps (open at 2026-05-12)

1. **No Health Canada cosmetic notification** for any SKU. Required for any volume — including C2C — per Health Canada Cosmetic Regulations.
2. **No Canadian entity or responsible person.** Regulations updated in the last year now require a Canadian RP to file notifications on behalf of foreign brands. Ecomundo or an alternative fills this role.
3. **No extended-allergens disclosure** on packaging. New rule takes effect 2026-07-31 (see below).
4. **No formal Quebec French-language compliance review** for Quebec-bound SKUs.
5. **No internal regulatory function** dedicated to Canada compliance. SJS does not have a Canada-side regulatory staff position; Pedrero plus RP partner cover.

## Hard deadline — 2026-07-31

### What's changing

Health Canada's extended-allergens labeling rule takes effect 2026-07-31. Cosmetics distributed in Canada after that date must disclose extended allergens on the label per the new schedule.

### Existing-market grace

Existing SKUs already in the Canadian market have until 2028 to comply. SJS does not have shelf presence in Canada — every shipment is C2C — so the grace doesn't help.

### Sephora Canada exception

Sephora Canada will not accept SKUs missing the extended-allergens disclosure after 2026-07-31, regardless of the 2028 grace. If SJS is planning Sephora Canada distribution post-2026-07-31, every SKU needs to ship with the new label by that date.

### Compliance path

1. Engage Ecomundo (or Pedrero-recommended alternative) as Canadian RP.
2. Pedrero (Amy) supplies the extended-allergens schedule and confirms which SJS ingredients map to which extended allergens.
3. Perrine handles French translations for Quebec dual-language compliance (already in her scope per role-map).
4. Alvin (Operator) supplies artwork files; claims-il-and-label-keeper §6 cross-checks the new artwork against approved IL plus the extended-allergens disclosure plus French translation.
5. Pedrero approves the new label per SKN-OPS-008 Rev.2 §4 Pedrero send.
6. Print run on approved label; old stock works through C2C until depleted; new stock ships compliant.

## Quebec French-language compliance

### What's required

Every inscription on the packaging (not just the mandatory regulated statements — every inscription) must appear in both English and French. Applies to SKUs distributed in Quebec.

### Implementation

- Perrine handles French translations (confirmed at 2026-05-12 touchbase; Perrine is fluent and works in product lead role with French / Quebec language fluency).
- Translation requirement applies to packaging text, not necessarily to marketing collateral that ships separately.
- Pedrero / Ecomundo confirms which inscriptions are mandatory vs which qualify as "inscriptions" requiring bilingual treatment.

### Cross-check workflow

claims-il-and-label-keeper §6 fires a Quebec bilingual check whenever an artwork file lands for a SKU bound for Canada. Match outcome:
- **Pass** — every inscription is bilingual; artwork archives.
- **Partial** — mandatory statements bilingual but other inscriptions not; flag to Operator for translation pass with Perrine.
- **Fail** — English only; route back to PD designer for bilingual rework.

## RP partner options for Canada

Per 2026-05-12 Pedrero touchbase:

| Partner | Status | Notes |
|---|---|---|
| Ecomundo | Existing agreement on annual fee model | Pedrero re-introducing for Canada Health Canada notifications. Lighter touch; no extensive RP review unless requested. |
| Alternative 1 | TBD | Pedrero introduces on request |
| Alternative 2 | TBD | Pedrero introduces on request |
| Beoria | Deprecated | Very thorough but demanding turnaround; replaced |

See `rp-partners.md` for canonical catalog.

## Asana task seed at first run

| Task | Section | Window End | Notes |
|---|---|---|---|
| `Canada — Extended Allergens — 2026` | Registrations — Renewal Window | 2026-07-31 | 60-day reminder fires 2026-06-01 |
| `Health Canada Notification — [SKU] — 2026` (one per active in-market SKU shipped to Canada since 2023) | Inbound Staging → In Pedrero Review when RP engaged | Per RP timeline | Backlog filing |
| `Quebec French-Language Compliance — Portfolio Sweep — 2026` | Registrations — Active (parent), subtasks per SKU | 2026-07-31 (Quebec / Sephora cutoff) | Cross-flags to claims-il-and-label-keeper §6 |
| `Canada Customs Hold Log — Rolling` | Pedrero Liaison | Continuous | Operator logs each customs incident; Pedrero / Ecomundo consult on resolution |

## International scope future state

UK and South Africa are tracked in `state-packaging-laws.md` and `rp-partners.md` as pending. Activation pattern mirrors Canada: Pedrero introduces RP partner, Operator confirms scope, regulatory-manager seeds a `[Country] — Cosmetic Notification — [YEAR]` task and corresponding label cross-check workflow.

## Update protocol

1. New customs hold → log in `Canada Customs Hold Log` task with date, SKU, resolution.
2. Health Canada rule change → Pedrero or Ecomundo flags; update this file + relevant Asana tasks.
3. New country activates → add country section to this file (or split into per-country reference); update `rp-partners.md`.
4. SJS launches Canadian retail (vs C2C) → revisit notification + entity requirements; entity may need to be formalized vs RP arrangement.
5. Update `last_updated`.
