"""Download and profile the unchanged UCI workbook. No cleaning is applied."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
import json
import shutil
import zipfile
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
URL = 'https://archive.ics.uci.edu/static/public/502/online%2Bretail%2Bii.zip'

def main():
    raw = ROOT / 'data/raw'
    raw.mkdir(parents=True, exist_ok=True)
    archive = raw / 'online_retail_ii.zip'
    workbook = raw / 'online_retail_II.xlsx'
    if not workbook.exists():
        if not archive.exists():
            with urlopen(URL, timeout=120) as response, archive.open('wb') as out:
                shutil.copyfileobj(response, out)
        with zipfile.ZipFile(archive) as z:
            names = [n for n in z.namelist() if n.endswith('online_retail_II.xlsx')]
            if len(names) != 1:
                raise ValueError('Expected exactly one source workbook')
            with z.open(names[0]) as source, workbook.open('wb') as out:
                shutil.copyfileobj(source, out)
    sheets = pd.read_excel(workbook, sheet_name=None, engine='openpyxl')
    frames = []
    sheet_stats = {}
    for name, frame in sheets.items():
        print(f'Loaded {name}: {len(frame):,} rows', flush=True)
        sheet_stats[name] = len(frame)
        frames.append(frame)
    df = pd.concat(frames, ignore_index=True)
    expected = ['Invoice', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'Price', 'Customer ID', 'Country']
    if df.columns.tolist() != expected:
        raise ValueError(f'Unexpected schema: {df.columns.tolist()}')
    cancelled = df.Invoice.astype(str).str.upper().str.startswith('C')
    positive = (~cancelled) & df.Quantity.gt(0) & df.Price.gt(0)
    counts = df.loc[positive & df['Customer ID'].notna()].groupby('Customer ID').Invoice.nunique()
    metrics = {
        'rows': len(df), 'distinct_invoice_ids': int(df.Invoice.nunique()),
        'distinct_customer_ids': int(df['Customer ID'].nunique()),
        'distinct_stock_codes': int(df.StockCode.nunique()),
        'countries': int(df.Country.nunique()),
        'cancellation_lines': int(cancelled.sum()),
        'cancellation_invoice_ids': int(df.loc[cancelled, 'Invoice'].nunique()),
        'negative_quantity_lines': int(df.Quantity.lt(0).sum()),
        'zero_quantity_lines': int(df.Quantity.eq(0).sum()),
        'negative_price_lines': int(df.Price.lt(0).sum()),
        'zero_price_lines': int(df.Price.eq(0).sum()),
        'exact_duplicate_excess_rows': int(df.duplicated().sum()),
        'missing_customer_id_lines': int(df['Customer ID'].isna().sum()),
        'preliminary_positive_purchase_lines': int(positive.sum()),
        'identified_customers_with_positive_purchases': len(counts),
        'identified_customers_with_two_or_more_positive_invoices': int(counts.ge(2).sum()),
    }
    report = {'source_url': URL, 'workbook_sha256': hashlib.sha256(workbook.read_bytes()).hexdigest(),
              'sheet_rows': sheet_stats, 'date_min': str(df.InvoiceDate.min()), 'date_max': str(df.InvoiceDate.max()),
              'metrics': metrics, 'missing_by_column': {k:int(v) for k,v in df.isna().sum().items()},
              'dtypes': {k:str(v) for k,v in df.dtypes.items()}}
    assert sum(sheet_stats.values()) == metrics['rows']
    assert metrics['identified_customers_with_two_or_more_positive_invoices'] <= len(counts)
    out = ROOT / 'reports'
    out.mkdir(exist_ok=True)
    (out/'profile.json').write_text(json.dumps(report, indent=2)+'\n')
    md = ['# Initial data-quality report', '', 'Generated from the unchanged source workbook by `scripts/profile_retail.py`. Counts describe invoice lines unless explicitly labeled otherwise. No rows removed.', '',
          f"Date coverage: {report['date_min']} to {report['date_max']}.", '', '## Workbook sheets', '', '| Sheet | Rows |', '|---|---:|']
    md += [f'| {k} | {v:,} |' for k,v in sheet_stats.items()]
    md += ['', '## Observed profile', '', '| Measure | Count |', '|---|---:|']
    md += [f"| {k.replace('_', ' ')} | {v:,} |" for k,v in metrics.items()]
    md += ['', '## Missing values', '', '| Column | Missing rows |', '|---|---:|']
    md += [f'| {k} | {v:,} |' for k,v in report['missing_by_column'].items()]
    md += ['', '## Decisions for the cleaning stage', '',
      '- Missing customer IDs can remain in eligible sales totals, but must be excluded from customer-level retention and segmentation. Report this coverage.',
      '- C-prefixed invoices are cancellations. Negative quantities and non-positive prices need separate classification; do not equate every negative line with a matched return.',
      '- Exact duplicate excess rows are review candidates, not proven errors. Establish a policy before removing them. No reliable source line ID exists.',
      '- Positive-purchase counts exclude C-prefixed invoices and require positive price and quantity. They are preliminary: no duplicate or non-merchandise-code policy has been applied.',
      '- The repeat-customer count establishes analytical feasibility; it is not a cohort retention rate. Use equal observation windows and exclude incomplete periods in later comparisons.',
      '- Historical transactions do not establish current market conditions, profit, ad ROI, causal campaign impact or full lifetime value.', '',
      'Source: [Chen, D. (2012), Online Retail II, UCI](https://doi.org/10.24432/C5CG6D), CC BY 4.0.', '',
      f"Workbook SHA-256: `{report['workbook_sha256']}`", '']
    (out/'data_quality_report.md').write_text('\n'.join(md))
    print(json.dumps(report, indent=2), flush=True)

if __name__ == '__main__':
    main()
