import openpyxl as opx
from io import BytesIO

from metrics import (grossMargin, opMargin, netMargin,
                     currentRatio, quickRatio, debtToEquity,
                     returnOnEquity, returnOnAssets, interestCoverage)

low = 0.4

medium = 0.7

CURRENCY = "#,##0"
PERCENT = "0.0%"
MULTIPLE = "0.00"


def marginFlag(gm):
    if gm is None:
        return "no gross margin"
    if gm < low:
        return "low"
    if gm < medium:
        return "medium"
    return "high"


HEADERS = ["Year", "Revenue ($)", "Cost of Goods Sold ($)", "Operating Income ($)",
           "Net Income ($)", "Gross Margin", "Operating Margin", "Net Margin",
           "Current Ratio", "Quick Ratio", "Debt to Equity", "Return on Equity",
           "Return on Assets", "Interest Coverage", "Flag"]

FORMATS = [None, CURRENCY, CURRENCY, CURRENCY, CURRENCY,
           PERCENT, PERCENT, PERCENT,
           MULTIPLE, MULTIPLE, MULTIPLE,
           PERCENT, PERCENT, MULTIPLE, None]


def buildWorkbook(years, ticker):
    w = opx.Workbook()
    ws = w.active
    ws.title = ticker

    for col, header in enumerate(HEADERS, start=1):
        ws.cell(row=1, column=col, value=header)

    # oldest year first, so the sheet reads left-to-right like the charts
    for r, y in enumerate(reversed(years), start=2):
        gm = grossMargin(y["revenue"], y["cogs"])
        values = [
            y["year"].year,
            y["revenue"],
            y["cogs"],
            y["operatingIncome"],
            y["netIncome"],
            gm,
            opMargin(y["operatingIncome"], y["revenue"]),
            netMargin(y["netIncome"], y["revenue"]),
            currentRatio(y["currentAssets"], y["currentLiabilities"]),
            quickRatio(y["currentAssets"], y["currentLiabilities"], y["inventory"]),
            debtToEquity(y["totalLiabilities"], y["shareholderEquity"]),
            returnOnEquity(y["netIncome"], y["shareholderEquity"]),
            returnOnAssets(y["netIncome"], y["totalAssets"]),
            interestCoverage(y["operatingIncome"], y["interestExpense"]),
            marginFlag(gm),
        ]
        for col, (value, fmt) in enumerate(zip(values, FORMATS), start=1):
            cell = ws.cell(row=r, column=col, value=value)
            if fmt is not None and value is not None:
                cell.number_format = fmt

    for col in range(1, len(HEADERS) + 1):
        ws.column_dimensions[ws.cell(row=1, column=col).column_letter].width = 22

    return w


def workbookBytes(years, ticker):
    """Return the .xlsx as bytes, for st.download_button — nothing touches disk."""
    buffer = BytesIO()
    buildWorkbook(years, ticker).save(buffer)
    return buffer.getvalue()


if __name__ == "__main__":
    from data import history
    for tk in ["MSFT", "AAPL", "GOOGL", "BAC"]:
        buildWorkbook(history(tk), tk).save(f"{tk}_financials.xlsx")
        print(f"wrote {tk}_financials.xlsx")
