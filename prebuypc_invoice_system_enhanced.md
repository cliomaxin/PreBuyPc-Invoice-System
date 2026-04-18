# PreBuyPc Consultancy --- Invoice System Plan (Enhanced)

## Overview

A Django-based invoicing system for PreBuyPc consultancy services. You
capture client details, service line items, and payment activity. The
system generates a clean, mobile-responsive invoice with accurate
financial records and shareable access.

## User Flow

1.  Create a new invoice\
2.  Select or create client\
3.  Add line items with notes, quantity, and pricing\
4.  System calculates totals and locks them on save\
5.  View invoice in styled HTML\
6.  Share via secure public link\
7.  Record payments manually\
8.  Track status automatically

## Client Model

-   name\
-   email\
-   phone\
-   company_name\
-   billing_address\
-   kra_pin\
-   notes\
-   created_at\
-   updated_at

## Invoice Model

-   invoice_number\
-   client\
-   currency (default KES)\
-   date_issued\
-   due_date\
-   status (draft, sent, paid, overdue, cancelled, refunded)\
-   tax_rate\
-   discount\
-   subtotal (stored)\
-   tax_amount (stored)\
-   grand_total (stored)\
-   paid_at\
-   notes\
-   public_token\
-   is_active\
-   created_at\
-   updated_at

## InvoiceItem Model

-   invoice\
-   service_category\
-   detail_notes\
-   quantity (\>0)\
-   unit_price\
-   total (stored)

## Payment Model

-   invoice\
-   amount\
-   method (mpesa, cash, bank)\
-   reference\
-   phone\
-   created_at

## Invoice Integrity Rules

-   Totals stored on save\
-   No recalculation after save\
-   Historical accuracy preserved

## Status Logic

-   draft\
-   sent\
-   paid\
-   overdue\
-   cancelled\
-   refunded

Rules: - If due date passes and unpaid → overdue\
- If total payments \>= grand total → paid

## Payment Handling

-   Manual entry only\
-   Supports partial payments\
-   Tracks multiple payments\
-   Stores M-Pesa reference codes\
-   No API integration

## Validation Rules

-   Quantity \> 0\
-   Price \>= 0\
-   At least one item required\
-   Payment cannot exceed balance\
-   M-Pesa requires reference\
-   No duplicate references

## Sharing

-   Public URL via UUID\
-   No login required

## Export Options

-   Print\
-   PDF\
-   Image (PNG)\
-   WhatsApp sharing

## UI Features

-   Client autocomplete\
-   Saved service templates\
-   Duplicate invoice\
-   Live total preview

## Performance

-   Index invoice_number\
-   Index client\
-   Index status

## Security

-   CSRF protection\
-   Input validation\
-   UUID public links

## Reporting

-   Monthly revenue\
-   Outstanding payments\
-   Paid vs unpaid\
-   Top services\
-   Repeat clients

## Audit

-   Track created_by\
-   Track updated_by\
-   Timestamps

## Branding

-   Terms and conditions\
-   Business info\
-   Signature support

## Future Expansion

-   Multi-user\
-   Organization model\
-   Role system

## Build Phases

### Phase 1

-   Models\
-   Stored totals\
-   Invoice creation\
-   Share link

### Phase 2

-   Payment model\
-   Manual M-Pesa tracking\
-   PDF and image export

### Phase 3

-   Dashboard\
-   Reports\
-   Scaling features
