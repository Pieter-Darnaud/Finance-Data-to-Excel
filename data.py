# Import yfinance tool:

import yfinance as yf











def precheck(statement, rowName, year):
     try:
         return statement.loc[rowName].iloc[year]
     except (KeyError, IndexError):
         return None
def new_precheck(statement, rowName):
     try:
         return statement.loc[rowName].iloc[0]
     except (KeyError, IndexError):
         return None     


def history(ticker):
    t = yf.Ticker(ticker)
    f = t.financials
    b = t.balance_sheet
    n = min(len(t.financials.columns), len(t.balance_sheet.columns))
    daCol =[]
    for i in range(n):
        daCol.append({"ticker": ticker, "year": f.columns[i], "revenue": precheck(f, "Total Revenue",i),
                 "cogs": precheck(f, "Cost Of Revenue",i),
                 "operatingIncome": precheck(f, "Operating Income", i),
                 "interestExpense": precheck(f, "Interest Expense", i),
                 "currentAssets": precheck(b, "Current Assets", i),
                 "currentLiabilities": precheck(b, "Current Liabilities", i),
                 "inventory": precheck(b, "Inventory", i),
                 "totalLiabilities": precheck(b, "Total Liabilities Net Minority Interest", i),
                 "shareholderEquity": precheck(b, "Stockholders Equity", i),
                 "totalAssets": precheck(b, "Total Assets", i),
                 "netIncome": precheck(f, "Net Income", i)})
    return daCol

def get_financials(companyTicker):
     t = yf.Ticker(companyTicker)
     f = t.financials
     b = t.balance_sheet
     return{
         "ticker": companyTicker,
         "revenue": new_precheck(f, "Total Revenue"),
         "cogs": new_precheck(f, "Cost Of Revenue"),
         "operatingIncome": new_precheck(f, "Operating Income"),
         "interestExpense": new_precheck(f, "Interest Expense"),
         "currentAssets": new_precheck(b, "Current Assets"),
         "currentLiabilities": new_precheck(b, "Current Liabilities"),
         "inventory": new_precheck(b, "Inventory"),
         "totalLiabilities": new_precheck(b, "Total Liabilities Net Minority Interest"),
         "shareholderEquity": new_precheck(b, "Stockholders Equity"),
         "totalAssets": new_precheck(b, "Total Assets"),
         "netIncome": new_precheck(f, "Net Income")
     }





         






companies = []

def companyChecker(sCompanies):
    for i in range(len(sCompanies)):
        fake = True
        
        for j in range(len(companies)):
            if get_financials(companies[j]["ticker"])["ticker"] == sCompanies[i]:
                fake = False
                break
        if fake:    
        
            companies.append(get_financials(sCompanies[i]))

#Testing def functions
companyChecker(["MSFT", "AAPL", "GOOGL", "BAC"])







       







