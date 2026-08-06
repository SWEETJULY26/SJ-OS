"""What each activity actually is, plus a worked example.

Keyed by the exact activity text in raci_rows.py. Two fields per entry:

  what    - one or two sentences defining the activity in AC Brands terms,
            naming the system or procedure it runs through.
  example - a concrete instance, using real SKUs, vendors, partners and SOP
            numbers from the repo rather than invented ones.

The RACI says who. This says what. A row with no entry here still shows its
assignment note and source in the drawer, marked as having no breakdown yet.
"""

INFO = {

# ---------------------------------------------------------------- Product Development
"Formula stage-gate progression through the PD Formula Tracker": dict(
    what="Moving a formula from one stage to the next in the PD Formula Tracker: brief, bench, submission, revision, approved. Each move is a decision that the formula is good enough to leave its current stage, and it is logged rather than assumed.",
    example="Milinyc returns Revision 3 of a lip treatment. Perrine reads the bench notes and confirms the texture and payoff are right, so the SKU moves from Revision to Signed Approvals. The Operator confirms the move; a reversal back to Revision gets a stronger intent check because it usually means something failed.",
),
"Compatibility, stability, RIPT and PET decisions (pre-launch)": dict(
    what="The four pre-launch safety and durability tests, and the call on whether results pass. Compatibility is formula against its packaging, stability is the formula over time and temperature, RIPT is a human skin-irritation panel, PET is preservative efficacy.",
    example="A cream passes 12-week accelerated stability but the PET comes back marginal at week 8. Perrine decides whether the preservative system needs reworking or whether the result is within noise. If it reworks, the formula drops back a stage and the launch date moves.",
),
"Packaging development with fillers and component vendors": dict(
    what="Getting the physical package right with the people who make and fill it: tooling, dielines, decoration, closures, fill compatibility. Runs with HCT, Element, Impress and the contract filler.",
    example="A pump on a moisturizer keeps failing in the field. Erin decides whether to re-tool the pump or change supplier, Jan runs the vendor conversation and sample rounds, and Perrine is consulted because the pump touches the formula.",
),
"Direction-changing PD decisions (launch scope, supplier change, kill calls)": dict(
    what="The decisions that change what a product is or whether it ships at all. Moving a launch date, cutting a shade or size, switching manufacturer, or killing a project outright.",
    example="A SKU is running late and the choice is a reduced launch (fewer sizes, same date) or a full launch a quarter later. Danielle makes that call. The AMR transition was the same shape of decision, and it triggered the reformulation claim bridge downstream.",
),
"Founder approval on brand-line moves": dict(
    what="Decisions that change what the Sweet July Skin brand line is, as distinct from decisions about a single product. New category entry, a line extension, or anything that repositions the brand.",
    example="Extending beyond skincare and lip into a new category. That is Ayesha's call rather than a PD or Ops decision, because it changes what the brand stands for and her name is on it.",
),
"PD signal intake from meetings and supplier email, plus PD status reporting": dict(
    what="Catching PD commitments wherever they were made and turning them into tracked tasks. Fireflies transcripts and Outlook threads feed the Asana PD queues through the bridges, and the reverse direction publishes status back out.",
    example="A KDC-One call ends with three commitments and a sample due date. The Fireflies bridge posts them to the PD queue with owners rather than leaving them in a transcript nobody reopens.",
),
"Reformulation triggered by a Quality or Regulatory reverse-handoff": dict(
    what="Reformulating because Quality or Regulatory sent the product back, not because PD chose to. A repeat CAPA, a failed stability result, or a claim that no longer holds pushes the SKU back into development.",
    example="Complaint trending shows the same texture issue across three batches, the CAPA root cause lands on the formula, and the SKU returns to bench. The claim bridge then decides whether the old clinical claims survive the new formula.",
),
"Document control: specifications, dielines, artwork versions, BOMs, landed-cost integrity": dict(
    what="Keeping one current version of every product document and making sure the numbers behind it still add up. Specs, dielines, artwork versions, bills of materials, and the landed cost that the margin work depends on.",
    example="Artwork goes to Revision 4 but the BOM still points at the Revision 2 dieline. Document control catches that before the printer does, which is the difference between a version note and a scrapped print run.",
),

# ---------------------------------------------------------------- Operations & Supply Chain
"Vendor master data, onboarding (NDA + W9 gate), sourcing and performance scorecards": dict(
    what="Everything about a vendor as a record rather than a relationship: getting them set up correctly, holding the NDA and W9 gate before work starts, running RFQs, and scoring how they actually perform.",
    example="A new component supplier cannot receive a purchase order until the NDA and W9 are both on file. The gate exists so a vendor never starts work under an unsigned arrangement, and their on-time and defect history then feeds the scorecard that decides whether they get the next award.",
),
"Purchase order lifecycle: placement, acknowledgement variance, close and discrepancy": dict(
    what="A purchase order from issue to close, including the moments where reality diverges from the order. Acknowledgement variance is when the vendor confirms different quantities, prices or dates than you asked for.",
    example="You order 10,000 caps at a set price for a set week. The acknowledgement comes back at a higher unit price and two weeks later. That variance gets surfaced and resolved rather than discovered at receipt or on the invoice.",
),
"Goods receipt on PD-linked purchase orders": dict(
    what="Receiving material that a live product programme is waiting on, and recording it against the right purchase order and batch. Distinct from routine receiving because a PD-linked receipt usually unblocks a stage gate.",
    example="Components arrive for a launch build. The receipt records quantity and batch, links to the PO, and tells the PD side the fill can be scheduled. A short shipment here moves a launch date.",
),
"Three-way reconciliation across PLM, Shopify and Logiwa": dict(
    what="Checking that the three systems that each think they know your inventory actually agree: PLM as the product record, Shopify as what is sellable, Logiwa as what the warehouse physically holds.",
    example="Logiwa shows 400 units, Shopify is selling against 520, PLM says 480. Until that is reconciled you are either overselling into a backorder or sitting on stock the store will not offer.",
),
"Vendor invoice classification and cost capture (five HITL gates)": dict(
    what="Reading each vendor invoice, deciding what kind of cost it is, and writing it to the record that margin and close depend on. Five human approval gates because a misclassified cost is invisible once it lands.",
    example="A Pedrero invoice arrives through Ramp. It has to be classified as regulatory rather than general professional services, or the regulatory spend rollup understates and the quarterly cost picture is wrong.",
),
"Inventory position keeping, batch creation on receipt and the location ledger": dict(
    what="Knowing what you have, where it is and which batch it belongs to. Batches are created at receipt, which is what makes later recall, expiry and quality tracing possible at all.",
    example="A finished-goods delivery is received as a numbered batch with its own expiry. Six months later a complaint names that batch, and because the batch exists in the ledger you can find every unit that shipped from it.",
),
"Adjustments, write-offs and return dispositions": dict(
    what="Correcting the inventory record when physical reality differs, and deciding what happens to units that come back. A return is either restockable, damaged or destroyed, and someone has to say which.",
    example="A customer return arrives with a used pump. It gets dispositioned as unsellable and written off rather than quietly returned to sellable stock, which is both a quality decision and an inventory one.",
),
"S&OP: forecast, inventory targets and buy recommendations": dict(
    what="Sales and operations planning: what you expect to sell, how much cover you want to hold, and therefore what to buy and when. The upstream decision that everything else in supply chain executes.",
    example="A promo is coming and lead time from the filler is long. S&OP decides the buy now, because deciding it later means either an out-of-stock during the promo or paying for air freight.",
),
"Inbound freight, customs, duty and carrier claims": dict(
    what="Moving goods into the business and handling what goes wrong in transit. Customs clearance, duty and HTS classification, broker holds, and claims when a carrier loses or damages a shipment.",
    example="A component shipment sits on a broker hold over a classification question. Every day it sits pushes the production slot, so the hold gets worked rather than waited out.",
),
"Daily DTC order operations and the Logiwa report parse": dict(
    what="The daily rhythm of direct-to-consumer fulfilment: today's orders shipped, today's exceptions, parsed out of the Logiwa report into the OC3PL Asana project.",
    example="The daily parse shows six orders unshipped past their window and one address bounce. Those become tracked exceptions with owners instead of a number nobody follows up on.",
),
"Pre-ship out-of-stock holds from the shortage sheet": dict(
    what="Catching orders that cannot ship because a SKU is short, before they are picked rather than after. Driven by the OC3PL shortage sheet read daily at order level.",
    example="An order contains a SKU that went short overnight. Holding it pre-ship means one customer conversation about a delay, instead of a partial shipment, a refund and a second outbound.",
),
"Retailer ASN / EDI 856 and routing-guide compliance (Ulta DC, Amazon Vendor)": dict(
    what="Shipping into a retailer's distribution centre exactly the way their routing guide demands. The ASN, EDI 856, is the electronic advance notice; the routing guide covers pallet build, labels, appointments and paperwork.",
    example="An Ulta DC delivery goes out with a pallet label in the wrong position. The DC charges back the non-compliance, which comes straight off the margin on that shipment. Compliance is cheaper than the chargeback.",
),
"Production scheduling with manufacturing partners": dict(
    what="Booking and holding production slots with the fillers and manufacturers, and sequencing what gets made when. Runs against KDC-One, Vegelabs, Allure Labs and AMR.",
    example="Two SKUs need the same line in the same window and one has a retailer commitment behind it. Scheduling decides which runs first, and the other SKU's launch plan moves accordingly.",
),

# ---------------------------------------------------------------- Quality
"Customer complaint intake, classification and first response": dict(
    what="Every end-customer quality signal comes in through one door, gets classified, and gets answered. Classification decides whether it is a routine complaint, a potential adverse event or a recall trigger, which changes what happens next and how fast.",
    example="A customer reports stinging after use. Classified as a routine complaint it is logged and answered. Classified as a possible adverse reaction it starts the SAE triage clock instead. Getting that call right at intake is the whole point of the single door.",
),
"Complaint trend analysis by SKU and batch": dict(
    what="Reading complaints as a pattern rather than as individual tickets. Rate per SKU, clustering by batch, and whether a rate is moving.",
    example="Three separate pump complaints look like bad luck. Grouped by batch they turn out to be the same lot, which turns a customer-service matter into a packaging decision and possibly a batch hold.",
),
"NCR and CAPA lifecycle, intake through close (SKN-OPS-001)": dict(
    what="Non-conformance and corrective action, run end to end per SKN-OPS-001. A non-conformance is the thing that went wrong; the CAPA is the investigation, the fix, and the proof the fix worked. Root cause uses 5 Whys or Fishbone.",
    example="An out-of-spec viscosity result opens an NCR, converts to a CAPA, root-causes to a mixing step at the filler, gets a corrective action, and cannot close until effectiveness is verified on a later batch. Closing without that verification is how the same defect returns.",
),
"Lab finding intake and OOS / OOT classification (SKN-OPS-006)": dict(
    what="Handling test results that come back wrong. Out of specification means outside the allowed range; out of trend means inside the range but drifting in a way that predicts a future failure.",
    example="Three consecutive batches test inside spec but each one lower than the last. That is OOT rather than OOS, and catching it is what stops the fourth batch from being a genuine failure.",
),
"Vendor quality flag and scorecard signal back to Purchasing": dict(
    what="When quality problems trace to a supplier, telling Purchasing in a form that affects future awards. The flag is the incident; the scorecard signal is what makes it count commercially.",
    example="Incoming components fail inspection twice in a quarter. The flag routes to Purchasing so the vendor scorecard reflects it before the next RFQ, rather than the same vendor winning again on price.",
),
"Batch hold and release (SKN-OPS-007)": dict(
    what="The decision to stop a batch from shipping, and the decision to let it go. Every hold and every release is an explicit, logged approval under SKN-OPS-007, not a status that drifts.",
    example="A batch is held pending a stability read. If the read passes it is released with the reason recorded; if it fails the hold becomes a disposition decision. Either way there is a name against it.",
),
"In-market stability testing decisions (PET, accelerated, real-time)": dict(
    what="Continuing to test product that is already on shelf. Real-time stability confirms the shelf life you printed is actually true, and PET confirms the preservative system still holds.",
    example="An 18-month real-time pull comes back weaker than the accelerated data predicted. That is a decision about the stated shelf life on future production, and possibly about what is already in market.",
),
"Near-expiry batch disposition at the 30-day threshold": dict(
    what="Deciding what happens to stock approaching expiry, at a fixed 30-day trigger rather than whenever someone notices. Sell through, discount, divert to sampling, or write off.",
    example="A batch hits 30 days out with meaningful units left. Moving it into PR seeding or sampling recovers some value; doing nothing turns it into a write-off at day zero.",
),
"Serious adverse event triage and recall kickoff (SKN-OPS-002, SKN-OPS-003)": dict(
    what="The highest-consequence path in the system. Triage decides whether a report is a serious adverse event; recall kickoff decides whether product comes off shelf. Recall requires an explicit kickoff phrase plus step-by-step approval, so it cannot start by accident.",
    example="A report describes a reaction needing medical attention. Triage classifies it as reportable, which starts both the internal investigation and the 15-day MoCRA filing clock on the regulatory side.",
),
"SOP ratification, annual review and cross-cutting quality tasks": dict(
    what="Owning the procedures themselves: approving a new revision, reviewing each SOP annually, and running the quality work that is not tied to one product, such as audits and retailer questionnaires.",
    example="SKN-OPS-008 goes from Rev 1.0 to Rev 2.0 after the Pedrero touchbase adds the Pantone, Canada and Quebec passes. Ratification is what makes the new revision the one the skills actually read.",
),
"Quality dashboard publish to the landing hub": dict(
    what="Publishing the quality picture where the team can see it, on weekly, monthly and quarterly cadences, to the landing hub rather than into a thread.",
    example="The weekly digest shows open CAPAs, batches on hold and complaint rate. Published on a cadence it becomes something people check; sent ad hoc it becomes something people miss.",
),
"Final quality check on product and documentation across every function": dict(
    what="The cross-function gate added on 2026-07-30. Each function still owns its own work, and this sits on top of it: a last read for inconsistency in either the product or the paperwork, anywhere in the business.",
    example="A launch packet is complete but the IL version on the artwork does not match the approved IL. Every individual function signed off correctly and the mismatch is still there. The gate is what catches that.",
),
"Quality management system framework and monthly quality-trend review": dict(
    what="Owning the shape of the quality system rather than running it: which SOPs exist, how the gates fit together, and the monthly review that turns individual events into a pattern worth deciding on.",
    example="One pump complaint is noise. A pattern across a quarter is a reason to reopen the packaging decision. The monthly trend review is where that becomes visible, and the pump issue is the live case.",
),

# ---------------------------------------------------------------- Regulatory & Compliance
"Pre-launch ingredient list review gate (SKN-OPS-008)": dict(
    what="Nothing launches until Pedrero has reviewed and approved the ingredient list for the approved formula. The IL packet is staged, sent, returned and archived with a version stamp.",
    example="A formula is approved at bench, so the IL packet goes to Amy Pedrero under the SKN-OPS-008 subject convention. Until the approval comes back with a version reference, artwork cannot be released to the printer.",
),
"Pedrero engagement and send approval": dict(
    what="Controlling what goes out to the external regulatory partner. Every send is composed internally, approved by the Reg Lead, and logged, because Pedrero has no access to our systems and the email thread is the record.",
    example="An attestation draft is ready for review. It goes out to Amy with Heather and Teona copied, under the right subject prefix, with a 10-business-day window recorded. Nothing substantive is drafted on Pedrero's behalf.",
),
"Claim substantiation and new-claim defensibility": dict(
    what="Holding audit-ready evidence for every claim on the product, and gating new claims before they ship. The file is what you hand over when a retailer audits or a competitor challenges.",
    example="Marketing proposes a firmer efficacy line for a serum. Before it reaches packaging it needs evidence that supports that specific wording, reviewed externally. The gate exists because the person who wants the claim should not be the one judging the evidence.",
),
"Label artwork archive, IL cross-check and label-law checks (Pantone, Canada, Quebec, 19-state toxics)": dict(
    what="Checking that what the printer prints matches what was approved, and that it satisfies the label laws that apply. Pantone per CA SB 343, Canada extended allergens, Quebec French-language, and packaging-toxics certificates across 19 states.",
    example="Carton artwork arrives at Revision 4. Cross-check confirms it carries the current approved IL, the recycling mark is the correct Pantone, and the French copy is present. A miss here reaches shelf.",
),
"Reformulation claim bridge when a SKU reformulates without QIL parity": dict(
    what="Deciding whether existing clinical and consumer-test claims survive a formula change. They do not carry over by default: formula similarity has to be established first, ideally by recovering the prior formula's qualitative ingredient list.",
    example="Eye Cream moves to a new manufacturer. The open order with the prior manufacturer keeps the QIL request path viable, so Pedrero can compare old against new and ride the claims through. If that window closes, the choice is analytical comparison testing or retiring the claim.",
),
"Retailer attestation responses (Sephora, Ulta, Whole Foods, Credo)": dict(
    what="The questionnaires that keep a SKU on a retailer's standards programme: Sephora Clean and Planet Positive, Ulta Conscious Beauty, Whole Foods, Credo. Each answer is mapped to evidence from the claim substantiation file.",
    example="A Sephora Clean renewal comes due. Each question is answered from the evidence file, gaps are flagged before anything is staged, Pedrero reviews, then the Reg Lead submits. Miss the renewal window and the SKU drops off the programme.",
),
"MoCRA registrations, state filings and Leaping Bunny renewal": dict(
    what="Keeping the company and its products registered where the law requires it, and keeping certifications current. MoCRA facility and product listings, state filings including Prop 65 and the EPR regimes, and the Leaping Bunny renewal.",
    example="An EPR threshold is approaching in a state where volume is growing. Registering ahead of it is routine; discovering it after crossing is a penalty conversation.",
),
"SAE and recall agency filings, including the 15-day MoCRA clock (SKN-OPS-009)": dict(
    what="The agency side of the worst days. A serious adverse event carries a 15-day statutory filing clock under MoCRA, and a recall carries an FDA classification and report. The clock runs from awareness, not from when the file is ready.",
    example="An SAE is classified as reportable. The 15-day clock starts, the FDA report is staged for Pedrero review, and the filing goes in inside the window with the submission logged against the event.",
),
"Regulatory fan-out routing and the regulatory dashboard publish": dict(
    what="Taking regulatory flags raised elsewhere, mostly out of Quality, and routing each to the skill that owns it, then publishing the regulatory picture on a monthly cadence.",
    example="A complaint surfaces a label-accuracy question. The Quality side flags it, the fan-out sends it to the label keeper rather than leaving it in a quality queue where no regulatory owner is watching.",
),
"Pedrero engagement letter, scope and renewal": dict(
    what="The commercial relationship with the regulatory partner rather than the work: scope, retainer, response windows, dispute resolution, and the annual renewal.",
    example="The engagement letter sets a 10-business-day standard response. When an attestation deadline is tighter than that, the tightened window has to be agreed rather than assumed.",
),

# ---------------------------------------------------------------- Retail & Wholesale
"Retailer and reseller first contact": dict(
    what="The front door for anyone who wants to sell Sweet July Skin: inbound retailer interest, reseller enquiries, and unsolicited distributor approaches. Deciding which are worth pursuing and which get a polite no.",
    example="A regional chain asks about stocking three SKUs. First contact establishes volume, terms and margin implications before it becomes a relationship, because a channel taken on bad terms is hard to unwind.",
),
"Retail channel launch programs: UBM cohort positioning, price ladder, Amazon Vendor": dict(
    what="Standing a SKU up in a retail channel, as distinct from running that channel day to day. Where the brand sits against its comp set on the shelf, how the range steps in price, and the mechanics of Amazon Vendor as a wholesale relationship.",
    example="Ulta Beauty Marketplace launched June 2026. Positioning decided which comp brands to sit adjacent to and which price band to claim. The open question is the lip at $20 against a $24 to $29 peer band, which reads as influencer-premium rather than accessible-prestige.",
),
"Wholesale pipeline and new retail partner development": dict(
    what="Working the list of potential retail partners forward: who is in conversation, at what stage, what it would take to close, and what the economics would be.",
    example="A specialty retailer is interested but their margin requirement puts two SKUs below floor. The pipeline decision is whether to go with a subset, reprice, or pass.",
),
"Retail price architecture and the pricing matrix": dict(
    what="The whole price structure across SKUs and channels: MSRP by archetype band, wholesale price, and the floors each channel has to clear. The matrix is what keeps a price change in one channel from breaking another.",
    example="Three SKUs sit below their archetype band today, Castaway Cream and Pava Toner at $30 and Castaway Cleansing Oil at $32. That is a price-architecture decision rather than a one-SKU question, because moving one step changes how the whole ladder reads.",
),
"Retailer promo calendar (Sephora, Ulta) and promo planning": dict(
    what="Which promotions you participate in, when, and at what depth. Retailer promo calendars are set months ahead and each event has a funding and margin consequence.",
    example="A gift-with-purchase event needs inventory committed well before the window and comes off margin. Planning it early is the difference between a funded promo and an unbudgeted one.",
),

# ---------------------------------------------------------------- Marketing & Brand
"Quarterly competitive teardowns across the five comp brands": dict(
    what="A deep quarterly read on the closest competitors: pricing, launches, claims, packaging, channel posture. Ten comp brands are profiled with tier ratings and full price ladders.",
    example="Summer Fridays sits at tier 1 as the closest structural peer, running $24 lip to $45 moisturizer to $49 hero mask to $82 fragrance. That ladder is the benchmark our own pricing gets read against.",
),
"Quarterly teardown sign-off before circulation": dict(
    what="Reading the teardown before it goes out and deciding it is right. A competitive read that circulates with a wrong conclusion gets repeated in decisions for a quarter.",
    example="A teardown concludes a competitor is discounting structurally when it was a one-off event. Sign-off is where that gets caught, before it becomes an argument for repricing.",
),
"Monthly competitive trend digest and cross-stream signal routing": dict(
    what="A lighter monthly pass on category movement, plus routing what it finds to whoever needs it. A competitor's pricing move is a margin signal; a packaging move is a PD signal.",
    example="A competitor launches a refillable format. That routes to PD as a packaging question and to Margin as a cost one, rather than sitting in a digest nobody actions.",
),
"Social listening and comp brand monitoring (TikTok, IG, Pinterest, retailer new arrivals)": dict(
    what="Watching what the category and the comp set are doing in public, including retailer new-arrivals pages, which is often where a competitor launch shows up first.",
    example="A comp brand's lip product starts trending on TikTok. Volume signals like that are why lip is treated as the category-leading gateway SKU across the cohort.",
),
"Brand guideline custody (fonts, colors, logos, voice)": dict(
    what="Holding the definitive brand guidelines and deciding when something departs from them. Custody means the current version is unambiguous and exceptions are decisions rather than drift.",
    example="A campaign wants a typeface outside the system for one execution. That is a custody decision, and saying yes once without recording it is how a brand system stops being one.",
),
"Annual team holiday communications (11 sends across 3 templates)": dict(
    what="The internal holiday and office-closure notices: 11 scheduled sends built from three templates, auto-sent on date, always from Alvin with the team on BCC.",
    example="The November Holiday Season Overview goes out ahead of Thanksgiving so nobody is planning work into a closure. Scheduled rather than remembered.",
),
"Weekly founder briefing, Slides 5 and 6": dict(
    what="The weekly operations read for Ayesha, in the Canva deck. Slide 5 is business operations, Slide 6 is product development from the ops angle, filtered to founder-level signal.",
    example="A supply-chain risk that could move a launch date belongs on Slide 5. A routine PO acknowledgement does not. The filter is the work.",
),
"Operational special projects: labels, PR seeding, sampling": dict(
    what="The operational side of marketing pushes: getting labels produced, product into the right hands for PR, and samples where they need to be. Named explicitly in the Operations Specialist job description.",
    example="A press moment needs 200 units kitted and shipped to a list by a date. That is a fulfilment project with a deadline, and it competes with regular order flow for the same hands.",
),
"Campaign direction and seasonal brand moments": dict(
    what="What the brand is saying this season and why: the concept, the moment, the hook. Added as a row on 2026-07-31 because it did not exist anywhere, which is why the President had almost no Marketing presence.",
    example="A summer moment built around a hero SKU sets what Creative produces, what Klaviyo sends, what paid amplifies and what inventory has to be in position. Direction first, execution after.",
),
"Editorial and content calendar": dict(
    what="What goes out when, across channels. The calendar is what turns campaign direction into dated, owned deliverables.",
    example="A launch date drives backwards into content shot dates, email sends and social posts. Without the calendar the launch arrives before the assets do.",
),
"Email marketing: Klaviyo flows and campaign sends": dict(
    what="Owned-audience email: the automated flows that run continuously (welcome, cart, post-purchase) and the one-off campaign sends. Executed by WITHIN.",
    example="A campaign send goes to a segment while the abandoned-cart flow keeps running underneath. Flows compound quietly; campaigns spike. Both are needed and they are planned differently.",
),
"Paid media: Meta, Google and channel spend": dict(
    what="Bought audience across Meta and Google, and how much goes into each. Run by WITHIN, with margin floors as the constraint on spend.",
    example="Q3 strategy confirmed Pineapple Punch as the primary driver at the 20 July review. Spend concentrates behind a driver rather than spreading, and Alvin is consulted where spend runs against margin floors.",
),
"Social media content and publishing": dict(
    what="Producing and posting the organic social content, day to day, in the brand voice.",
    example="A product moment needs native content per platform rather than one asset cross-posted. Kate runs the calendar and the publishing.",
),
"Influencer and earned media programs": dict(
    what="Getting the product to people whose audiences matter and earning coverage rather than buying it. Seeding lists, gifting, relationships and press.",
    example="A seeding push around a launch overlaps with the operational sampling work, which is why the two rows connect: someone has to pick the list and someone has to ship it.",
),
"WITHIN agency relationship and quarterly business reviews": dict(
    what="Managing the digital marketing agency as a commercial relationship: scope, performance, spend and the quarterly review.",
    example="The 20 July QBR set Q3 strategy. Reviews are where the agency's performance gets read against what it costs, rather than the relationship running on autopilot.",
),

# ---------------------------------------------------------------- Creative
"Creative direction on packaging, artwork and brand visuals": dict(
    what="The aesthetic and craft decisions on how the product and brand look. Erin holds the technical authority on packaging and artwork.",
    example="A carton needs a finish decision that affects both look and unit cost. Creative direction makes the call, Ayesha is consulted because the brand carries her name, and the cost consequence lands in the margin work.",
),
"Packaging and artwork execution": dict(
    what="Producing the actual files to print-ready standard: dielines, mechanicals, decoration specs and version discipline.",
    example="Direction is settled and Jan executes the mechanical against the current dieline and current IL. Execution errors are expensive here because they are discovered at print.",
),
"Creative Requests intake and design coordination": dict(
    what="The single queue for design asks from across the business, so requests get prioritised rather than arriving as direct messages.",
    example="Three teams need assets in the same week. The intake queue makes the contention visible so it can be sequenced, instead of whoever asked loudest going first.",
),

# ---------------------------------------------------------------- Ecommerce & DTC
"Shopify revenue and channel position read": dict(
    what="Reading what the store is actually doing: revenue, orders, conversion, and how DTC sits against the other channels.",
    example="DTC revenue is flat while Amazon grows. That changes where inventory should sit and where promo money should go, so somebody has to be reading it rather than reporting it after the quarter.",
),
"Daily DTC fulfillment KPIs and the SJ Shipping Dashboard": dict(
    what="The daily service picture after the order ships: on-time rate, late shipments, errors, returns. Lives in the SJ Shipping Dashboard project.",
    example="On-time delivery slips two days running. Caught daily it is a conversation with the 3PL; caught monthly it is a pattern of customer complaints you now have to answer.",
),
"Channel operations and promo setup across DTC, UBM and Amazon": dict(
    what="Configuring each channel to sell correctly: listings, pricing, availability and promo mechanics, in three places that each work differently.",
    example="A sitewide promo has to be built in Shopify, reflected on UBM, and handled on Amazon where you do not fully control price. A mismatch across the three is visible to customers immediately.",
),
"Proactive reships and fulfillment-issue resolution": dict(
    what="Fixing a customer's order before they have to chase you. A lost shipment, a damaged arrival or a mis-pick gets reshipped on our initiative.",
    example="Tracking shows a parcel stalled for a week. Reshipping without waiting for the complaint costs one unit and keeps the customer; waiting costs the unit anyway plus the relationship.",
),
"Amazon channel management (FBA, AWD, Seller Central)": dict(
    what="Running Amazon as an operational channel: FBA inbound and storage, AWD as upstream warehousing, and the Seller Central listing side, as distinct from the Vendor wholesale relationship.",
    example="An FBA restock has to be planned around Amazon's inbound limits and fee windows. Getting that wrong strands inventory in the wrong place while the listing shows out of stock.",
),
"Product detail page content and product copy": dict(
    what="What the customer reads before buying: titles, bullets, descriptions, ingredient copy and imagery, on the store and on retailer pages.",
    example="A claim on a PDP has to match what the claim substantiation file supports. Marketing writes it, but a claim that outruns the evidence is a regulatory problem on a marketing surface.",
),

# ---------------------------------------------------------------- Finance
"Margin architecture framework and quarterly portfolio review": dict(
    what="The ratified margin framework and the quarterly sweep of every active SKU against every channel floor, plus the four portfolio-level checks.",
    example="The quarterly review runs wholesale floor hold, specialty prestige readiness, the 25 percent acquisition-mix cap and perpetual launch mode, and reports four traffic lights with exceptions named.",
),
"Per-SKU margin pressure-test against channel floors": dict(
    what="Running one SKU's real landed cost and price against each channel's floor to see where it clears and where it fails. Channel-by-channel pass or fail with a margin waterfall.",
    example="A serum clears DTC comfortably, clears Ulta Marketplace, and fails the Sephora floor. That is a launch-scope decision before it is a pricing one.",
),
"Walk-away decision when a SKU breaks its channel floor": dict(
    what="What to do about a SKU that does not pencil, in the framework's order of preference: reformulate, reprice, restrict to fewer channels, or retire. Acquisition SKUs reorder that, putting restrict ahead of reformulate.",
    example="A SKU misses its specialty floor by a few points. Reformulating to take cost out is preferred; restricting it to DTC and Amazon is the fallback that keeps it alive without breaking the channel.",
),
"SKU archetype and Standard / Acquisition designation": dict(
    what="Two tags set at concept approval, before the BOM locks, that drive the price band and the COGS composition limits. Archetype is what the product leads with; designation is why it exists commercially. Neither can be changed retroactively.",
    example="A vitamin C serum leading with a 15 percent active is formula_hero. A cooling eye treatment with a metal applicator is ritual_hero. Tagging the second as the first puts it in the wrong price band with the wrong cost ceiling.",
),
"Monthly and quarterly vendor cost rollups": dict(
    what="Adding up what each vendor and category actually cost over the period, from the captured invoice data. What makes spend visible by function rather than only in aggregate.",
    example="Regulatory spend year to date is a number you can only produce if every Pedrero invoice was classified correctly at capture. The rollup is where misclassification shows up.",
),
"Accounts payable, bookkeeping and payroll": dict(
    what="The transactional finance engine: paying suppliers, keeping the books, running payroll. Executed by Ironclad Finance, with no internal finance headcount.",
    example="A vendor invoice moves from approval into the payment run and onto the ledger. Alvin answers for the cost side because it flows out of purchasing and the inventory ledger.",
),
"Month-end close and management reporting": dict(
    what="Shutting the period and producing the numbers leadership decides on. Reconciliations, accruals, and the reporting pack.",
    example="Close cannot finish until inventory valuation is settled, which is why the cost side and the reporting side have to hand off cleanly each month.",
),
"Annual budget and forecast consolidation": dict(
    what="Building the annual plan and keeping the rolling forecast honest against it. Consolidated by Ironclad with Danielle accountable.",
    example="A hire and a launch both land in the same quarter. The budget is where those compete for the same money rather than being approved separately.",
),
"Inventory valuation and cost of goods": dict(
    what="What the stock on hand is worth and what each unit sold actually cost. Feeds both the balance sheet and every margin calculation.",
    example="A landed-cost error on a component flows into COGS, which flows into the margin pressure-test, which is how a SKU can look like it clears a floor when it does not.",
),

# ---------------------------------------------------------------- People & Admin
"Hiring the Operations Specialist and the PD Project Manager Specialist": dict(
    what="The two approved roles from the 2026-07-17 redesign, both reporting to Nicole. Ops Specialist first, PD Specialist phased in after.",
    example="Both seats appear on the matrix as columns with transition arrows, so you can see exactly which activities move on hire: 18 to Ops, 16 to PD.",
),
"Tool procurement, vendor renewals and shared-folder admin": dict(
    what="The software and access side of running the business: buying tools, catching renewals before they auto-charge, and keeping shared storage organised.",
    example="A seat-based tool renews annually whether or not the seats are still used. Catching it before renewal is the only time you can right-size it.",
),
"Employee onboarding, offboarding and access deprovisioning": dict(
    what="Getting someone working on day one and fully disconnected on their last, split across two partners. Calm HR runs the employment side, Coastal Interactive runs equipment and accounts, and the internal systems half stays in-house.",
    example="The departed-role-holder checklist exists because a stale role record broke collaborator resolution during a build. Asana reassignment and wiki contact state are as much a part of offboarding as returning a laptop.",
),
"Operations Specialist recruiting": dict(
    what="The live search: job description, sourcing through Calm HR, screening, interviewing and offer. Prioritised ahead of the PD role.",
    example="Danielle's condition was cleaning up the system first so the role can function, which is why SOP cleanup and the 22 unassigned tasks close before a start date.",
),
"PD Specialist role definition and phased recruiting": dict(
    what="Scoping the second seat properly before recruiting it. Framed as project management and accountability, air traffic control rather than strategy or ideation.",
    example="The job description names running the quality system outright, plus document control and product regulatory work. Until it is filled, Nicole gates quality and Alvin executes it.",
),
"SOP cleanup and operational prep before new-hire onboarding": dict(
    what="Making the system fit to hand over: procedures current, queues clean, nothing waiting in an archived project. The precondition Danielle set on the hire.",
    example="22 tasks from the retired coordinator seat sit unassigned in a holding project with four overdue. Those close before an Ops Specialist starts, not after.",
),
"Employee handbook and HR policy": dict(
    what="The written employment terms and policies, maintained by Calm HR as co-employer with Alvin as liaison and Danielle co-approving.",
    example="A policy change has to be reflected in the handbook and communicated, not just decided. The co-employment arrangement is what makes that a shared obligation.",
),
"Benefits administration and payroll processing": dict(
    what="Enrolment, changes and the payroll run itself, through Calm HR as PEO on the Paylocity platform.",
    example="An enrolment window opens and every employee needs a decision recorded. Missing it means someone waits a year for coverage.",
),
"Employment compliance and separations": dict(
    what="Staying inside employment law and handling exits properly. Danielle is on every Calm HR thread and every separation.",
    example="A separation has documentation, final-pay and access consequences that run in parallel. Doing them in the wrong order is where the risk is.",
),

# ---------------------------------------------------------------- IT / Systems & Data
"PLM schema, write path, audit log and Supabase wiki custody": dict(
    what="The product data layer that every skill reads at run time: the Supabase schema, the single sanctioned write path, the audit log, and the wiki pages the bridges resolve names against.",
    example="plm-assistant is the sole writer. Everything else stages a change and hands it over, which is what keeps the audit log meaningful and stops two systems writing conflicting product records.",
),
"Landing hub publish and Netlify Function maintenance": dict(
    what="The AC Brands landing hub where dashboards are published, and the serverless functions behind them. Publishing goes through a GitHub commit and push, never a direct deploy.",
    example="The quality dashboard refresh publishes to the hub on cadence. The hub's own function map, with a named lead per business function, is what filled the marketing and wholesale gaps on this matrix.",
),
"Asana project, section, custom-field and connector configuration": dict(
    what="The Asana structure the skills depend on: projects, sections, custom fields and the connector setup. Change a section name and the automation that writes to it stops working.",
    example="A skill moves a task to In Pedrero Review by name. Renaming that section without updating the skill breaks the routing silently, which is why configuration is an owned activity rather than a preference.",
),
"Skill suite authorship, audit and versioning": dict(
    what="Writing, auditing and versioning the skills themselves, plus the role-maps and canonical files they read. The execution layer this quarter is meant to build out.",
    example="Retiring QA Lead as a gate label meant updating nine role-maps with resolution notes, because those are runtime config: leave them stale and every skill keeps routing CAPA closes to the wrong person.",
),
"The 23 scheduled Routines and their HITL gates": dict(
    what="The automations that run on a schedule and the human approval gates inside them. Each Routine re-reads its skill fresh on every run.",
    example="Every one of the 23 stops at an approval only Alvin can clear, so a week away queues work rather than pausing it. That is on the Gaps sheet as a single point of failure.",
),
"RACI and role framework across Operations and PD": dict(
    what="This matrix and the role structure behind it: who answers for what, which gates exist, and keeping it current as the org changes.",
    example="The document you are reading. It is generated from raci_rows.py in the repo, so a change made here has to land there to be real.",
),
"Website platform, Shopify storefront and web releases": dict(
    what="sweetjuly.com and the Shopify storefront as a product: platform decisions, theme and template work, and the release process. Developed by Teknologics.",
    example="A storefront release changes checkout. Danielle is accountable for the release, Nicole is the systems and tech owner, and Teknologics does the development.",
),
"Web and digital systems ownership, including the Teknologics engagement": dict(
    what="Owning the web and digital stack as a system rather than a project: integrations, data flow between store and back office, and the development partner relationship.",
    example="Scope note worth confirming: Nicole's systems-and-tech ownership is recorded against web and digital. PLM, Asana config, hub publish and the 23 Routines still sit with Alvin.",
),
"Back-end IT infrastructure, identity and endpoint management": dict(
    what="The infrastructure nobody sees until it breaks: accounts and identity, device management, and the back end. Run by Coastal Interactive as managed service, distinct from the storefront.",
    example="Single sign-on and endpoint policy apply across the team. Coastal is the back end, Teknologics is the storefront, and confusing the two sends an escalation to the wrong partner.",
),
"Equipment procurement, onboarding and asset lifecycle": dict(
    what="Buying, issuing, tracking and recovering hardware from purchase through to exit.",
    example="A new hire needs a machine configured before day one, and a leaver's machine has to come back and be wiped. Both are Coastal's execution with Alvin as liaison.",
),
"Coastal Interactive managed-service engagement and escalation": dict(
    what="The managed IT relationship: scope, escalation path and who to call when something is down.",
    example="An outage needs one clear escalation route rather than several people contacting the provider separately. Alvin is the liaison, which is what keeps that single-threaded on purpose.",
),
}
