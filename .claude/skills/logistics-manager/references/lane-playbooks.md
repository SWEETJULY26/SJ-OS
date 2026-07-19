# Lane playbooks

Per-lane operating notes for the live SJS freight network. Updated as we run.

This file holds the muscle memory for each lane — origin, destination, carrier
of record, typical transit, customs profile, and the things that go wrong.
When you draft a shipment record for a known lane, the defaults should match
what's documented here. When something doesn't match, surface it as an exception
on the shipment row.

---

## Inbound finished-goods lanes

### KDC-One (skincare bulk + fill)

- Origin: KDC-One facility (verify exact site per program)
- Destination: OC3PL Anaheim
- Typical carrier: LTL pallet, KDC's freight contract
- Transit: 3–5 business days domestic
- Customs: N/A
- Bulk-to-fill split: when bulk is produced at one KDC site and filled at
  another, the bulk leg is a separate `fg_inbound` shipment with its own
  receipt confirmation. The fill leg is what eventually ships to OC3PL. Both
  legs land on `shipments` with `bulk_to_fill` tag.
- Common failure mode: KDC sometimes splits a single PO across multiple ship
  dates without telling us. Watch for partial receipts at OC3PL that don't
  match the PO total.

### Vegelabs (cleansing/body bulk + fill)

- Origin: Vegelabs facility
- Destination: OC3PL Anaheim
- Typical carrier: LTL pallet
- Transit: 2–4 business days domestic
- Customs: N/A
- Common failure mode: Vegelabs ASNs sometimes lag the actual ship date by 24
  hours. If a tracking number arrives before the ASN, log the shipment from the
  tracking number; the ASN updates later.

### Allure Labs

- Origin: Allure Labs (West Coast)
- Destination: OC3PL Anaheim
- Typical carrier: LTL pallet, occasionally direct van for short-distance runs
- Transit: 1–3 business days
- Customs: N/A
- Common failure mode: Allure invoices arrive separately from the freight bill;
  cross-check both before logging final landed cost.

---

## Inbound component lanes

### HCT (primary packaging — Asia origin)

- Origin: HCT factory (China typically; verify per PO)
- Destination: filler (KDC-One or Vegelabs depending on program)
- Typical carrier: ocean freight via Flexport, occasional air for rush
- Transit: 30–45 days ocean, 5–7 days air
- Customs: yes — broker via Flexport, HTS code per PO line, duty paid logged
  to shipment row, brokerage fee logged separately
- Common failure mode: long lead time amplifies any ETA shift. Holds at LA/LB
  customs add 3–10 days easily. Surface every customs status change as a
  weekly digest exception until cleared.

### Element Packaging

- Origin: Element (domestic)
- Destination: filler (typically KDC-One)
- Typical carrier: LTL pallet
- Transit: 3–5 business days
- Customs: N/A
- Common failure mode: Element occasionally short-ships components when their
  upstream supplier has a quality reject. Confirm received quantity matches PO
  before closing the shipment.

### Impress Packaging (Asia origin)

- Origin: Impress factory (China)
- Destination: filler
- Typical carrier: ocean freight via Flexport
- Transit: 30–45 days ocean
- Customs: yes — same pattern as HCT
- Common failure mode: same long-lead-time amplification as HCT, plus Impress
  has had recent QC reject events that triggered RTV (out of scope for v4 —
  inventory-manager carries until v4.1+).

### CDW (variable origin)

- Origin: depends on component (verify per PO)
- Destination: filler
- Typical carrier: varies
- Customs: case-by-case
- Common failure mode: CDW catalog spans multiple origins; check the PO line
  rather than assuming.

---

## Outbound retailer lanes

### Ulta DC (UBM)

- Origin: OC3PL Anaheim
- Destination: Ulta DC (location varies by PO routing — Romeoville IL, Greer
  SC, Chambersburg PA, Phoenix AZ, depending on assignment)
- Typical carrier: retailer-mandated routing (Ulta routing guide, see
  `asn-templates.md` and `retailer_compliance_specs` table)
- Transit: 2–6 business days depending on DC and origin
- ASN format: EDI 856 via portal
- Compliance hot buttons: pallet build to spec (Ulta's tier-by configuration is
  strict), GS1-128 label placement, advance ship notice timing (must be in
  Ulta's portal before truck arrival)
- Common failure mode: a routing guide rev that we miss until a chargeback hits.
  Run the compliance check against the latest `retailer_compliance_specs.version`
  before every ASN draft.

### Amazon Vendor Central

- Origin: OC3PL Anaheim
- Destination: Amazon FC (varies by PO)
- Typical carrier: Amazon Partnered Carrier program when eligible, else SCAC
  per PO
- Transit: 3–7 business days
- ASN format: EDI 856 plus Vendor Central portal
- Compliance hot buttons: prep requirements (poly bagging, expiration label,
  case pack), ASN window, label format
- Common failure mode: prep violations. Verify case pack and prep against the
  Amazon Vendor compliance spec before staging the ASN.

### Sephora — future

Not yet active. Add lane and `retailer_compliance_specs` row when the channel
opens.

---

## Outbound DTC escalation

### OC3PL → consumer (escalation only)

Daily volume is owned by oc3pl-order-manager. Logistics picks up only when:

- Carrier loses a shipment (UPS / FedEx tracker stalled past expected window)
- Address bounce → reship workflow
- RIA from OC3PL where carrier needs a claim or tracer
- Class-action-shaped pattern (multiple consumer reships in a week pointing to
  a single failure mode)

See `escalation-playbook.md` for the carrier-by-carrier process.
