


def cogs(bInventory, purchases, eInventory):
    return bInventory + purchases - eInventory

def grossProfit(revenue, cogs):
    return revenue - cogs

def opIncome(grossProfit, opex):
    return grossProfit - opex

def grossMargin(revenue, cogs):
   
    if revenue == 0 or revenue == None or revenue != revenue or cogs == 0 or cogs == None or cogs != cogs:
        return "N/A" 
    return (revenue - cogs) / revenue

def netMargin (netIncome, revenue):
    if revenue == 0 or revenue == None or revenue != revenue or netIncome == 0 or netIncome == None or netIncome != netIncome:
            return "N/A" 
    return netIncome / revenue

def opMargin (opIncome, revenue):
    if revenue == 0 or revenue == None or revenue != revenue or opIncome == 0 or opIncome == None or opIncome != opIncome:
            return "N/A" 
    return opIncome / revenue

def currentRatio (currentAssets, currentLiabilities):
    if currentLiabilities == 0 or currentLiabilities == None or currentLiabilities != currentLiabilities or currentAssets == 0 or currentAssets == None or currentAssets != currentAssets:
             return "N/A" 
    return currentAssets / currentLiabilities

def quickRatio(currentAssets, currentLiabilities, inventory):
    if currentLiabilities == 0 or currentLiabilities == None or currentLiabilities != currentLiabilities or inventory == 0 or inventory == None or inventory != inventory or currentAssets != currentAssets or currentAssets == 0 or currentAssets == None:
             return "N/A" 
    return (currentAssets - inventory) / currentLiabilities

def debtToEquity(totalLiabilities, shareholderEquity):
    if shareholderEquity != shareholderEquity or shareholderEquity == 0 or shareholderEquity == None or totalLiabilities == 0 or totalLiabilities == None or totalLiabilities != totalLiabilities:
        return "N/A"
    
    return totalLiabilities / shareholderEquity

def returnOnEquity(netIncome, shareholderEquity):
    if shareholderEquity == 0 or shareholderEquity != shareholderEquity or shareholderEquity == None  or netIncome == 0 or netIncome == None or netIncome != netIncome: # Revenue and total assets cancel
            return "N/A"
    return netIncome / shareholderEquity

def returnOnAssets(netIncome, totalAssets):
    if totalAssets == 0 or totalAssets == None or totalAssets != totalAssets or netIncome == 0 or netIncome == None or netIncome != netIncome:
            return "N/A"
    return netIncome / totalAssets

def interestCoverage(operatingIncome, interestExpense):
    if interestExpense ==  0 or interestExpense == None or interestExpense != interestExpense or operatingIncome == 0 or operatingIncome == None or operatingIncome != operatingIncome:
     return "N/A"
    
    return operatingIncome / interestExpense
