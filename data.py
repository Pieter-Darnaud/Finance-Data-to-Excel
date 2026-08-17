# Import yfinance tool:

import yfinance as yf






# To test if companies have a value, use this: 
def get_financials(companyTicker):
    
    
    try:
        company = yf.Ticker(companyTicker).financials
        return (
            {"ticker": companyTicker,
             "revenue": company.loc["Total Revenue"].iloc[0],
             "cogs": company.loc["Cost Of Revenue"].iloc[0]}
            
        )
    except KeyError as e:
        print(f"  skipping {companyTicker}: no {e} line")
    
        return None 






companies = []

def companyChecker(sCompanies):
    for i in sCompanies:
        if get_financials(i) != None:
            companies.append(get_financials(i))

#Testing def functions
companyChecker(["MSFT", "AAPL", "GOOGL", "BAC"])







       







