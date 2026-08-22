# Import yfinance tool:

import yfinance as yf






# To test if companies have a value, use this: 
'''def get_financials(companyTicker):
    
    
    try:
        company = yf.Ticker(companyTicker).financials
        return (
            {"ticker": companyTicker,
             "revenue": company.loc["Total Revenue"].iloc[0],
             "cogs": company.loc["Cost Of Revenue"].iloc[0]}
            
        )
    except KeyError as e:
        print(f"  skipping {companyTicker}: no {e} line")
    
        return None '''


def precheck(statement, rowName):
    try:
        return statement.loc[rowName].iloc[0]
    except KeyError as e:
        return None

def get_financials(companyTicker):
    t = yf.Ticker(companyTicker)
    f = t.financials
    b = t.balance_sheet
    return{
        "ticker": companyTicker,
        "revenue": precheck(f, "Total Revenue"),
        "cogs": precheck(f, "Cost Of Revenue"),
        "operatingIncome": precheck(f, "Operating Income"),
        "interestExpense": precheck(f, "Interest Expense"),
        "currentAssets": precheck(b, "Current Assets"),
        "currentLiabilities": precheck(b, "Current Liabilities"),
        "inventory": precheck(b, "Inventory"),
        "totalLiabilities": precheck(b, "Total Liabilities Net Minority Interest"),
        "shareholderEquity": precheck(b, "Stockholders Equity"),
        "totalAssets": precheck(b, "Total Assets")

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







       







