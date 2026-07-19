---
name: Pedrero Regulatory contact catalog
description: Canonical Pedrero contact card. Source of truth for who to email on what, who's primary vs cc, and how Pedrero engagement works. claims-il-and-label-keeper, adverse-event-and-recall-reporter, and asana-pd-manager all reference this file.
last_updated: 2026-05-09
---

# Pedrero Regulatory contact catalog

Pedrero Regulatory is Sweet July Skin's external regulatory partner. All substantive regulatory review (IL approval, claim sign-off, attestation review, SAE classification, recall classification, MoCRA registration filing, state filing review, engagement-level scope work) flows through Pedrero. No internal SJS personnel substitute for Pedrero substantive review.

## Engagement model

Pedrero is consult-only. Pedrero contacts have no Asana access, no internal authority, and no privileged read of SJS PLM or Outlook. Every engagement flows through Outlook on the Operator's account, with Pedrero contacts as Cc on internal Asana tasks for record purposes (informational follower — they don't see the Asana surface).

## Contact roles

Contact identifiers live in Supabase wiki — `public.wiki_pages WHERE page_type='contact'` for amy-pedrero, heather-folkes, teona-bebia. Pedrero Regulatory's organization-level scope lives at `partner/pedrero-regulatory`. The four bridges load these at run time.

Engagement roles for System C sends:

- **Principal — Amy Pedrero.** Default `To` on every Pedrero send. Binding regulatory calls.
- **Secondary — Heather Folkes.** Cc on every send. Principal coverage when Amy is unavailable.
- **Secondary — Teona Bebia.** Cc on every send. Secondary coverage.

**On-call expectation for SAE and Class I recall:** same-day acknowledgment, full review within window per `adverse-event-and-recall-reporter/references/reportable-events-procedure.md` §5.5. If Amy doesn't respond within window, Heather covers; escalation per Procedure §6.

## Subject line conventions across System C

Subject prefix drives outlook-asana-bridge auto-routing back to the originating skill task.

| Filing type | Owner skill | Subject prefix |
|---|---|---|
| IL review | claims-il-and-label-keeper | `[IL Review — SKU-CODE]` |
| New claim sign-off | claims-il-and-label-keeper | `[New Claim Sign-Off — SKU-CODE]` |
| Retailer attestation | claims-il-and-label-keeper | `[Attestation Review — RETAILER — SKU-CODE]` |
| Label cross-check | claims-il-and-label-keeper | `[Label Cross-Check — SKU-CODE]` |
| MoCRA SAE filing | adverse-event-and-recall-reporter | `[SAE Filing — SKU-CODE]` |
| FDA recall | adverse-event-and-recall-reporter | `[FDA Recall — Class X — SKU-CODE]` |
| State AE | adverse-event-and-recall-reporter | `[State AE — STATE — SKU-CODE]` |
| MoCRA-specific recall | adverse-event-and-recall-reporter | `[MoCRA Recall — SKU-CODE]` |
| Registration filing review | regulatory-manager | `[Registration Review — REGISTRATION TYPE — SKU-CODE]` |
| Pedrero engagement letter renewal | regulatory-manager | `[Engagement Letter — Renewal — YEAR]` |
| Pedrero scope change | regulatory-manager | `[Engagement Scope Change — YYYY-MM-DD]` |
| Pedrero general inquiry | regulatory-manager | `[Pedrero Inquiry — TOPIC]` |

Always include `URGENT — by [date]` when statutory clock is tighter than 5 business days (typically applies to SAE Filing and FDA Recall — Class I).

## Engagement letter

The Pedrero engagement letter governs scope, retainer, response windows, and dispute resolution. Annual renewal expected; first renewal date confirmed at v6.3 first invocation with Operator. Engagement letter renewal is a regulatory-manager Job 5 task; lives in Pedrero Liaison section of SJS Regulatory Management.

## Update protocol

1. Confirm change with Operator and Reg Lead.
2. Update this file's table.
3. Update `last_updated`.
4. Cross-check `asana-pd-manager/SKILL.md` Pedrero Regulatory contact catalog (lines ~73-75); keep in sync.
5. If a contact email or principal/secondary structure changes, alert claims-il-and-label-keeper and adverse-event-and-recall-reporter — both skills draft Outlook sends from this catalog.
