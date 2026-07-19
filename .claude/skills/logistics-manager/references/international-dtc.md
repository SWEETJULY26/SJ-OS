# International DTC reference

Cross-border DTC is its own lane. The failure mode is not a domestic carrier
losing a parcel — it is a customs authority refusing the parcel, a customer
getting hit with a duty bill they did not expect, or a regulatory filing
that should have been on file before the first order shipped and was not.

This file holds the per-market posture, the Canada playbook (the live market),
and the criteria a cross-border partner has to meet before SJS routes consumer
parcels through them.

Writing follows the AC Brands writing style rules in the organization-wide
Claude instructions.

---

## Per-market compliance posture matrix

The four realistic next markets for SJS DTC are Canada, EU, UK, and AU. Each
has a different regulatory filing requirement, a different labeling rule set,
and a different DDP-vs-DDU answer.

| Market | Customs broker required | Regulatory filing | Labeling requirement | DDP vs DDU | Restricted-ingredient source |
|---|---|---|---|---|---|
| Canada | Yes (partner-included or direct) | CNF (Cosmetic Notification Form) per SKU before first import | Bilingual (English + French) ingredient list, metric net contents, importer of record | **DDP-at-checkout — recommended** | Health Canada Cosmetic Ingredient Hotlist |
| EU (when launched) | Yes | CPNP (Cosmetic Product Notification Portal) per SKU before first import; Responsible Person required | EU INCI list, e-mark net contents, RP address, batch code, PAO/expiry | DDP-at-checkout — recommended at launch | EU Cosmetic Regulation 1223/2009 Annex II–VI |
| UK (when launched) | Yes | UK SCPN (Submit Cosmetic Product Notification) per SKU; UK Responsible Person required | UK INCI list, RP address, batch code, PAO/expiry | DDP-at-checkout — recommended at launch | UK Cosmetic Regulation Annex II–VI |
| AU (when launched) | Yes | NICNAS (now AICIS) registration; cosmetic ingredient inventory check | AU ingredient list, net contents, Australian sponsor | DDP-at-checkout — recommended at launch | AICIS Inventory + Therapeutic Goods Order |

DDP-at-checkout is the recommended posture across all four markets. The reason:
the live customer-pays-duties complaint that drove this flow proved DDU is a
customer experience failure even when it is the cheaper-to-operate option.
Customers do not expect a second invoice from a foreign carrier. DDU is permitted
only as a named exception (high-value bundle that prices through the threshold
intentionally, or a market-entry test where partner integration is not yet in
place). Document the exception on the shipment row in `notes`.

---

## Canada playbook

Canada is the live market. CBSA is refusing parcels today. This section is the
operating playbook for getting that fixed and for keeping it from breaking again.

### CNF filing workflow with Pedrero

Pedrero Regulatory is the interim external partner for Canadian cosmetic
notifications. Every SJS SKU sold into Canada needs a CNF on file with Health
Canada before the first parcel ships. The workflow:

1. **Trigger.** New SKU approved for Canada launch, or existing SKU with a
   formula change that affects the CNF (ingredient added, removed, or
   reclassified).
2. **Stage.** Draft the CNF request — SKU, INCI ingredient list, function code,
   product type code (Health Canada uses ICCR codes), responsible party (SJS).
   Send to Pedrero with the supporting documents (formulation breakdown,
   product label image, INCI confirmation from the filler).
3. **File.** Pedrero submits to Health Canada through the CNF portal. Health
   Canada returns a CNF number and effective date.
4. **Capture.** Log the CNF number on the SKU's PLM regulatory record and
   reference it on every Canada-bound `international_outbound_dtc` shipment
   row in `regulatory_filing_ref`.
5. **Status check.** CNF status is read-only after filing — there is no
   periodic renewal. A formula change requires a new CNF; a label-only change
   does not. Pedrero confirms whether a change triggers a refile.

If a Canada order ships without a CNF on file, the parcel is at risk of CBSA
refusal under the Cosmetic Regulations (Food and Drugs Act). That is the
failure mode driving this flow.

### Health Canada Cosmetic Ingredient Hotlist cross-check

The Hotlist is a list of ingredients that Health Canada either prohibits or
restricts in cosmetics sold in Canada. It is updated periodically — the
last revision was 2022, with a published change log. Cross-check the SJS
ingredient master against the current Hotlist whenever:

- A new SKU enters the Canada launch path
- A formula change adds an ingredient to an existing Canada SKU
- Health Canada publishes a Hotlist revision (rare but blocking when it
  happens — surface to PD and Quality immediately)

A prohibited ingredient blocks the SKU from Canada. A restricted ingredient
requires a concentration check and may need a labeling caveat. If the Hotlist
flag triggers and the SKU is already shipping, pause Canada DTC for that SKU
and route the formula question through quality-manager (when v5 lands) or
the filler's R&D contact.

### Bilingual labeling

Canada cosmetic labeling has three non-negotiables that catch SJS at the
SKU-design stage:

- **Bilingual ingredient list.** English INCI plus French equivalents (or
  the Health Canada-approved bilingual format). Filler-sourced labels need to
  carry both before Canada launch.
- **Metric net contents.** Net contents in metric units (mL or g). Imperial
  alone is non-compliant.
- **Importer of record.** A Canadian importer name and address must be on
  the label or on a permanent-affix sticker. SJS uses the cross-border
  partner's Canadian entity for this in the current setup.

Label proofs go through Pedrero for compliance review before the first
production run for Canada. A failed bilingual check raises a
`bilingual_label_fail` exception flag on the shipment row.

### DDP-at-checkout — recommended posture for Canada

DDP-at-checkout means the customer sees the duty and tax in the cart total
at checkout and pays it as part of the order. The cross-border partner
remits the duty to CBSA on entry. The customer never gets a second invoice
from the carrier.

This is the recommended posture for Canada. The case:

- Customer experience parity with US — one price, one charge, no surprise
- Refusals drop because duty is prepaid and the entry is clean
- Margin impact is bounded and visible at the cart, not after the fact

DDU (delivered duty unpaid) means the customer pays duty to the carrier on
delivery. It is cheaper to operate but generates the customer-pays-duties
complaint that drove this flow. Permit DDU only as a named exception with the
reason captured on the shipment row.

### Sample HS codes for SJS cosmetics

Indicative HTS chapter 33 codes for the realistic SJS Canada SKUs. The
broker classifies on the entry — these are the working set, not authoritative.

- Cleansing balm — HTS 3304.99 (other beauty / skin care preparations)
- Body butter — HTS 3304.99
- Lip treatment — HTS 3304.10 (lip preparations)
- Toner / essence — HTS 3304.99
- Hair treatment / scalp serum — HTS 3305.90 (other hair preparations)
- Bar soap — HTS 3401.11 (toilet soap)

Confirm with the cross-border partner's broker on the first entry per SKU.
Capture the final HTS on `declared_hts` on the shipment row.

---

## Cross-border partner evaluation criteria

A cross-border partner sits between SJS DTC and the destination country's
customs authority. They run the declaration, remit duty, and forward the
parcel to the consumer. The criteria below are the bar a candidate has to
clear before SJS routes parcels through them.

**DDP-at-checkout — must-have, not nice-to-have.** The whole point of this
lane is to land the duty in the cart total. A partner that only does DDU is
not a fit.

**Shopify integration.** Native Shopify app or a clean API integration with
documented developer support. The partner injects landed cost (price + duty +
tax + cross-border shipping) into the cart at checkout. A manual workaround
adds operational cost and breaks DDP at scale.

**Broker function — included or referred.** Some partners include customs
broker function in their service. Others refer to a third-party broker and
SJS pays the broker separately. Both work, but the cost split has to be
visible upfront — partner fee, broker fee, duty, parcel forwarding — so
margin impact is clean.

**Margin impact at the bag level.** Run a worked example with a
representative SJS bag (typical Canada AOV, typical bag composition).
Confirm the cross-border-margin-impact stays within the threshold set in
the SJS margin architecture. If a partner takes the bag below floor on a
typical mix, they are not a fit.

**EU expansion roadmap support.** Canada is live; EU is the next realistic
market. A partner that supports CPNP-aware fulfillment, EU Responsible
Person sign-on, and UK SCPN is a stronger fit than a Canada-only player.
Capture the partner's EU roadmap before the Canada decision so the next
expansion is not a forced switch.

Score candidates on these five criteria and capture the score on the
vendor record in PLM (`vendors.notes` until a structured field exists).
The current Canada partner of record gets re-scored on the same scale at
the next contract review.
