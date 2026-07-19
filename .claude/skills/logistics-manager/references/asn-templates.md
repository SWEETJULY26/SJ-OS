# ASN templates and retailer compliance

The structured rule extract for each retailer's routing guide. Source PDFs live
in SharePoint under the logistics folder. PLM `retailer_compliance_specs` holds
the fields you enforce against. Update both when a routing guide rev lands.

---

## Ulta DC (UBM channel)

Active before June 2026 launch. Owned by Operations and Order Ops.

### ASN format

EDI 856 via Ulta's vendor portal (Open Text / GXS). Send the ASN before the
truck departs OC3PL. Ulta penalizes late ASNs (chargeback per PO line).

Required segment minimums:

- BSN (Beginning Segment) — shipment ID, ship date/time
- HL — hierarchical loop (shipment → order → tare → pack)
- TD1 / TD3 / TD5 — carrier, equipment, routing
- MAN — pallet GS1-128 SSCC
- PRF — Ulta PO number
- PO4 — case pack info
- LIN — UPC and Ulta item number per line
- SN1 — quantity shipped per line
- CTT — total transaction control

### Pallet build

Tier-by-pallet to Ulta's spec. Default (verify against latest spec row before
each ASN):

- Standard pallet: 48" × 40" GMA
- Max height: 60" inclusive of pallet
- Max weight: 2,000 lb
- Mixed-SKU pallets: only if labeled per Ulta spec — clearly identified, mixed
  pallet placard, manifest by tier
- Stretch wrap: minimum 4 wraps at top and bottom, full coverage

### Label spec

GS1-128 SSCC label per pallet. Placement: front and one short side, 50" from
floor (±2"). Barcode scan-readable horizontally.

Per-case label: UPC + Ulta item number + quantity. Placement on the long side
of the case so it scans when palletized.

### Routing

Ulta assigns the routing in the PO. Do not self-route. Default carrier is
typically a contracted LTL provider Ulta names per origin → destination DC pair.

### Hazmat

Skincare typically not hazmat, but flammable formulas (ethanol-based mists,
some treatments) need hazmat label and shipping paper. Flag at ASN draft if
the SKU's `hazmat_class` is non-null in PLM.

### Overage tolerance

Default 0% — Ulta does not accept overages. Underages tolerated up to 2% per PO
line; beyond that triggers a fill-rate penalty. Match SN1 quantity exactly to
PO line quantity; if a partial ship is unavoidable, surface it as a routing-
request issue before sending the ASN.

### Routing guide rev tracking

When Operations or Order Ops forwards a new Ulta routing guide PDF, parse the
diff against the current `retailer_compliance_specs.version`. Stage a write
with the new version number, last_updated date, and changed fields. Upload the
PDF to SharePoint.

---

## Amazon Vendor Central

Active. Owned by Operations.

### ASN format

EDI 856 plus Vendor Central portal entry. Submit before truck departs OC3PL.

### Prep requirements

These are the chargeback-driving fields. Verify against the spec row before
every ASN draft:

- Poly bagging: required for liquid SKUs and any SKU prone to leak. Suffocation
  warning printed.
- Expiration label: required for any SKU with shelf life. Date on the unit and
  on the case.
- Case pack: must match Amazon's expected case quantity per ASIN. If we ship a
  different case pack than Amazon expects, surface a relabel cost.
- Carton label: FNSKU barcode, scan-readable.
- Pallet label: ARN (Amazon Reference Number) on each pallet.

### Carrier

Amazon Partnered Carrier program when eligible (small parcel only); else SCAC
per PO. Ship window enforced — early or late ships chargeback.

### Hazmat

Amazon hazmat program is stricter than Ulta's. If the SKU has any flammable
component, route to Amazon's hazmat onboarding before adding to Vendor Central.

### Overage tolerance

Default 0%. Underages up to 5% accepted, beyond that chargebacks. Match
quantities exactly.

### Routing guide rev tracking

Same pattern as Ulta — parse PDF diff, stage write to
`retailer_compliance_specs`, upload PDF to SharePoint.

---

## Sephora — placeholder

Not yet active. When the channel opens:

1. Stage a new `retailer_compliance_specs` row with `retailer_name = 'Sephora'`
2. Parse Sephora's routing guide into the structured fields
3. Create a "Sephora" lane entry in `lane-playbooks.md`
4. Add lane to the weekly digest scope

---

## Compliance check workflow

When you draft an ASN, run this check before staging:

1. Pull the latest `retailer_compliance_specs` row for the retailer
2. Pull the underlying `outbound_orders` row for the retailer PO
3. Compare ship quantities to PO line quantities (overage tolerance)
4. Check pallet build math against `pallet_spec` — count cases per tier, tiers
   per pallet, total pallets, weight
5. Check hazmat handling against the SKU's `hazmat_class` field (read via plm-
   assistant)
6. If any check fails, surface as an exception with the failed rule named —
   don't auto-stage the ASN until resolved
7. If all checks pass, draft the ASN per the format spec and stage for
   Operations or Order Ops to send

Failed checks land in the `Outbound — Retailer` section of the Asana project
with the exception_flag set on the related shipment row.
