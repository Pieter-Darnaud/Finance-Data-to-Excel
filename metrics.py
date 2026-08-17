


def cogs(bInventory, purchases, eInventory):
    return bInventory + purchases - eInventory

def grossProfit(revenue, cogs):
    return revenue - cogs

def opIncome(grossProfit, opex):
    return grossProfit - opex

def grossMargin(revenue, cogs):
   
    if revenue == 0:
        return "N/A" 
    return (revenue - cogs) / revenue

def netMargin (netIncome, revenue):
    if revenue == 0:
            return "N/A" 
    return netIncome / revenue

def opMargin (opIncome, revenue):
    if revenue == 0:
            return "N/A" 
    return opIncome / revenue

def currentRatio (currentAssets, currentLiabilities):
    if currentLiabilities == 0:
             return "N/A" 
    return currentAssets / currentLiabilities

def quickRatio(currentAssets, currentLiabilities, inventory):
    if currentLiabilities == 0:
             return "N/A" 
    return (currentAssets - inventory) / currentLiabilities

def debtToEquity(totalLiabilities, shareholderEquity):
    if shareholderEquity == 0:
        return "N/A"
    
    return totalLiabilities / shareholderEquity

def returnOnEquity(netIncome, shareholderEquity):
    if shareholderEquity == 0: # Revenue and total assets cancel
            return "N/A"
    return netIncome / shareholderEquity

def returnOnAssets(netIncome, totalAssets):
    if totalAssets == 0:
            return "N/A"
    return netIncome / totalAssets

def interestCoverage(operatingIncome, interestExpense):
    if interestExpense == 0:
     return "N/A"
    
    return operatingIncome / interestExpense
