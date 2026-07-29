# Wiki layer audit — 2026-07-29

Audit of Supabase `public.wiki_pages` (133 pages) against the SJ-OS repo and `decisions/log.md`. Ran alongside the `asana_task_contract.md` build, because the contract's Phase 0 wiki pre-check depends on this layer being trustworthy.

**Headline:** structural integrity is clean. Freshness is not — the bridges' Job 0 write-back has not fired since 2026-05-26, so 123 of 133 pages are untouched seed data.

---

## Clean

- **Foreign-key linkage: perfect.** Every `sku` page resolves to a real `products` row, every `supplier` page to a real `vendors` row. No dangling `product_id` / `vendor_id`, no page missing its link.
- **SOP wiki coverage: 1:1** with `sop_documents` after this audit's fix — 14 procedures and forms, 14 pages, no orphans either direction.
- **Slug hygiene: 1 mismatch in 133**, now fixed.
- **Product coverage:** only 2 of 42 products lack a wiki page, both bundles (`SET-PPHD-001` Pineapple Punch Hydration Duo, `SJS-STARTER-SET` Vacation Skin Starter Set). Low priority — bundles carry no independent formulation or vendor story.

## Fixed in this pass

**1. `supplier/kdc-one` slug broke the lookup rule.** The vendor is `KDC/One (Port Jervis)`, so the documented rule (`'supplier/' || wiki_slugify(vendors.name)`) computes `supplier/kdc-one-port-jervis`. The page was at `supplier/kdc-one`. Any skill resolving the slug would have missed it, and — per the slug rule's own instruction that a `wiki_lookup` miss means the page genuinely doesn't exist — created a **duplicate page for the highest-volume supplier**, splitting the PO 100342 / 100344 ledger across two pages. Renamed to what the rule computes.

**2. SKN-OPS-005 existed only in the repo.** The NCR Procedure was ratified 2026-05-09 and drives capa-coordinator's entire NCR intake (severity bands, escalation criteria, effectiveness windows), with a full procedure file at `capa-coordinator/references/ncr-procedure.md`. It had **no `sop_documents` row and no wiki page**. For eleven weeks the runtime SOP catalog could not answer "current revision of SKN-OPS-005" while every NCR cited it. Row and page created.

**3. `next_review_date` was NULL on all 13 SOP rows.** quality-manager Job 1 fires `[SOP Annual Review — SKN-OPS-NNN]` tasks off that column, so the annual-review sweep had nothing to fire on. Backfilled from the repo catalog. **Consequence now visible: SKN-OPS-001 through 004 and all five SKN-F-OPS forms are 29 days overdue for annual review** (due 2026-06-30). Nine review tasks should fire.

**4. SKN-OPS-008 revision drift.** Repo catalog said Rev 1.0 / eff 2026-05-09. PLM says Rev 2.0 / eff 2026-05-12, and claims-il-and-label-keeper's own description says "Walks SKN-OPS-008 Rev.2." Two of three surfaces agreed; the catalog was the stale one. Corrected there.

**5. Four skills described ratified SOPs as working drafts.** `adverse-event-and-recall-reporter` (009), `claims-il-and-label-keeper` (008), `quality-lab-coordinator` (006), and `capa-coordinator` (005) all still said "pending ratification." capa-coordinator contradicted itself — its design-principles section documents the 2026-05-09 ratification while its description called the procedure pending. All corrected.

**6. `sop-catalog.md` contradicted itself.** Its table listed SKN-OPS-005 as Ratified; its example-queries section answered "what SOPs are pending ratification" with "SKN-OPS-005, pending QA Lead review." Rewritten.

**7. The `pending-ratification://` sentinel is misleading.** Four ratified SOPs (005, 006, 007, 009) carry `sharepoint_url = 'pending-ratification://skn-ops-NNN'`. It means "SharePoint master not yet filed," not "SOP not ratified" — and it's the likely source of finding 5's drift. Documented in the catalog rather than renamed, since renaming the scheme touches four rows and a convention.

**8. Five contacts had no email.** The bridges resolve people by sender address and domain, so a contact page with `Email: —` cannot be matched from an inbound email at all. Backfilled Erin, Ivy, Kate, Soraya, and Ayesha from verified Asana workspace accounts. **Still missing** (external, addresses not on hand): Danilo Megia (FWS), David Greco (HCT), Terrie (OC3PL).

**9. `plm/asana` was a rejected `last_source` value.** `wiki_pages_last_source_check` predated asana-plm-bridge Flow 5 and allowed only `email/outlook`, `meeting/fireflies`, `plm/outlook`, `manual`, `seed`. All five documented `plm/asana` writes would have failed with a 23514 violation. Migration `add_plm_asana_to_wiki_pages_last_source_check` added it.

## Open — needs a decision

**Job 0 has not written since 2026-05-26.** This is the finding that matters most.

`audit_logs` for `entity_type = 'wiki_pages'`: 186 writes in 2026-05, then nothing until this audit. Only 9 pages have ever been bridge-written. All 40 `sku` pages still carry the `(not yet populated)` placeholder in every section. 42 of 44 contacts, 16 of 21 suppliers, and all 15 partner pages and 13 SOP pages are untouched seed.

All four bridges document Job 0 as firing after confirmed Asana writes, and `fireflies-asana-bridge` states it runs daily. Eval runs on 2026-07-20 and 2026-07-21 processed real emails and meetings. No wiki write landed from any of it.

The innocent explanation is that Job 0's trigger is *confirmed* Asana writes, and eval runs stop at the confirmation gate by design — so evals legitimately don't fire it. That doesn't cover a two-month gap in real daily operation. Either very few Asana writes were confirmed in that window, or Job 0 is being skipped after the writes that were. Worth determining which before leaning on this layer.

Two things follow from it. The recognition lexicon the bridges load at run time is mostly seed data, so entity recognition is weaker than the design assumes. And the new contract's Phase 0 wiki pre-check will find almost nothing until Job 0 actually runs — it's written as an accelerator, not the dedupe mechanism, so this doesn't break it, but it won't help yet either.

**`Bridge-and-System-Audit-2026-05-26.md` is a dangling reference.** Cited from `sjs-master/SKILL.md`, `asana-pd-manager/SKILL.md`, and `bridge_queue_contract.md` as the authority for the queue-contract and run-time-entity-discovery decisions. The file exists nowhere — most likely lost in the 2026-07-19 consolidation that moved cross-system files into `references/architecture/`. The decisions it drove are still in force and documented in the files that cite it, so nothing is broken, but three files point at something unreadable.

## Decision-log cross-check

One decision had never been written up: the 2026-07-17 retirement of the Ops Coordinator role in favour of two specialist hires. A Fireflies eval run captured it from the SJS Builder Session and explicitly flagged it for the log at the time. Logged 2026-07-29, along with the Ciarra offboarding cleanup it implied.

Otherwise the log tracks: the 2026-04-29 shared-architecture decision and the 2026-07-19 SJ-OS consolidation are both reflected in the repo's current shape.

## Rule going forward

Three surfaces have to agree on any SOP: `sop-catalog.md` (repo), `sop_documents` (PLM), and the `sop/` wiki page. When they disagree, PLM is runtime truth — fix the repo file, then confirm the wiki page exists. Findings 2, 3, 4, and 6 were all the same failure: a change landing on one surface and not the other two.
