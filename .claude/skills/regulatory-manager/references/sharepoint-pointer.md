---
name: SharePoint regulatory folder pointer
description: Canonical SharePoint folder structure for System C regulatory artifacts. claims-il-and-label-keeper and adverse-event-and-recall-reporter migrate v6.1/v6.2 interim Asana attachments to SharePoint at v6.3 build. SharePoint MCP is read-only at v6.3; manual folder setup is a precondition.
last_updated: 2026-08-07 (re-check: folder still not stood up; OneDrive shadow archive noted; anchor-parallel path corrected)
---

# SharePoint regulatory folder pointer

Sweet July Skin's regulatory artifact archive lives at SharePoint root `Sweet July/Regulatory/`. v6.1 (claims-il-and-label-keeper) and v6.2 (adverse-event-and-recall-reporter) operated with interim Asana attachments because the SharePoint folder didn't exist at those build times. v6.3 stands up the pointer; v6.1/v6.2 attachments migrate to SharePoint per the schedule below.

## Folder structure

| Subfolder | Owner skill | Contents |
|---|---|---|
| `Sweet July/Regulatory/IL Versions/` | claims-il-and-label-keeper | IL packets sent to Pedrero; IL version history per SKU; allergen breakdowns |
| `Sweet July/Regulatory/Claim Substantiation/` | claims-il-and-label-keeper | Sustained claim sub evidence per SKU per claim (clinical, in-vitro, peer-reviewed citations, formal Pedrero opinions) |
| `Sweet July/Regulatory/Label Artwork Archive/` | claims-il-and-label-keeper | Approved label versions per SKU per artwork piece (cartons, components, inserts) |
| `Sweet July/Regulatory/Retailer Attestations/` | claims-il-and-label-keeper | Drafts, submitted responses, renewal evidence (Sephora Clean+Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo) |
| `Sweet July/Regulatory/Reportable Events/` | adverse-event-and-recall-reporter | SAE filings, recall reports, agency correspondence, 21 CFR 7 supporting docs |
| `Sweet July/Regulatory/Registrations/` | regulatory-manager | MoCRA listings, MoCRA facility registrations, state filings (CA Prop 65, CA Fragrance and Flavor Right to Know, CA Toxic-Free Cosmetics Act, NY/WA/OR), Leaping Bunny certification evidence |
| `Sweet July/Regulatory/Pedrero Correspondence/` | regulatory-manager | Engagement letters, scope discussions, general inquiries — non-filing-specific Pedrero work |

Anchor parallel (corrected 2026-08-07): the Quality SOP home was `Sweet July/Product Development/Quality Control & Assurance/` — nested two levels down, not at root, and unabbreviated (`Product Development`, never `PD`). So the original "mirrors that pattern at the same root level" reasoning was built on a wrong reading of the real tree. Note also that since 2026-08-04, canonical SOP *text* lives in the repo at `sops/` — SharePoint is no longer the SOP system of record either.

## Precondition status (as of v6.3 build)

**Folder existence: not yet stood up.** Out-of-band Ops task to create folder structure with appropriate permissions before v6.3 first invocation. v6.3 build flags this as a known precondition; if folder doesn't exist at first invocation, surface to Operator and pause migration step. Skill operates without SharePoint until then — Asana attachments stay on tasks per v6.1/v6.2 interim plan.

**Re-checked 2026-08-07 (three months later): still not stood up.** `Sweet July/Regulatory/` returns zero hits tenant-wide. Meanwhile the de facto regulatory artifact archive has formed in **Alvin's personal OneDrive** at `alvin_ac-brands_com/.../Sweet July Skin/Compliance & IL/` (21 items as of 2026-08-07: signed Vegelabs IL/Allergen/QQ, compliance summaries, TIL PDFs 18N280–283, IL tracker, packaging compliance ladder) — and 12 of the KDC lip-treatment TIL rows PLM logged on 2026-07-30 carry `file_url` values pointing into that personal OneDrive. Personal OneDrive is deprovisioned when its owner leaves; this is a single-person bus-factor filing location for the brand's regulatory artifacts. The decision this file has been waiting on since May — build this structure, or formally designate a different home and rewrite this pointer — is still open, and every month it stays open the OneDrive shadow archive grows.

## v6.1/v6.2 attachment migration

Once the SharePoint folder exists, regulatory-manager runs the migration walk per Job 7 (license audit) or operator-direct ("migrate v6.1 attachments"):

1. Read every Active / In-Effect task in SJS Regulatory Management (v6.1 IL versions, claim sub files, label archives, attestation records).
2. For each task, copy attachments to the matching SharePoint subfolder using the file naming convention from SKN-OPS-008 §5: `[SKU-CODE]_[ARTIFACT-TYPE]_[VERSION]_[YYYY-MM-DD].ext`.
3. Update the Asana task: replace attachment with a SharePoint URL pointer in the task description.
4. Repeat for SJS Reportable Events (v6.2) Closed and Submitted to Agency tasks per SKN-OPS-009 §7.
5. Operator approves migration in batches; Reg Lead approves any task description edit.

**HITL:** Operator approves migration kickoff and per-batch close. Reg Lead approves any Asana task edit during migration.

## SharePoint MCP status

Read-only at v6.3. Skill cannot write to SharePoint via MCP. File uploads are manual UI steps until SharePoint MCP gains write capability.

## Update protocol

1. Confirm change with Operator.
2. Update this file's structure table.
3. Update `last_updated`.
4. If a subfolder owner changes, update the owning sub-skill SKILL.md retention/storage section.
5. If the SharePoint root path changes (e.g., reorg to a different team site), update this file plus the v6.1/v6.2 migration walk.
