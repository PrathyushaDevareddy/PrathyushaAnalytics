# Source data dictionary

Grain: one source invoice line. An invoice may have multiple rows. No unique line identifier is provided. Keep original sheet and row number as provenance when creating cleaned tables.

| Source header | Proposed SQL name | Meaning / handling |
|---|---|---|
| Invoice | invoice_id | Identifier; preserve as text. C prefix marks cancellation. Not unique per row. |
| StockCode | stock_code | Product or special item code; preserve text and inspect non-merchandise codes. |
| Description | description | Item description; may be missing or vary for one code. |
| Quantity | quantity | Signed line quantity. Negative/zero values need classification. |
| InvoiceDate | invoice_at | Source transaction timestamp; timezone not specified. |
| Price | unit_price_gbp | Unit price in sterling. Negative/zero values need classification. |
| Customer ID | customer_id | Customer identifier; nullable. Excel numeric inference does not make this a measure. |
| Country | country | Customer country as recorded; standardize only with an explicit mapping. |

Proposed derived fields for the next stage: `line_value_gbp = quantity * unit_price_gbp`, `is_cancellation`, `has_customer_id`, and source provenance. Use decimal-aware money calculations for final reporting. None are source-provided profitability measures.

Relationships to validate: invoice-to-customer consistency, invoice-to-date consistency, stock-code-to-description variation. Treat exact matches across all eight source columns as duplicate candidates until a policy is documented.

Source definitions: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii). The downloaded workbook uses the original headers above rather than the normalized labels shown in some source documentation.
