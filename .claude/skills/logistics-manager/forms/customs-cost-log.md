# Customs cost log — staged write

Use this form when broker invoices land for an Asia-origin shipment. Logs duty,
brokerage fee, and (when not already captured) freight against the shipment
record so landed COGS rolls up cleanly.

Most invoices come in two waves: (1) an early customs entry summary with HTS
codes and duty calc, (2) a final broker invoice with brokerage fee and any
fees billed later (ISF, exam fee, demurrage if applicable). Stage one form per
invoice; the shipment row accumulates.

---

## Form fields

```yaml
shipment_id: <FK to shipments.id>
broker: <Flexport|other broker name>
invoice_reference: <broker invoice number>
invoice_date: <YYYY-MM-DD>

# --- Customs entry detail ---
customs_entry_number: <broker-assigned entry number, null if not yet assigned>
hts_codes:
  - code: <HTS code>
    description: <plain language>
    qty: <int>
    declared_value: <decimal USD>
    duty_rate: <percentage as decimal, e.g., 0.053>
    duty_amount: <decimal USD>
    section_301_rate: <decimal, e.g., 0.075 or 0.25, null if not applicable>
    section_301_amount: <decimal USD, null if not applicable>

# --- Cost lines ---
duty_paid: <decimal USD, sum of duty_amount + section_301_amount across lines>
brokerage_fee: <decimal USD>
freight_paid: <decimal USD, may be on the same or separate invoice>
other_fees:
  - fee_type: <isf|exam|demurrage|chassis|other>
    fee_amount: <decimal USD>
    note: <free text>

# --- Total ---
landed_cost_line_delta: <decimal USD — what to add to shipments.landed_cost_line>
landed_cost_line_after: <decimal USD — running total after this entry>

# --- Audit ---
source_email_id: <Outlook message ID via outlook-plm-bridge>
source_pdf_path: <SharePoint path to invoice PDF, null if not yet filed>
notes: <free text>
```

---

## HTS code handling

If the shipment carries one HTS code, store it on `shipments.hts_code_ref`. If
the shipment carries multiple HTS codes (common for mixed component
shipments — caps under one code, jars under another), store `"see multi_hts"`
on `hts_code_ref` and the full array on `shipments.multi_hts` jsonb.

The form here always captures the full per-line breakdown so the per-SKU
landed cost can be computed downstream — purchasing-manager and sjs-margin-
architect both depend on it.

---

## Confirmation flow

1. Stage the YAML on the Asana parent task in `Customs Watch`
2. Surface to Operations with the broker, invoice number, total customs cost,
   and running landed cost
3. On approval, plm-assistant updates `shipments.duty_paid`,
   `shipments.brokerage_fee`, `shipments.freight_paid` (additive), appends to
   `shipments.multi_hts` if multi-line, and recomputes
   `shipments.landed_cost_line`
4. Source PDF gets filed to SharePoint under the logistics customs folder
5. Surface the landed cost delta to purchasing-manager so the per-SKU cost
   feeds back into the vendor scorecard

---

## When customs hold or exam adds cost

Examination fees, ISF fines, and demurrage all show up in `other_fees`. Each
gets a line with `fee_type` and a note explaining why. These costs feed into
the lane's vendor scorecard differently than baseline duty:

- Baseline duty is the cost of doing business — not vendor-attributable
- ISF fines, exam fees, demurrage are typically operational misses — flag to
  purchasing-manager so the vendor scorecard captures the pattern

---

## Closing the customs status

When the final broker invoice lands and customs is fully cleared, update
`shipments.customs_status = 'cleared'` in the same staged write. This is the
event that fully closes the customs portion of the lane.
