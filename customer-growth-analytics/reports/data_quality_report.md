# Initial data-quality report

Generated from the unchanged source workbook by `scripts/profile_retail.py`. Counts describe invoice lines unless explicitly labeled otherwise. No rows removed.

Date coverage: 2009-12-01 07:45:00 to 2011-12-09 12:50:00.

## Workbook sheets

| Sheet | Rows |
|---|---:|
| Year 2009-2010 | 525,461 |
| Year 2010-2011 | 541,910 |

## Observed profile

| Measure | Count |
|---|---:|
| rows | 1,067,371 |
| distinct invoice ids | 53,628 |
| distinct customer ids | 5,942 |
| distinct stock codes | 5,305 |
| countries | 43 |
| cancellation lines | 19,494 |
| cancellation invoice ids | 8,292 |
| negative quantity lines | 22,950 |
| zero quantity lines | 0 |
| negative price lines | 5 |
| zero price lines | 6,202 |
| exact duplicate excess rows | 34,335 |
| missing customer id lines | 243,007 |
| preliminary positive purchase lines | 1,041,670 |
| identified customers with positive purchases | 5,878 |
| identified customers with two or more positive invoices | 4,255 |

## Missing values

| Column | Missing rows |
|---|---:|
| Invoice | 0 |
| StockCode | 0 |
| Description | 4,382 |
| Quantity | 0 |
| InvoiceDate | 0 |
| Price | 0 |
| Customer ID | 243,007 |
| Country | 0 |

## Decisions for the cleaning stage

- Missing customer IDs can remain in eligible sales totals, but must be excluded from customer-level retention and segmentation. Report this coverage.
- C-prefixed invoices are cancellations. Negative quantities and non-positive prices need separate classification; do not equate every negative line with a matched return.
- Exact duplicate excess rows are review candidates, not proven errors. Establish a policy before removing them. No reliable source line ID exists.
- Positive-purchase counts exclude C-prefixed invoices and require positive price and quantity. They are preliminary: no duplicate or non-merchandise-code policy has been applied.
- The repeat-customer count establishes analytical feasibility; it is not a cohort retention rate. Use equal observation windows and exclude incomplete periods in later comparisons.
- Historical transactions do not establish current market conditions, profit, ad ROI, causal campaign impact or full lifetime value.

Source: [Chen, D. (2012), Online Retail II, UCI](https://doi.org/10.24432/C5CG6D), CC BY 4.0.

Workbook SHA-256: `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`
