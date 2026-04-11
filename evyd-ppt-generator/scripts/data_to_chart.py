"""
Data-to-Chart converter — transform CSV/Excel into chart slide JSON fragments.

Usage:
  python3 scripts/data_to_chart.py data.csv --type bar --title "Revenue Trend"
  python3 scripts/data_to_chart.py data.xlsx --sheet Sheet1 --type pie
  python3 scripts/data_to_chart.py data.csv --type bar --title "Q1" --summary

Input:  CSV or Excel file. First column = categories, remaining columns = series.
Output: JSON fragment (stdout) ready to paste into content.json slides array.
"""

import argparse, json, sys

try:
    import pandas as pd
except ImportError:
    print("Error: pandas is required. Install with: pip install pandas openpyxl",
          file=sys.stderr)
    sys.exit(1)


def load_data(path, sheet=None):
    """Load CSV or Excel into a DataFrame."""
    if path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(path, sheet_name=sheet or 0)
    return pd.read_csv(path)


def df_to_chart_json(df, chart_type, title, section='', background='white',
                     footnote='', summary=False):
    """Convert DataFrame to a chart slide JSON dict."""
    categories = [str(v) for v in df.iloc[:, 0].tolist()]
    series = []
    for col in df.columns[1:]:
        values = df[col].tolist()
        series.append({'name': str(col), 'values': values})

    slide = {
        'type': 'chart',
        'chart_type': chart_type,
        'title': title,
        'background': background,
        'categories': categories,
        'series': series,
    }
    if section:
        slide['section'] = section
    if footnote:
        slide['footnote'] = footnote

    if summary and len(series) > 0:
        stats = []
        for s in series:
            vals = [v for v in s['values'] if isinstance(v, (int, float))]
            if vals:
                stats.append(f"{s['name']}: min={min(vals)}, max={max(vals)}, "
                             f"mean={sum(vals)/len(vals):.1f}")
        if stats:
            slide['footnote'] = (footnote + '  |  ' if footnote else '') + \
                                '  |  '.join(stats)

    return slide


def main():
    parser = argparse.ArgumentParser(
        description='Convert CSV/Excel to chart slide JSON')
    parser.add_argument('data', help='Path to CSV or Excel file')
    parser.add_argument('--type', default='bar',
                        help='Chart type (bar/line/pie/area/radar/scatter/...)')
    parser.add_argument('--title', default='Chart', help='Slide title')
    parser.add_argument('--section', default='', help='Section label')
    parser.add_argument('--background', default='white',
                        choices=['blue', 'white'])
    parser.add_argument('--footnote', default='', help='Footnote text')
    parser.add_argument('--sheet', default=None, help='Excel sheet name')
    parser.add_argument('--summary', action='store_true',
                        help='Append min/max/mean stats to footnote')
    args = parser.parse_args()

    df = load_data(args.data, args.sheet)
    slide = df_to_chart_json(df, args.type, args.title, args.section,
                             args.background, args.footnote, args.summary)
    print(json.dumps(slide, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
