# ASN draft — staged write

Use this form when staging an Advance Ship Notice for a retailer outbound
shipment. Currently active retailers: Ulta DC (UBM channel) and Amazon Vendor
Central. Sephora when the channel opens.

The form stages an ASN ready to send through the retailer's vendor portal.
Operations or Order Ops sends; the skill logs the send back through
outlook-plm-bridge once the confirmation lands in Sent Items.

Reference the structured retailer specs at `references/asn-templates.md` and
the live row in PLM `retailer_compliance_specs` for the latest segment and
prep requirements.

---

## Form fields

```yaml
shipment_id: <FK to shipments.id>
retailer: <Ulta|Amazon|Sephora>
retailer_po: <retailer's PO number — Ulta PRF, Amazon PO>
ship_window:
  start: <YYYY-MM-DD>
  end: <YYYY-MM-DD>
ship_date: <YYYY-MM-DD, planned actual ship date>

# --- Compliance check results ---
compliance_check:
  spec_version: <retailer_compliance_specs.version row used>
  pallet_build_pass: <true|false>
  label_spec_pass: <true|false>
  hazmat_pass: <true|false>
  overage_pass: <true|false>
  ship_window_pass: <true|false>
  failures: <array of plain-language fail reasons, empty if all pass>

# --- ASN content ---
lines:
  - line_number: <int>
    upc: <12-digit UPC>
    retailer_item_id: <Ulta item number or Amazon ASIN>
    sku: <SJS internal SKU>
    qty_shipped: <int, must match PO line within tolerance>
    case_pack: <int>
    cases: <int>
    pallets_for_line: <int, may be fractional in jsonb>

pallet_count: <total pallet count>
total_weight_lb: <decimal>
carrier: <carrier per Ulta or Amazon assignment>
sscc_range:
  start: <GS1-128 SSCC>
  end: <GS1-128 SSCC>
arn: <Amazon ARN, null if Ulta>

# --- Audit ---
draft_format: <EDI_856|VendorCentral_portal|both>
ready_to_send: <true|false>
notes: <free text — anything Operations or Order Ops needs to know before sending>
```

---

## Compliance check rules

If any of `pallet_build_pass`, `label_spec_pass`, `hazmat_pass`, `overage_pass`,
`ship_window_pass` is false, do not stage the ASN as `ready_to_send: true`.
Instead:

1. Open an exception in the Asana `Outbound — Retailer` section with the failed
   rule named
2. Set `compliance_fail` flag on the shipment row
3. Surface to Operations with the specific failure and the fix needed
4. Re-run the compliance check after the fix; only then mark ready

---

## Confirmation flow

1. Stage the YAML draft on the Asana parent task in `Outbound — Retailer`
2. Surface to Operations or Order Ops with the retailer, PO, ship date, line
   count, and compliance summary
3. On approval, the EDI 856 file or portal entry is prepared (out of skill
   scope to send — Operations or Order Ops clicks send)
4. After send, outlook-plm-bridge picks up the Sent Items confirmation and
   updates `shipments.asn_number` and `shipments.current_status`

---

## Send-window timing

Both Ulta and Amazon penalize late ASNs. Default rule: ASN must be transmitted
before the truck departs OC3PL. The skill stages the draft as soon as the ship
date and quantities are confirmed (typically 24-48 hours before truck pickup),
so the human review window is real, not panicked.

If the draft is staged inside 4 hours of pickup, mark `priority_send: true` in
notes so Operations or Order Ops sees urgency.
