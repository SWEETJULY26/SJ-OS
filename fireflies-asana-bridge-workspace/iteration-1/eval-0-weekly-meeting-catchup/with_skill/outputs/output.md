# Weekly Meeting Catch-Up — July 14–20, 2026

Source: live Fireflies MCP reads (`fireflies_get_transcripts` + `fireflies_fetch` on all 8 transcripts returned for the window). Read-only run — nothing written to Asana. Classified per `fireflies-asana-bridge` master classifier; primary-label priority is quality > regulatory > ops > pd > margin > intel > founder.

8 meetings this week:
1. [EXT] WITHIN x Sweet July QBR — 07/20, 64 min
2. SJ Ops Daily Stand Up — 07/20, 16 min
3. PJ/Sweet July Skin TB (KDC-One/HCT) — 07/20, 10 min
4. SJS Builder Session (Alvin + Nicole, org design) — 07/17, 50 min
5. Daily Ops Stand Up (Nicole + Ciarra) — 07/17, 46 min
6. ACE 15-Min Weekly Finance Review — 07/16, 12 min
7. SJ Skin Weekly TB (Alvin, Nicole, Perrine, Danielle, Soraya) — 07/15, 37 min
8. PJ/Sweet July Skin TB (KDC-One/HCT) — 07/14, 19 min

---

## 🚨 URGENT

- **Amazon appeal denied on the pineapple punch face mask** — Amazon flagged it as a skin-lightening product, pulled it pre-launch, and denied the first appeal; a heavy-metals test is now the condition for re-appeal. Amazon's own recommended labs quote $3–6K; Perrine and Madeleine are getting comparison quotes (expect under $1K). — Owner: Madeleine (quote), Perrine (comparison quotes) | *(SJ Skin Weekly TB, 07/15)*
  Labels: `regulatory` + `quality`
  → claims-il-and-label-keeper / regulatory-manager (Amazon compliance appeal), quality-lab-coordinator (heavy metals test result once in)
  → Cross-ref: same issue also flagged as a `margin` item below (don't use Amazon's lab — it's a markup)

- **Guava inventory is the tightest SKU in the portfolio — real stockout risk at Amazon/OC3PL.** Selling 600+ units/month, ~61 days of supply at Amazon, 900 units held in reserve for discovery sets, and a discrepancy where guava cartons showed up on Allure's destruction list (should not be there). Ciarra has been told to start de-kitting proactively and to confirm the destruction-list carton removal. — Owner: Ciarra | Due: ongoing, next FWS/OC3PL replenishment trigger | *(SJ Ops Daily Stand Up 07/20, Daily Ops Stand Up 07/17)*
  Labels: `ops`
  → inventory-manager / oc3pl-order-manager
  → Cross-ref: Amazon UPC change ticket (below), marketing-unit transfer (below)

- **Ulta is openly frustrated with KDC-One's inability to commit to a production date** for the lychee/pineapple punch launch — Perrine told Ulta's contact three weeks running "not next week." Raw material finally arrived and is in a 5-day test window; batching targeted week of 7/27. A slip here is a retailer-relationship risk, not just a timeline slip. — Owner: Alvin/Perrine (Ulta comms), Greg D. (KDC-One production commitment) | *(PJ/SJ Skin TB 07/14 and 07/20)*
  Labels: `pd` + `founder` (Ulta relationship, Ayesha briefing-worthy)
  → asana-pd-manager (Formula Tracker / production timeline task), ayesha-weekly-briefing (surface the retailer friction)

- **Photo shoot cancellation-penalty risk** — HCT/KDC-One owe field samples (Fig Sorel, Jamaican Cherry) for a scheduled photo shoot; Perrine flagged real financial penalties (studio, photographer) if the shoot slips. Alex D. committed to a same-day answer on 7/15 for sample timing. — Owner: Alex Delmarco (HCT) | Due: was "tomorrow" as of 7/14 call | *(PJ/SJ Skin TB 07/14)*
  Labels: `pd`
  → asana-pd-manager

---

## 🩺 QUALITY

- Eye cream barcode mislabeling caused an Amazon listing issue — root cause is the pack-list template defaulting to the wrong barcode source (should say "use manufacturer barcode," not "use Amazon barcode," since the eye cream already carries a printed barcode). Nicole is briefing OC3PL and checking the template to prevent recurrence. — Owner: Nicole | *(Daily Ops Stand Up, 07/17)*
  → quality-lab-coordinator (root-cause / preventive fix) or capa-coordinator if this warrants a formal NCR
  → Cross-ref: `ops` (oc3pl-order-manager, since this is also a fulfillment process fix)

- Heavy metals test (pineapple punch face mask, Amazon compliance) — see URGENT above; also a quality data point once results land (needs filing/documentation regardless of appeal outcome).
  → quality-lab-coordinator

- Stability waiver review ongoing for lychee/pineapple punch lip treatment — Perrine assesses risk as low (same base formula, differs only by flavor/tint) but flagged that documentation still needs to be formalized. — Owner: Alvin (track), Perrine (risk assessment) | *(SJ Skin Weekly TB, 07/15)*
  → batch-lifecycle-tracker / quality-lab-coordinator
  → Cross-ref: `pd`, `regulatory` (IL/claim timing)

---

## 📜 REGULATORY

- Amazon face-mask appeal / heavy metals test — see URGENT.
  → claims-il-and-label-keeper, regulatory-manager

- Cleansing oil — Washington state lead-in-cosmetics risk flagged by regulatory; Perrine is sourcing comparable heavy-metals test quotes (same vein as the face mask) via Veggie Labs and a second vendor. — Owner: Perrine | *(SJ Skin Weekly TB, 07/15)*
  → regulatory-manager
  → Cross-ref: `margin` (test cost comparison), `plm`

- Toner IL — back from regulatory; Padrero review in progress. Question raised (and answered): hold the toner unit-carton production run until Padrero clears it, rather than proceed at risk — Perrine's guidance was to wait if timeline allows. — Owner: Alvin | *(SJ Skin Weekly TB, 07/15)*
  → claims-il-and-label-keeper

- Padrero priority queue for the rest of the year: toner (next), then the three phase-one lip SKUs (Fig, Cherry, Sorrel Tea) — Alvin to confirm this sequencing with regulatory. — Owner: Alvin | *(SJ Skin Weekly TB, 07/15)*
  → claims-il-and-label-keeper

- ILs for approved phase-one SKUs received from Padrero/Caroline; need to be worked into copy docs — some newer SKUs (Coffee Fix lip treatment, etc.) may not have official copy docs yet. — Owner: Alvin + Nicole (process discussion) | *(SJ Skin Weekly TB, 07/15)*
  → claims-il-and-label-keeper, asana-plm-bridge

---

## 📌 OPS / PD ACTION ITEMS

**Ops — inventory / fulfillment**
- Ciarra: instruct FWS to begin de-kitting guava sets proactively; confirm carton availability at Allure. | *(SJ Ops Daily Stand Up 07/20)*
- Ciarra: follow up on removal of guava cartons from the Allure destruction list; confirm completion. | *(SJ Ops Daily Stand Up 07/20)*
- Ciarra: execute the Amazon UPC change via Seller Central support ticket for the headband SKU. | *(SJ Ops Daily Stand Up 07/20)*
- Nicole: trigger/confirm Amazon go-live status for face masks and add the transfer task as an Asana dependency (blocking, not blocked-by). | *(SJ Ops Daily Stand Up 07/20)*
- Nicole: transfer marketing-use units (master cartons of 5-packs, plus single packs) from OC3PL to the retail store once the full face-mask shipment arrives; full inventory/replenishment review requested by Alvin. | *(SJ Ops Daily Stand Up 07/20)*
- Alvin: add Terry headband SKU to the inventory dashboard (done, per transcript — confirm in Asana). | *(SJ Ops Daily Stand Up 07/20)*
- Ciarra/Nicole: zero out negative toner inventory (-10 at Oakland) in Shopify/Cloud. | *(Daily Ops Stand Up 07/17)*
- Nicole: prioritize 150 headband units to Amazon FBA; verify UPC with OC3PL first. | *(Daily Ops Stand Up 07/17)*
- Nicole: track summer scarves delivery at OC3PL, expedite inventory upload given Ayesha's Today Show appearance driving possible demand spike. | *(Daily Ops Stand Up 07/17, WITHIN QBR 07/20)*
- Nicole/Ciarra: air-ship half the guava order (5K air / 5K sea) to hit the August timeline; confirm cartons at Allure. | *(Daily Ops Stand Up 07/17, PJ/SJ Skin TB 07/20)*
- Ciarra: hand off ocean-shipment receiving (face masks, ETA 7/22 LA) to Nicole with Gogo Customs as freight forwarder — full handover thread now includes Nicole/Alvin. | *(Daily Ops Stand Up 07/17)*
- Nicole: decide on tinted-SKU kitting approach (10K units — individually shipped vs. KDC-kitted with possible MOQ) once brainstorm with Katie/Soraya happens. | *(Daily Ops Stand Up 07/17)*

**PD — supplier / production**
- Alex Delmarco (HCT): confirm guava tube production schedule to match essential-SKU readiness (8/14); report back on FNA-instruction requirement for lychee/other flavors post pineapple-punch pilot. | *(PJ/SJ Skin TB 07/20, 07/14)*
- Greg D. Vecchia / JD Ayden (KDC-One): real-time updates on pineapple punch raw-material testing; batching targeted week of 7/27; include Trina Churchill (new client-services contact) on all future supply-planning threads. | *(PJ/SJ Skin TB 07/20)*
- Alvin: schedule air shipment for guava following the lychee air-shipment cadence. | *(PJ/SJ Skin TB 07/20)*
- Alvin: continue reconciling KDC-One/testing invoices; share status with Perrine. | *(SJ Skin Weekly TB 07/15)*
- Alvin: courier signed tube artwork to HCT; artwork still open for Phase 2 tinted SKUs and Coffee Fix (lip + eye cream) pending Danielle/Ayesha review. | *(SJ Skin Weekly TB 07/15)*
- Nicole: sign off on glossy drawdown samples (premium vs. standard) once Katie submits them. | *(SJ Skin Weekly TB 07/15)*
- Alvin: flag vitamin C percentage display (secondary packaging) for a Danielle/Soraya decision — conversation has stalled since Soraya's PTO. | *(SJ Skin Weekly TB 07/15)*
- Alvin: prepare Resurrection Bomb packaging pilot decision pending Capsum sample arrival (ordered from China, no domestic backup exists if rejected). | *(SJ Skin Weekly TB 07/15)*
- Alvin: share the Asana visual board directly on KDC-One/HCT supplier calls going forward to hold the team accountable on dates — raised specifically after a 4–5 month miscommunication on guava-tube priority. | *(PJ/SJ Skin TB 07/14)*

---

## 💬 DECISIONS (log as comments / decisions log)

- **Org design decision:** Eliminate Ciarra's Ops Coordinator role by end of August (not a performance-out — a role redesign) and replace it with two new specialist roles — an Operations Specialist and a Product Development Project Manager Specialist — both reporting to Nicole. Alvin and Nicole will divide her current work in the interim (Alvin: inventory/logistics; Nicole: order management/OC3PL). *(SJS Builder Session, 07/17)* — **Recommend logging to `decisions/log.md`** given this is a quarter-priority hiring decision (ties directly to `context/priorities.md`).
- **Org design decision:** Push to move Ivy's reporting line from Danielle to Soraya (people-management only, not creative direction) — Danielle has been hesitant; Alvin is making the case. *(SJS Builder Session, 07/17)* — candidate for decisions log.
- Builder sessions (Alvin/Nicole recurring 1:1) moved earlier in the day going forward, to avoid afternoon drop-off in effectiveness. *(SJS Builder Session, 07/17)*
- Toner unit-carton production: hold for Padrero regulatory review rather than proceed at risk (per Perrine's recommendation). *(SJ Skin Weekly TB, 07/15)*
- Copy doc "distributed by" line: change from AC Brands to Sweet July across SKU copy docs (soursop caught; check the rest). *(SJ Skin Weekly TB, 07/15)*
- Resurrection Bomb launch: confirmed for fall 2027 (last launch of the year), not summer as previously discussed. *(SJ Skin Weekly TB, 07/15)*

---

## 📊 STATUS SIGNALS

- **Guava (Amazon + OC3PL + discovery-set reserve)** — Affects: Inventory / OC3PL Order Management | Suggested RAG: **Amber** — tight but managed with an active mitigation plan (air shipment, de-kitting, FWS replenishment trigger at 500 units).
- **Toner** — Affects: Inventory | Suggested RAG: **Amber** — low stock, October receipt date, may need a stability-testing waiver to hit that date; secondary packaging held for regulatory.
- **Lychee/pineapple punch production (Ulta-facing)** — Affects: PD / Retail relationship | Suggested RAG: **Red** — Ulta has been told "not next week" three weeks running; raw material now in-house and testing, but no committed production date yet.
- **Pineapple punch face mask (Amazon)** — Affects: Regulatory / Quality | Suggested RAG: **Red** — appeal denied once, heavy-metals test outstanding, product off Amazon since before launch.
- **Ulta partnership overall** — Affects: Founder / Retail | Suggested RAG: **Amber** — one month in, progress slower than expected per finance review; being monitored closely.
- **Eye cream** — Affects: Quality / OC3PL | Suggested RAG: **Green-trending** — root cause identified (barcode template), fix in progress, restock expected within a couple weeks from Allure.

---

## 💰 MARGIN

- Heavy metals test sourcing (face mask + cleansing oil) — Amazon's recommended labs quote $3–6K; Perrine getting comparable quotes from Veggie Labs and a second vendor, expects under $1K. Explicitly framed as "Amazon money grab." | *(SJ Skin Weekly TB, 07/15)*
  → margin-pressure-test (vendor cost comparison), cross-ref `regulatory`/`quality` above
- KDC-One testing invoice reconciliation in progress — Alvin flagged discrepancies between initial and balance invoices; sharing with Perrine to review before payment. | *(SJ Skin Weekly TB, 07/15)*
  → margin-pressure-test / purchasing-manager
- Pacific Automation equipment-possession dispute still unresolved (they claim SC30 has equipment SC30 says it doesn't have) — ongoing back-and-forth, no resolution yet. | *(ACE Finance Review, 07/16)*
  → purchasing-manager / vendor dispute, no direct Asana queue named in bridge contract — flag to Alvin for direct follow-up.

---

## 🔭 INTEL

- Q2 performance (WITHIN QBR): $105K Q2 revenue, +7% YoY despite product-launch delays; paid media +17% revenue growth (TikTok/Meta strong); Amazon +91% sales during Prime Week; organic/SEO +12% YoY. Q3 priorities: omnichannel balance across D2C/Ulta/Amazon, Pineapple Punch launch as the growth driver.
  → sjs-retail-intel (Amazon/Ulta channel data), sjs-comp-intel (n/a this week — no competitor mentions)
- Ayesha's Today Show appearance (Sweet July, Ulta, face mask mentions, "What's in My Bag" segment) — driving potential demand spike on summer scarves; Soraya tracking boosting/organic-content opportunities.
  → sjs-retail-intel, ayesha-weekly-briefing

---

## 👤 FOUNDER BRIEFING

- Ulta production-timeline frustration (see URGENT/Red status) — founder-briefing-worthy given retailer relationship risk.
- Today Show appearance and "What's in My Bag" segment performance — good-news item for the briefing.
- Q2 QBR results ($105K, +7% YoY, Amazon +91% Prime Week) — standard founder rollup material.
- Canada market entry — confirmed on hold; Ayesha reassessed and decided not to pursue the Top Shelf Canada deal for now. *(ACE Finance Review, 07/16)*
- Three-year PD plan — Ayesha, Danielle, and the skin consultant did an initial "pie in the sky" pass; Alvin/Dan circling back to make it realistic ahead of the budget meeting. *(ACE Finance Review, 07/16)*
- Org redesign (Ciarra transition, two new specialist roles) — worth a founder-facing FYI even though it's an operator-level decision, since it ties to this quarter's hiring priority.

---

## ⚙️ PLM FLAGS (cross-flag to `outlook-plm-bridge` / `asana-plm-bridge`)

- Pineapple punch raw material now fully received and in testing (final outstanding raw material arrived) — batching targeted week of 7/27. Update formula/batch record status.
- Lychee, guava, essential production dates confirmed: lychee end of July, guava 8/7, essential 8/14 — update PLM production schedule fields.
- Trina Churchill (KDC-One) now the client-services/replenishment contact of record — update vendor contact record.
- Toner IL cleared regulatory intake, in Padrero review — update PLM regulatory-status field.
- Soursop copy doc updated with new IO section; "distributed by" corrected to Sweet July — update PLM copy/label record.
- Capsum packaging samples for Resurrection Bomb in transit from China, no backup vendor exists — flag as a supply-risk note on the PLM record.

---

## Which of these should I push?

This was a read-only catch-up per your request — nothing has been written to Asana. Say "all," list specific items by section/bullet, or "skip." Given the safety/compliance priority order, I'd suggest starting with the two 🚨 URGENT regulatory/quality items (Amazon face-mask appeal + guava stockout risk) if you want to triage before doing a full push.
