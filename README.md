# Finance Data to Excel

**Live app: [finance-data-to-excel.streamlit.app](https://finance-data-to-excel.streamlit.app/)**

A Python tool that pulls a public company's financial statements from Yahoo Finance,
computes twelve accounting ratios across every reported year, and presents them as a web
dashboard with trend charts and a downloadable Excel workbook.

Type a ticker, get the analysis. No installation required.

Built in Python, using an LLM for terminal workflows, library imports, and Markdown
documentation.

## What it shows

For any ticker, the app reports nine ratios grouped by what they measure:

| Tab | Ratios | Question it answers |
|---|---|---|
| Profitability | gross margin, operating margin, net margin | Does the business make money? |
| Liquidity | current ratio, quick ratio | Can it pay its near-term bills? |
| Leverage | debt-to-equity, interest coverage | How much debt, and can it service it? |
| Returns | return on equity, return on assets | How well does it use its capital? |

Each ratio appears as a card showing the current year's value and an arrow marking the
change from the prior year. Below the cards, a line chart plots the ratio across every
year Yahoo reports, and an expander lists any years where the figure could not be
computed.

The eleven raw figures behind the ratios (revenue, cost of revenue, operating income,
net income, current assets, current liabilities, inventory, total liabilities,
shareholder equity, total assets, interest expense) sit in a collapsible section at the
top.

## The four files

Each file has one job. The split means the accounting logic can be read and tested on
its own, and the front end can change without touching it.

```
FinancialsProject/
├── metrics.py          the accounting engine (no imports at all)
├── data.py             fetches statements from Yahoo Finance
├── export.py           builds the Excel workbook
├── app.py              the Streamlit web interface
├── requirements.txt
├── README.md
├── LICENSE             MIT
└── .gitignore
```

### `metrics.py`: the accounting engine

Twenty-one functions. Twelve compute an accounting figure or ratio; nine compute how a
ratio changed across years.

This file imports nothing. Every function takes plain numbers and returns a plain
number, so the math can be checked without a network connection, without pandas, and
without Streamlit installed.

Each dividing function guards its inputs before computing. If a value is missing, is
`NaN`, or would put a zero in the denominator, the function returns `None` rather than
raising:

```python
def grossMargin(revenue, cogs):
    if revenue == 0 or revenue == None or revenue != revenue or cogs == 0 or cogs == None or cogs != cogs:
        return None
    return (revenue - cogs) / revenue
```

The `revenue != revenue` test catches `NaN`, which is the only value in Python that is
not equal to itself. A `None` check alone will not catch it, because `NaN is not None`
evaluates to `True`.

The nine `*Delta` functions take a list of one ratio's values across years, drop the
entries that could not be computed, and return a dictionary of year-over-year changes
plus an overall change. Margins and returns report percentage change; the four multiples
report a raw difference. When fewer than two usable years remain, the function returns a
short string saying so instead of a dictionary.

**Run it on its own:**

```bash
python3 -c "from metrics import grossMargin; print(grossMargin(100, 60))"
```

### `data.py`: the fetch layer

Two live functions.

`precheck(statement, rowName, year)` pulls one cell out of a statement. yfinance returns
each statement as a pandas DataFrame indexed by line-item name with one column per
reporting year, so a single value needs both coordinates: `.loc` picks the row and
`.iloc[year]` picks the column. If the row is absent or the year is out of range,
`precheck` returns `None`.

`history(ticker)` fetches the income statement and the balance sheet, then builds one
dictionary per reporting year:

```python
{"ticker": "MSFT", "year": Timestamp("2026-06-30"),
 "revenue": 331839000000.0, "cogs": 106374000000.0, ...}
```

The list is ordered newest first, so `history("MSFT")[0]` is the most recent year.
Column counts vary by company and by statement, so the function takes the shorter of the
two and stops there.

Every field goes through `precheck` individually. A company missing one line item still
returns complete years for everything else it does report.

**Run it on its own:**

```bash
python3 -c "from data import history; h = history('MSFT'); print(len(h), 'years'); print(h[0])"
```

### `export.py`: the Excel writer

`buildWorkbook(years, ticker)` creates a workbook with one row per reporting year,
oldest first, and fifteen columns: the year, four raw figures, all nine ratios, and a
margin flag. Number formats are applied per column so currency displays with thousands
separators and margins display as percentages.

Raw numbers go into the cells and `number_format` controls how they appear. The values
stay sortable and summable in Excel instead of becoming text.

`workbookBytes(years, ticker)` returns the same workbook as bytes in memory. The web app
uses this, because Streamlit Cloud's filesystem does not persist between requests.

`marginFlag(gm)` classifies gross margin into bands: below 40% is `low`, 40% to 70% is
`medium`, above 70% is `high`, and a company with no reported cost of revenue gets `no
gross margin`.

**Run it on its own** to write one spreadsheet per ticker into the project folder:

```bash
python3 export.py
```

Edit the ticker list at the bottom of the file to change which companies it writes.

### `app.py`: the Streamlit interface

The web front end. Three helper functions sit at the top:

`fmt(value, kind)` turns a number into display text. Percent values get one decimal and a
`%`, multiples get two decimals and a `×`, currency gets a dollar sign. A missing value
becomes the string `N/A`.

`deltaOf(result, key, kind)` pulls one year-over-year change out of a `*Delta` result and
formats it with a sign. It returns `None` when there is not enough history, which tells
Streamlit to draw the card without an arrow.

`missingNote(series, years, label)` writes one caption describing which years a ratio
could not be computed for.

Below the helpers, the script reads the ticker from the sidebar, fetches the history,
computes all nine series, and renders the tabs.

**Run it locally:**

```bash
streamlit run app.py
```

This starts a local web server and opens a browser tab. The terminal stays occupied
until you stop the server with `Ctrl-C`.

## How the pieces connect

```
data.py  →  metrics.py  →  app.py     (numbers → ratios → screen)
                        →  export.py  (numbers → ratios → spreadsheet)
```

`data.py` produces numbers. `metrics.py` turns numbers into ratios. `app.py` and
`export.py` each present those ratios in their own format. Neither presentation layer
knows about the other, and `metrics.py` knows about neither.

One consequence worth noting: a missing value travels as `None` all the way through.
`fmt` turns it into `"N/A"` on screen, openpyxl leaves the spreadsheet cell blank, and
pandas reads it as a gap in the chart line. Each consumer renders it in its own idiom
without the others needing to agree on a format.

## Workflows

### Look up one company

Open the [live app](https://finance-data-to-excel.streamlit.app/), type a ticker in the
sidebar, read the tabs. Click the download button at the bottom for the spreadsheet.

### Run the dashboard locally

```bash
git clone https://github.com/Pieter-Darnaud/Finance-Data-to-Excel.git
cd Finance-Data-to-Excel
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
streamlit run app.py
```

On Windows, the activate line is `.venv\Scripts\activate`.

### Generate spreadsheets for several companies at once

With the environment set up as above:

```bash
python3 export.py
```

This writes `MSFT_financials.xlsx`, `AAPL_financials.xlsx`, `GOOGL_financials.xlsx`, and
`BAC_financials.xlsx`. Change the list at the bottom of `export.py` for different
companies.

### Use the ratio functions in your own code

`metrics.py` has no dependencies, so it can be copied into any project:

```python
from metrics import grossMargin, debtToEquity

print(grossMargin(331839000000, 106374000000))   # 0.679...
print(debtToEquity(315989000000, 442387000000))  # 0.714...
```

## Accounting formulas

| Function | Formula | What it measures |
|---|---|---|
| `cogs(bInventory, purchases, eInventory)` | beginning inventory + purchases − ending inventory | Cost of goods sold, derived from inventory flow |
| `grossProfit(revenue, cogs)` | revenue − COGS | What remains after the direct cost of the product |
| `opIncome(grossProfit, opex)` | gross profit − operating expenses | Profit from core operations, before interest and tax |
| `grossMargin(revenue, cogs)` | (revenue − COGS) / revenue | Share of each sales dollar surviving production cost |
| `opMargin(opIncome, revenue)` | operating income / revenue | Share surviving production and overhead |
| `netMargin(netIncome, revenue)` | net income / revenue | Share surviving every cost, including interest and tax |
| `currentRatio(currentAssets, currentLiabilities)` | current assets / current liabilities | Short-term solvency |
| `quickRatio(currentAssets, currentLiabilities, inventory)` | (current assets − inventory) / current liabilities | Solvency excluding stock that has to be sold first |
| `debtToEquity(totalLiabilities, shareholderEquity)` | total liabilities / equity | How much of the company is financed by borrowing |
| `returnOnEquity(netIncome, shareholderEquity)` | net income / equity | Return generated on owners' capital |
| `returnOnAssets(netIncome, totalAssets)` | net income / total assets | How productively assets generate profit |
| `interestCoverage(operatingIncome, interestExpense)` | operating income / interest expense | How many times over operating profit covers the interest bill |

Gross, operating, and net margin read as three checkpoints down the same income
statement. The gap between gross and operating shows what overhead costs; the gap between
operating and net shows what financing and tax cost.

## Companies that do not report every line

Not every company reports every figure, and the reasons are structural rather than
accidental.

A bank has no cost-of-revenue line, because it does not manufacture or buy the thing it
sells. It also does not split its balance sheet into current and non-current, so current
assets and current liabilities are absent too. A software company may report no
inventory. A debt-free company reports no interest expense.

The tool treats an absent figure as absent. It does not substitute zero, which would be
a different claim: a gross margin computed with zero cost of revenue comes out at 100%,
which would rank a bank as the most profitable company on the page.

So a bank shows real numbers for leverage and returns, `N/A` for the margin and liquidity
ratios, and a caption naming which ones are missing and why they could not be computed.

## Python concepts used

- Functions, one per accounting figure, with guards on their inputs
- Dictionaries and lists: a reporting year is a `dict`, a company's history is a `list`
- List comprehensions to compute one ratio across every year
- `for` loops and `if`/`elif`/`else` chains for the margin bands
- f-strings with format specifiers: `:.1%` for percentages, `:,.0f` for thousands
- `try`/`except` catching `KeyError` and `IndexError` on a missing statement row
- `None` as a sentinel for missing data, and the `x != x` test for `NaN`
- Modules and imports across four files, each importing only what it uses
- Third-party libraries: yfinance, pandas, openpyxl, Streamlit

## Requirements

Python 3.12 or newer.

```
yfinance      pulls the financial statements
openpyxl      writes the Excel workbook
pandas        the DataFrame the statements arrive in, and the chart data
streamlit     the web interface
```

Install them all with:

```bash
python3 -m pip install -r requirements.txt
```

## Built with

- [yfinance](https://pypi.org/project/yfinance/) for the financial data
- [openpyxl](https://pypi.org/project/openpyxl/) for the Excel output
- [pandas](https://pandas.pydata.org/) for the DataFrames and chart input
- [Streamlit](https://streamlit.io/) for the web interface and hosting

## Roadmap

- Compare several companies side by side
- Cache fetched data so a repeated ticker loads instantly
- Add a DuPont breakdown splitting return on equity into margin, asset turnover, and
  leverage
- Read tickers from a file or command-line argument
- Pull from SEC EDGAR filings instead of Yahoo Finance

## What I learned

In this project, I applied existing knowledge of accounting functions and terms to a new
area of learning for me in the python language, terminal commands, and Large Language
Model usage for formatting, description, and debugging. For this first iteration, I
focused on the three public companies of Apple, Microsoft, and Bank of America. The third
of these three was used to test a particular gross margin case. As I progressed through
the project, I realized the usefulness of terminal commands, and I plan to use many python
tools in the future via these commands. The f-string was crucial to me for making data
look a certain way, but I learned from the LLM that I was working with that I would need to
store real numbers as opposed to Strings in my text, keeping excel values useful, which
was helpful info. The gross margin formula was simplified to its core, using only the cost
of goods sold and total revenue values, which certainly made this first phase more
manageable for me.

For the second phase, I expanded from three hardcoded companies to any ticker a user types
in, and from one ratio to twelve. Bank of America, which I had originally used just to test
a gross margin edge case, ended up shaping the whole design. My first version substituted a
zero for its missing cost of revenue, which produced a 100% gross margin and made the bank
look like the most profitable company in the sheet. That taught me that a zero and a missing
value are two different facts, and that storing the missing one as `None` instead let every
part of the tool handle it in its own way: the web page shows "N/A", the spreadsheet cell
stays blank, and the chart draws a gap in the line. I also found out that missing data does
not always arrive the same way, since a line item that is absent entirely raises an error but
one that is present and empty returns NaN, which raises nothing and quietly spreads into
every number after it.
