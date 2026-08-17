# Finance Data to Excel

A Python tool that pulls public company financials from Yahoo Finance, computes gross
margin, classifies each company by margin band, and exports a formatted **Excel
dashboard**.

## What it does

For a set of tickers, the tool:

1. **Pulls** each company's income-statement figures (revenue and cost of revenue)
   from Yahoo Finance via `yfinance`.
2. **Screens out** companies that don't report a cost of revenue — see
   [Handling companies without a COGS line](#handling-companies-without-a-cogs-line).
3. **Computes** gross margin — `(revenue − COGS) / revenue`.
4. **Classifies** each company into a margin band:
   | Flag | Gross margin |
   |---|---|
   | `high` | ≥ 70% |
   | `medium` | 40% – 70% |
   | `low` | < 40% |

   *Note: these bands are absolute thresholds describing the raw margin, not
   industry-adjusted — a grocer's 25% reads as "low" here even though it's healthy for
   that sector. A future version would flag each company against its own history or
   industry (see [Roadmap](#roadmap)).*
5. **Exports** a styled `.xlsx` dashboard with numbers stored as real numbers and
   formatted for display.

## Example output

Running the tool for `["MSFT", "AAPL", "GOOGL", "BAC"]` prints:

```
  skipping BAC: no 'Cost Of Revenue' line
```

and writes:

| Ticker | Revenue ($) | Cost of Goods Sold ($) | Gross Margin | Flag |
|---|---|---|---|---|
| MSFT | 331,839,000,000 | 106,374,000,000 | 67.9% | medium |
| AAPL | 416,161,000,000 | 220,960,000,000 | 46.9% | medium |
| GOOGL | 402,836,000,000 | 162,535,000,000 | 59.7% | medium |

Four tickers went in; three rows came out. Bank of America is reported on the terminal
and left out of the sheet — that's the screening step, explained below.

(Data is pulled live from Yahoo Finance, so figures change over time.)

## Handling companies without a COGS line

Gross margin needs a cost of revenue, and **not every company reports one.** Banks are
the clearest example: Bank of America's income statement has no cost-of-revenue line
at all, because a bank doesn't manufacture or buy the thing it sells. Interest expense
isn't the same concept, so there's no honest substitute to drop in.

That absence is a real fact about the data, and the tool is built to notice it rather
than paper over it. Two details matter:

**A missing row raises, it doesn't return blank.** Asking pandas for a row label that
isn't there throws a `KeyError` — it doesn't hand back `None` or zero. So the lookup is
wrapped in a `try`, and the failure is converted into a value the rest of the program
can act on:

```python
def get_financials(companyTicker):
    try:
        company = yf.Ticker(companyTicker).financials
        return {"ticker":  companyTicker,
                "revenue": company.loc["Total Revenue"].iloc[0],
                "cogs":    company.loc["Cost Of Revenue"].iloc[0]}
    except KeyError as e:
        print(f"  skipping {companyTicker}: no {e} line")
        return None
```

**`None` is the signal to skip.** The company builder calls the fetch for each ticker
and keeps only the ones that came back with data, so a company with no COGS never
reaches the margin calculation:

```python
companies = []

def companyChecker(sCompanies):
    for i in sCompanies:
        if get_financials(i) != None:
            companies.append(get_financials(i))

companyChecker(["MSFT", "AAPL", "GOOGL", "BAC"])
```

The alternative — substituting `0` for the missing COGS — was tried first and rejected.
It computes to a **100% gross margin**, which would flag a bank as the most profitable
company in the sheet. Zero and "not reported" are different facts, and only one of them
is true here.

The trade-off in the current approach is that a screened company disappears from the
output entirely. Showing it with a blank margin and a `no gross margin` label would be
more informative, and that requires guarding each field independently rather than
failing the whole fetch — see the [Roadmap](#roadmap).

## How it works

### 1. Pulling data — `yfinance`

`yfinance` returns each statement as a table (a pandas DataFrame) indexed by line-item
name, with one column per reporting year. A single value needs **both** coordinates —
`.loc` picks the row label, `.iloc[0]` picks the most recent year:

```python
import yfinance as yf

t = yf.Ticker("MSFT")
revenue = t.financials.loc["Total Revenue"].iloc[0]   # 331,839,000,000
```

Without `.iloc[0]` the result is the whole row — four years of figures — rather than one
number, which is a subtle way to end up with the wrong type flowing downstream.

### 2. Computing & classifying — core Python

Each metric is its own function. Every ratio guards its denominator — dividing by zero
would raise rather than return a number — and returns `"N/A"` when it can't compute:

```python
def grossMargin(revenue, cogs):
    if revenue == 0:
        return "N/A"
    return (revenue - cogs) / revenue
```

A company is stored as a **dictionary** and the set of companies as a **list of
dictionaries** — one row of the eventual spreadsheet per entry:

```python
{"ticker": "MSFT", "revenue": 331839000000.0, "cogs": 106374000000.0}
```

Named keys rather than positions, so adding a field later (net income, total assets)
doesn't shift anything already being read. `get_financials` returns this shape directly,
so the list is built by calling it per ticker rather than assembling dictionaries by
hand.

A loop classifies each one into a margin band:

```python
for i in companies:
    if grossMargin(i["revenue"], i["cogs"]) == "N/A":
        flag = "no gross margin"
    elif grossMargin(i["revenue"], i["cogs"]) < 0.4:
        flag = "low"
    elif 0.4 <= grossMargin(i["revenue"], i["cogs"]) < 0.7:
        flag = "medium"
    else:
        flag = "high"
```

### 3. Exporting to Excel — `openpyxl` + formatting

A workbook is created, a header row written, then one row per company. Crucially, the
**raw numbers** are written to the cells and `number_format` controls how they *display*
— so the values stay sortable/summable in Excel instead of becoming text:

```python
import openpyxl as opx

w  = opx.Workbook()
ws = w.active
ws["A1"] = "Ticker"; ws["B1"] = "Revenue ($)"
ws["C1"] = "Cost of Goods Sold ($)"; ws["D1"] = "Gross Margin"; ws["E1"] = "Flag"

for i in range(len(companies)):
    ws["A" + str(i + 2)] = companies[i]["ticker"]
    ws["B" + str(i + 2)] = companies[i]["revenue"]
    ws["B" + str(i + 2)].number_format = "#,##0"        # 331,839,000,000
    ws["D" + str(i + 2)] = grossMargin(companies[i]["revenue"], companies[i]["cogs"])
    ws["D" + str(i + 2)].number_format = "0.0%"         # 0.679 → 67.9%

w.save("FinancialsPuller.xlsx")
```

## Accounting formulas

Each ratio and figure is defined as its own function mirroring a standard accounting
method:

| Function | Formula | What it represents |
|---|---|---|
| `cogs(bInventory, purchases, eInventory)` | beginning inventory + purchases − ending inventory | **Cost of Goods Sold** — the direct cost of the inventory actually sold in the period |
| `grossProfit(revenue, cogs)` | revenue − COGS | **Gross Profit** — what remains after the direct cost of making the product |
| `opIncome(grossProfit, opex)` | gross profit − operating expenses | **Operating Income** — profit from core operations, before interest and tax |
| `grossMargin(revenue, cogs)` | (revenue − COGS) / revenue | **Gross Margin** — gross profit as a share of revenue (the tool's main metric) |
| `opMargin(opIncome, revenue)` | operating income / revenue | **Operating Margin** — operating income as a share of revenue |
| `netMargin(netIncome, revenue)` | net income / revenue | **Net Margin** — profit as a share of revenue, after every cost |
| `currentRatio(currentAssets, currentLiabilities)` | current assets / current liabilities | **Current Ratio** — short-term solvency |
| `quickRatio(currentAssets, currentLiabilities, inventory)` | (current assets − inventory) / current liabilities | **Quick Ratio** — the stricter liquidity test, excluding stock |
| `debtToEquity(totalLiabilities, shareholderEquity)` | total liabilities / equity | **Debt-to-Equity** — capital structure risk |
| `returnOnEquity(netIncome, shareholderEquity)` | net income / equity | **ROE** — return generated on owners' capital |
| `returnOnAssets(netIncome, totalAssets)` | net income / total assets | **ROA** — how productively assets generate profit |
| `interestCoverage(operatingIncome, interestExpense)` | operating income / interest expense | **Interest Coverage** — how comfortably debt costs are covered |

`grossMargin` is the metric currently driving the dashboard. The liquidity, leverage, and
return ratios are built and ready for the next iteration, which adds balance-sheet data
(`.balance_sheet`) alongside the income statement.

## Python concepts used

- **Functions** — one per metric (`grossMargin`, `grossProfit`, `opMargin`)
- **Dictionaries & lists** — a company is a `dict`; the set of companies is a `list`
- **Loops & conditionals** — `for` over the companies, `if`/`elif`/`else` for the bands
- **f-strings** — formatted terminal output, e.g. `f"{ticker}: {gm:.2%}"`
- **Error handling** — a `try`/`except` in `get_financials()` catches a missing line
  item (`KeyError`) and skips the company instead of crashing
- **Modules & imports** — the tool is split across four files that import from each
  other, so each layer has one job and can change independently
- **Third-party libraries** — `yfinance` (data), `openpyxl` (Excel)

## Setup

Requires Python 3.12+.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python3 export.py
```

Writes **`FinancialsPuller.xlsx`** to the project folder (open it in Numbers, Excel, or
Google Sheets). To analyze different companies, edit the tickers near the top of
`data.py`.

## Project structure

```
FinancialsProject/
├── metrics.py          # the accounting engine — pure Python, no library imports
├── data.py             # pulls financials from Yahoo Finance (yfinance)
├── export.py           # writes the styled Excel dashboard (openpyxl); entry point
├── app.py              # reserved for the planned Streamlit front-end
├── requirements.txt    # dependencies (yfinance, openpyxl)
├── README.md
├── LICENSE             # MIT
└── .gitignore
```

The three layers are deliberately separate: **input** (`data.py`), **brain**
(`metrics.py`), **output** (`export.py`). `metrics.py` imports nothing at all, so the
accounting logic can be read, run, and tested without any third-party library installed
— and swapping the front-end later (Excel today, Streamlit next) never touches it.

## Built with

- **[yfinance](https://pypi.org/project/yfinance/)** — pulls the financial data
- **[openpyxl](https://pypi.org/project/openpyxl/)** — writes the Excel dashboard
- **pandas** — the DataFrame the financial data arrives in (installed with yfinance)

## Roadmap

- Show screened companies in the sheet with a blank margin and a `no gross margin`
  label, instead of omitting them — needs per-field error handling rather than
  failing the whole fetch
- Add an operating margin column
- Flag margin **trend** year-over-year (a company vs. its own history)
- Read tickers from a file or command-line argument instead of hardcoding
- A simple web front-end (Streamlit) to analyze any ticker on demand

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
