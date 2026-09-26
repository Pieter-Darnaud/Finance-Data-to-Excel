import streamlit as s

import pandas as p

import yfinance as yf


from metrics import grossMargin, currentRatio, netMargin, opMargin, quickRatio, debtToEquity, returnOnEquity, returnOnAssets, interestCoverage

from metrics import (grossMarginDelta, opMarginDelta, netMarginDelta,
                     currentRatioDelta, quickRatioDelta, debtToEquityDelta,
                     returnOnEquityDelta, returnOnAssetsDelta, interestCoverageDelta)

from data import history

from export import workbookBytes


def fmt(value, kind):
    if value == "N/A":
        return "N/A"
    if value != value or value == None:
        return "N/A"
    if kind == "percent":
        return f"{value:.1%}"
    if kind == "multiple":
        return f"{value:.2f}×"
    if kind == "currency":
        return f"${value:.2f}"


def deltaOf(result, key, kind):
    if not isinstance(result, dict):
        return None
    v = result.get(key)
    if v is None:
        return None
    if kind == "percent":
        return f"{v:+.1%}"
    return f"{v:+.2f}"

def missingNote(series, years, label):
    missing = [years[i]["year"].year for i in range(len(series)) if series[i] is None]
    if len(missing) == 0:
        s.caption(f"{label}: reported every year")
    elif len(missing) == len(series):
        s.caption(f"{label}: not reported by this company")
    elif len(missing) == 1:
        s.caption(f"{label}: no data for {missing[0]}")
    else:
        s.caption(f"{label}: no data for " + ", ".join(str(y) for y in missing))



s.title("Finance Data to Excel")
s.header("Enter a company's ticker in the sidebar:")


ticker = s.sidebar.text_input("Ticker", value="AAPL").upper().strip()
if not ticker:
    s.stop()
with s.spinner(f"getting {ticker}"):
    years = history(ticker)
    company = years[0]
    grossMarginSeries      = [grossMargin(y["revenue"], y["cogs"]) for y in years]
    opMarginSeries         = [opMargin(y["operatingIncome"], y["revenue"]) for y in years]
    netMarginSeries        = [netMargin(y["netIncome"], y["revenue"]) for y in years]
    currentRatioSeries     = [currentRatio(y["currentAssets"], y["currentLiabilities"]) for y in years]
    quickRatioSeries       = [quickRatio(y["currentAssets"], y["currentLiabilities"], y["inventory"]) for y in years]
    debtToEquitySeries     = [debtToEquity(y["totalLiabilities"], y["shareholderEquity"]) for y in years]
    returnOnEquitySeries   = [returnOnEquity(y["netIncome"], y["shareholderEquity"]) for y in years]
    returnOnAssetsSeries   = [returnOnAssets(y["netIncome"], y["totalAssets"]) for y in years]
    interestCoverageSeries = [interestCoverage(y["operatingIncome"], y["interestExpense"]) for y in years]

    gmD  = grossMarginDelta(grossMarginSeries)
    omD  = opMarginDelta(opMarginSeries)
    nmD  = netMarginDelta(netMarginSeries)
    crD  = currentRatioDelta(currentRatioSeries)
    qrD  = quickRatioDelta(quickRatioSeries)
    deD  = debtToEquityDelta(debtToEquitySeries)
    roeD = returnOnEquityDelta(returnOnEquitySeries)
    roaD = returnOnAssetsDelta(returnOnAssetsSeries)
    icD  = interestCoverageDelta(interestCoverageSeries)
if company["revenue"] is None:
    s.error(f"No instance  of financial data for {ticker}")
    s.stop()
s.metric("Ticker", company["ticker"])
with s.expander("Raw figures"):
    s.metric("Revenue", fmt(company["revenue"], "currency"))
    s.metric("Cost of Goods sold", fmt(company["cogs"], "currency"))
    s.metric("Interest Expense", fmt(company["interestExpense"], "currency"))
    s.metric("Operating Income", fmt(company["operatingIncome"], "currency"))
    s.metric("Current Assets", fmt(company["currentAssets"], "currency"))
    s.metric("Current Liabilities", fmt(company["currentLiabilities"], "currency"))
    s.metric("Inventory", fmt(company["inventory"], "currency"))
    s.metric("Total Liabilities", fmt(company["totalLiabilities"], "currency"))
    s.metric("Shareholder Equity", fmt(company["shareholderEquity"], "currency"))
    s.metric("Total Assets", fmt(company["totalAssets"], "currency"))
    s.metric("Net Income", fmt(company["netIncome"], "currency"))

df = yf.download(company["ticker"], period="1y")

one, two, three, four = s.tabs(["Profitability", "Liquidity", "Leverage", "Returns"])

with one:
    
    c1, c2, c3 = s.columns(3)
    with c1:
        s.metric("Gross Margin", fmt(grossMargin(company["revenue"], company["cogs"]), "percent"),
                 delta=deltaOf(gmD, "gross margin percent change 1", "percent"))
    with c2:
        s.metric("Operating Margin", fmt(opMargin(company["operatingIncome"], company["revenue"]), "percent"),
                 delta=deltaOf(omD, "operating margin percent change 1", "percent"))
    with c3:
        s.metric("Net Margin", fmt(netMargin(company["netIncome"], company["revenue"]), "percent"),
                 delta=deltaOf(nmD, "net margin percent change 1", "percent"))
    

    
    marginDf = p.DataFrame(
    {
        "Gross Margin": grossMarginSeries,
        "Operating Margin": opMarginSeries,
        "Net Margin": netMarginSeries},
        index=[str(y["year"].year)[0:1] + str(y["year"].year)[1:] for y in years]
    
    )
    s.line_chart(marginDf[::-1])
    with s.expander("Missing years"):
        missingNote(grossMarginSeries, years, "Gross margin")
        missingNote(opMarginSeries, years, "Operating margin")
        missingNote(netMarginSeries, years, "Net margin")

    s.write("Most recent Year" , df.index.year[0])

   


with two:
    
    c4, c5 = s.columns(2)

    with c4:
        s.metric("Current Ratio", fmt(currentRatio(company["currentAssets"], company["currentLiabilities"]), "multiple"),
                 delta=deltaOf(crD, "current ratio raw difference 1", "multiple"))

    with c5:
        s.metric("Quick Ratio", fmt(quickRatio(company["currentAssets"], company["currentLiabilities"], company["inventory"]), "multiple"),
                 delta=deltaOf(qrD, "quick ratio raw difference 1", "multiple"))

    ratioDf = p.DataFrame(
    {
        "Current Ratio": currentRatioSeries,
        "Quick Ratio":  quickRatioSeries
    },
    index = [str(y["year"].year)[0:1] + str(y["year"].year)[1:] for y in years]
    )


    s.line_chart(ratioDf[::-1])

    with s.expander("Missing years"):
        missingNote(currentRatioSeries, years, "Current ratio")
        missingNote(quickRatioSeries, years, "Quick ratio")
    s.write("Most recent Year" , df.index.year[0])

with three:
    
    c6, c7 = s.columns(2)

    with c6:
        s.metric("Debt To Equity", fmt(debtToEquity(company["totalLiabilities"],company["shareholderEquity"]), "multiple"),
                 delta=deltaOf(deD, "debt to equity raw difference 1", "multiple"),
                 delta_color="inverse")
    with c7:
        s.metric("Interest Coverage", fmt(interestCoverage(company["operatingIncome"], company["interestExpense"]), "multiple"),
                 delta=deltaOf(icD, "interest coverage raw difference 1", "multiple"))

    s.subheader("Debt to Equity Graph:")
    leverageDF = p.DataFrame(
    {
        "Debt to Equity": debtToEquitySeries
        
    },
    index = [str(y["year"].year)[0:1] + str(y["year"].year)[1:] for y in years]
    )

    s.line_chart(leverageDF[::-1])
    s.subheader("Interest Coverage Graph:")
    leverage2DF = p.DataFrame(
    {
        "Interest Coverage": interestCoverageSeries,
        
    },
    index = [str(y["year"].year)[0:1] + str(y["year"].year)[1:] for y in years]
    )

    s.line_chart(leverage2DF[::-1])

    with s.expander("Missing years"):
        missingNote(debtToEquitySeries, years, "Debt to equity")
        missingNote(interestCoverageSeries, years, "Interest coverage")
    s.write("Most recent Year" , df.index.year[0])


with four:
   
    c8, c9 = s.columns(2)

    with c8:
        s.metric("Return On Equity", fmt(returnOnEquity(company["netIncome"], company["shareholderEquity"]), "percent"),
                 delta=deltaOf(roeD, "return on equity percent change 1", "percent"))
    with c9:
        s.metric("Return On Assets", fmt(returnOnAssets(company["netIncome"], company["totalAssets"]), "percent"),
                 delta=deltaOf(roaD, "return on assets percent change 1", "percent"))
    roDF = p.DataFrame(
    {
        "Return on Equity": returnOnEquitySeries,
        "Return on Assets": returnOnAssetsSeries
    },
    index = [str(y["year"].year)[0:1] + str(y["year"].year)[1:] for y in years]
    )

    s.line_chart(roDF[::-1])

    with s.expander("Missing years"):
        missingNote(returnOnEquitySeries, years, "Return on equity")
        missingNote(returnOnAssetsSeries, years, "Return on assets")
    s.write("Most recent Year" , df.index.year[0])






s.divider()
s.download_button(
    label=f"Download {ticker} financials (.xlsx)",
    data=workbookBytes(years, ticker),
    file_name=f"{ticker}_financials.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
