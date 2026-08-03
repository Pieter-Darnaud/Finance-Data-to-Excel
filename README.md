# Company Financials Analyzer

A Python tool that pulls public company financials from Yahoo Finance, computes gross
margin, classifies each company by margin band, and exports a formatted **Excel
dashboard**.

## What it does

For a set of tickers, the tool:

1. **Pulls** each company's income-statement figures (revenue and cost of revenue)
   from Yahoo Finance via `yfinance`.
2. **Computes** gross margin — `(revenue − COGS) / revenue`.
3. **Classifies** each company into a margin band:
   | Flag | Gross margin |
   |---|---|
   | `high` | ≥ 70% |
   | `medium` | 40% – 70% |
   | `low` | < 40% |
   | `no gross margin` | no cost of goods sold (e.g. banks) |

   *Note: these bands are absolute thresholds describing the raw margin, not
   industry-adjusted — a grocer's 25% reads as "low" here even though it's healthy for
   that sector. A future version would flag each company against its own history or
   industry (see [Roadmap](#roadmap)).*
4. **Exports** a styled `.xlsx` dashboard with numbers stored as real numbers and
   formatted for display.

## Example output

| Ticker | Revenue ($) | Cost of Goods Sold ($) | Gross Margin | Flag |
|---|---|---|---|---|
| MSFT | 331,839,000,000 | 106,374,000,000 | 67.9% | medium |
| BAC | 113,097,000,000 | — | N/A | no gross margin |
| AAPL | … | … | … | … |

(Data is pulled live from Yahoo Finance, so figures change over time.)

## How it works

### 1. Pulling data — `yfinance`

`yfinance` returns each statement as a table (a pandas DataFrame) indexed by line-item
name. A value is pulled by selecting the row label and the most recent column:

```python
import yfinance as yf

t = yf.Ticker("MSFT")
Mrevenue = t.financials.loc["Total Revenue"].iloc[0]
Mcogs    = t.financials.loc["Cost Of Revenue"].iloc[0]
```

### 2. Computing & classifying — core Python

Each metric is its own function. Companies with no cost of revenue (banks) would divide
to a meaningless margin, so those are caught and returned as `"N/A"`:

```python
def grossMargin(revenue, cogs):
    if cogs == 0:
        return "N/A"
    return (revenue - cogs) / revenue
```

Companies are stored as dictionaries and collected in a list:

```python
Microsoft     = {"ticker": "MSFT", "revenue": Mrevenue, "cogs": Mcogs}
BankOfAmerica = {"ticker": "BAC",  "revenue": Brevenue, "cogs": 0}
companies     = [Microsoft, BankOfAmerica, Apple]
```

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

`grossMargin` is the metric currently driving the dashboard; the others are building
blocks for expanding it.

## Python concepts used

- **Functions** — one per metric (`grossMargin`, `grossProfit`, `opMargin`)
- **Dictionaries & lists** — a company is a `dict`; the set of companies is a `list`
- **Loops & conditionals** — `for` over the companies, `if`/`elif`/`else` for the bands
- **f-strings** — formatted terminal output, e.g. `f"{ticker}: {gm:.2%}"`
- **Error handling** — `try`/`except` around a data pull to skip missing line items
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
python3 Financials.py
```

Prints a per-company summary to the terminal and writes **`FinancialsPuller.xlsx`** to
the project folder (open it in Numbers, Excel, or Google Sheets). To analyze different
companies, edit the tickers near the top of `Financials.py`.

## Project structure

```
FinancialsProject/
├── Financials.py       # the whole tool: fetch → compute → export
├── requirements.txt    # dependencies (yfinance, openpyxl)
├── README.md
└── .gitignore
```

## Built with

- **[yfinance](https://pypi.org/project/yfinance/)** — pulls the financial data
- **[openpyxl](https://pypi.org/project/openpyxl/)** — writes the Excel dashboard
- **pandas** — the DataFrame the financial data arrives in (installed with yfinance)

## Roadmap

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
