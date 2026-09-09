# Customer Growth & Revenue Analytics

A portfolio case study exploring sales, repeat purchases and customer segments, followed by separate digital-analytics and CRM exercises.

## Current milestone

Repository setup and initial source-data profiling. The pipeline downloads and profiles the unchanged UCI Online Retail II workbook. Business findings, cleaning models and dashboards are future stages.

## Business questions

- Which products and customers contribute to sales?
- How do cancellations affect reported transaction value?
- Which customer groups return, and which might warrant a reactivation test?
- How should the business measure retention using comparable observation windows?

## Start here

- [Business scope and acceptance criteria](docs/project_brief.md)
- [Source data dictionary](docs/data_dictionary.md)
- [Actual data-quality findings](reports/data_quality_report.md)
- [Machine-readable profile](reports/profile.json)
- [Reproducible download and profiling code](scripts/profile_retail.py)

## Reproduce

From this project directory, with Python 3.11 or newer:

```sh
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/profile_retail.py
```

The script downloads the archive from UCI, preserves the workbook in `data/raw`, reads both sheets, and writes the two reports. Reading over a million Excel rows can take several minutes. Raw files are excluded from Git; the source URL, attribution and file checksum make the analysis reproducible.

## Roadmap

1. Completed: source retrieval, raw-data profiling and project documentation.
2. Next: decide cleaning policies, normalize identifiers, and prepare SQL tables.
3. Sales and customer analysis using SQL and Python.
4. Power BI dashboard and executive recommendations; setup deferred until this stage.
5. Separate GA4/BigQuery website-funnel module.
6. Separate fictional CRM practice exercise, subject to platform access.

The retail and GA4 samples represent different businesses and will not be joined. Ad spend, product cost and randomized experiment data are not available in the initial retail source. No profit, CAC, ROAS or causal uplift is claimed.

## Source and attribution

Chen, D. (2012). [Online Retail II](https://doi.org/10.24432/C5CG6D). UCI Machine Learning Repository. Dataset licensed CC BY 4.0. This is historical UK retail data, including wholesale customers; it is not a current US market sample. Identifiers are supplied by the public dataset. This project is independent of the data provider.
