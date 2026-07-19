# Routing request — staged write

Use this form when staging a routing request to a retailer DC. Routing
requests are the upstream of the ASN — the retailer assigns a carrier and a
dock appointment based on origin, destination, weight, and pallet count.

For Ulta UBM: routing comes back as an LTL provider plus a delivery window.
For Amazon: typically Partnered Carrier or a SCAC per PO. Either way, the
retailer drives the assignment; SJS does not self-route.

---

## Form fields

```yaml
shipment_id: <FK to shipments.id>
retailer: <Ulta|Amazon|Sephora>
retailer_po: <retailer's PO number>
origin: <OC3PL site address, full>
destination_dc: <retailer DC code or name>
ready_to_ship_date: <YYYY-MM-DD, day goods are pallet-built and ready>

# --- Shipment dimensions ---
total_cases: <int>
total_pallets: <int>
total_weight_lb: <decimal>
hazmat_present: <true|false>
hazmat_class_list: <array of UN classes, empty if none>

# --- Request channel ---
request_method: <retailer_portal|email>
portal_name: <Ulta vendor portal|Amazon Vendor Central|other, null if email>
recipient_email: <email address, null if portal>

# --- Draft body ---
draft_subject: <one-line subject for email or portal entry>
draft_body: <plain text body — see template below>

# --- Audit ---
ready_to_send: <true|false>
notes: <free text>
```

---

## Draft body template

Used for email-based routing requests (Ulta sometimes accepts email; Amazon
prefers portal). Keep tight, factual, no flourish.

```
Subject: Routing request — [Retailer PO #] — Sweet July Skin

Routing request for Sweet July Skin under PO [retailer_po].

Ready to ship: [ready_to_ship_date]
Origin: [OC3PL site name and address]
Destination: [destination_dc]

Total cases: [total_cases]
Total pallets: [total_pallets]
Total weight: [total_weight_lb] lb
Hazmat: [yes/no, list classes if yes]

Please advise routing and pickup window.

Thanks,
[Sender name]
Sweet July Skin Operations
```

---

## Confirmation flow

1. Stage the YAML on the Asana parent task in `Outbound — Retailer`
2. Surface to Operations or Order Ops with the retailer, PO, ready date,
   dimensions
3. On approval, draft body is finalized and either:
   - Pasted into the retailer portal by Operations or Order Ops, or
   - Emailed from the Operations mailbox to the retailer routing contact
4. outlook-plm-bridge logs the send back to the shipment record on Sent Items
   capture
5. Once routing comes back from the retailer, log the assigned carrier, SCAC,
   and pickup window in the shipment record (use a fresh shipment-record
   update form for the carrier and pickup fields)

---

## Lead time guidance

Default lead times for retailer routing response (tunable via
`settings.lm_routing_request_lead_*`):

- Ulta: 2-3 business days from request submission
- Amazon: 1-2 business days
- Sephora: TBD when channel opens

Submit the routing request that many days before the ready_to_ship_date to
avoid panic loops. If the shipment ready date is inside the lead time, mark
`priority_send: true` in notes.
