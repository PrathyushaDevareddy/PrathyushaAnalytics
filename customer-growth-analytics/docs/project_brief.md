# Business brief

## Objective

Investigate sales and repeat-purchase opportunities for a hypothetical retail leadership team using historical public data. The scenario is a portfolio exercise; no business deterioration or improvement is assumed.

| Stakeholder | Decision supported |
|---|---|
| Commercial manager | Product and customer priorities |
| CRM manager | Candidate loyalty/reactivation audiences |
| BI team | Consistent definitions and trustworthy totals |

## Initial scope

Download and profile UCI Online Retail II. Describe the invoice-line grain, identifiers, date coverage, missingness, duplicates, cancellation flags and unusual quantities/prices. Preserve all raw records. Defer cleaning decisions to the next milestone.

## Acceptance criteria for steps 1–2

- Existing portfolio remains accessible and links to the new project.
- Source workbook downloads from its documented provider.
- Every sheet is included; sheet row counts reconcile to the combined count.
- Report and JSON profile derive from runnable code, not hardcoded findings.
- Data dictionary explains actual source headers and planned standardized names.
- Missing IDs, repeated rows and cancellation candidates are quantified.
- Raw data stays unchanged, with checksum and attribution recorded.

## Future user stories

- As a commercial manager, I want monthly sales under a stated cancellation policy so I can compare periods fairly.
- As a CRM manager, I want customer cohorts with equal observation windows so I can choose audiences using comparable behavior.
- As a report user, I want totals that reconcile to documented eligible source rows so I can trust the dashboard.

## Metric decisions still required

Define eligible merchandise lines; distinguish adjustments from purchases; decide whether exact duplicate rows are errors; define an order key; reconcile cancellations; establish full-period cutoffs. Observed customer spend must not be labeled full lifetime value. RFM scores describe historical behavior, not predictions of campaign response.
