# Customs quick reference

For every Asia-origin lane (HCT, Impress, sometimes CDW), customs status is a
first-class field on the `shipments` row. Brokerage fee, duty paid, and freight
all roll into landed cost so sjs-margin-architect sees accurate inputs on the
next reorder.

You don't file customs entries yourself. You track status, log costs, and
escalate holds.

---

## Status values

`shipments.customs_status` enum:

- `n_a` — domestic lane, no customs leg
- `in_clearance` — broker has the entry; clearance pending
- `cleared` — released, freight on the way to final destination
- `hold` — CBP or another agency placed a hold; document review or other action
  needed
- `examination` — CBP pulled the container for inspection (cost + delay risk)

Any status other than `n_a` or `cleared` is an exception that surfaces in the
weekly digest. Examinations are SLA-critical — surface them same-day.

---

## Cost fields

When a shipment clears customs, log three numbers to the shipment row:

- `duty_paid` — the duty Flexport (or another broker) paid CBP on our behalf,
  invoiced back to us
- `brokerage_fee` — Flexport's customs brokerage charge for handling the entry
- `freight_paid` — the freight charge from origin to destination (ocean or
  air, plus drayage if applicable)

Roll-up:

```
landed_cost_line = freight_paid + duty_paid + brokerage_fee + (any other
  shipment-level adjustments — fuel surcharge, demurrage, detention)
```

That's what feeds sjs-margin-architect. Allocate to component cost in PLM
proportional to the PO line value.

---

## Brokers we use

**Flexport.** Primary for HCT and Impress ocean lanes. Email pattern: notify
emails come from `@flexport.com`. Customs status updates land in our inbox with
subject lines including "Customs", "Clearance", "Released", or "Held". The
outlook-plm-bridge is configured to detect these and stage shipment status
updates automatically.

**Other brokers.** Occasionally a one-off vendor uses a different broker. Log
the broker name on the shipment row; the bridge will need a manual paste until
patterns are added.

---

## KORUS FTA — Korea-origin cosmetics

The US–Korea Free Trade Agreement (KORUS) lets Korea-origin cosmetics clear
US customs at zero duty under HTS chapter 33, provided a valid Certificate
of Origin (COO) is on file at entry. The realistic SJS Korea-origin SKUs
sit in:

- HTS 3304.99 — other beauty / skin care preparations
- HTS 3307.90 — other perfumery, cosmetic, and toilet preparations

Without a valid COO, the broker pays the Column 1 (MFN) duty rate at entry.
That is the verification number on every Korea air-to-LAX entry: KORUS
zero-rate vs Column 1.

### Broker workflow

1. Vendor (Korean filler or component supplier) issues a Certificate of
   Origin per shipment, signed and dated, referencing the commercial
   invoice and the HTS line(s) claiming KORUS preference.
2. Broker validates the COO — exporter, producer, importer, HTS, origin
   criterion — before filing the entry summary.
3. Broker references the COO on the entry summary and applies the KORUS
   preference indicator.
4. Duty calc on the entry reflects the KORUS zero-rate. Capture both
   numbers on the shipment row — declared value, duty paid (zero under
   KORUS), brokerage fee — so the verification is visible in the
   landed-cost roll-up.

### Common failure modes

- **Missing COO at entry.** Broker pays Column 1 to release the
  shipment, then files a post-entry adjustment to claim KORUS preference
  and refund the duty. The refund path is slow (weeks to months) and
  ties up cash. Surface as an exception flag on the shipment row.
- **Declared origin mismatched against COO.** Origin field on the
  commercial invoice does not match the COO origin (e.g., COO says
  Korea, invoice says China for a co-packed component). Broker rejects
  KORUS preference; Column 1 duty applies. Catch this at the PO-issue
  step with the vendor.
- **COO covers wrong period.** Some Korean exporters issue blanket COOs
  by year. If the shipment date falls outside the COO validity window,
  the COO does not apply. Verify the date range on every entry.

### Duty calc check

```
korus_savings = commercial_invoice_value × column_1_rate − 0
```

For HTS 3304.99 the Column 1 rate is currently zero MFN as well, so the
KORUS savings on that line is zero in dollar terms but the preference
filing is still procedurally required. For HTS 3307.90 Column 1 is
typically 5.4% — that is the savings line on KORUS.

This is a sanity check, not authoritative. Defer to the broker's actual
entry classification and rate.

---

## HTS code reference

We don't author HTS codes. The vendor and broker classify each component. Your
job is to capture the HTS code on the shipment row (`hts_code_ref`) so it ties
back to the component for future reference. The broker's commercial invoice
shows the HTS code per line — pull from there.

If a shipment has multiple HTS codes (multi-component PO), capture the dominant
code and note the split in the shipment's exception_flags JSONB:

```json
{
  "multi_hts": true,
  "hts_codes": ["3923.10.0000", "3923.50.0000"],
  "primary_hts": "3923.10.0000"
}
```

---

## Duty calc mental model

A rough sanity check for whether a duty number looks right:

```
duty_paid ≈ commercial_invoice_value × duty_rate
```

Most primary packaging from China (HCT, Impress) sits in the 3.0–5.3% range
for HTS chapter 39 (plastics), plus any active Section 301 List 4A or 4B
tariff (currently 7.5%–25% depending on classification). So an effective rate
of 8%–30% on commercial invoice value is plausible. If the broker invoices
something far outside that band, ask them to confirm before logging.

This is a sanity check, not authoritative classification. Always defer to the
broker's actual entry.

---

## Broker email patterns the bridge looks for

The outlook-plm-bridge has these triggers configured under `broker_signals`:

- Subject contains "Customs Released" or "Cleared" → stage `customs_status =
  cleared` and surface for cost-log entry
- Subject contains "Hold", "Manifest Hold", "MET Hold", "ADD Hold" → stage
  `customs_status = hold` and create exception flag
- Subject contains "Examination", "Exam", "CET" → stage `customs_status =
  examination` and create exception flag
- Subject contains "Duty Statement" or "Customs Invoice" → extract duty + fee
  values and stage cost log

When the bridge stages an update, the shipment row appears in the Asana Customs
Watch section with a draft status change waiting for Operations approval.

---

## Escalation paths

Hold or examination on a shipment that's gating a production run:

1. Confirm hold reason with the broker (manifest, ADD, MET, ag, FDA, etc.)
2. If FDA-related, route to regulatory-manager when v6 lands; until then, surface
   to Pedrero Regulatory contact
3. If document-driven (commercial invoice missing detail, packing list
   mismatch), draft the broker outreach and stage for Operations to send
4. If random exam, time is the only path; update the digest exception every 48
   hours until cleared

Log the timeline in the shipment's `exception_flags` JSONB so we have data on
broker performance over time.
