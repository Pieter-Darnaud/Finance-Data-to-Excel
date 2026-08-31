


def cogs(bInventory, purchases, eInventory):
    return bInventory + purchases - eInventory

def grossProfit(revenue, cogs):
    return revenue - cogs

def opIncome(grossProfit, opex):
    return grossProfit - opex

def grossMargin(revenue, cogs):
   
    if revenue == 0 or revenue == None or revenue != revenue or cogs == 0 or cogs == None or cogs != cogs:
        return None 
    return (revenue - cogs) / revenue

def grossMarginDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
              
              
    x = 0
    if len(values) == 0:
             return  "no gross margin data"
    if len(values) == 1:
             return  "no gross margin change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
            x += 1

            c[f"gross margin percent change {x}"] = (values[j] - values[j+ 1]) / values[j+ 1]
    c["overall gross margin percent change"] = (values[0] - values[len(values) - 1]) / values[len(values) - 1]
    return c



        
        

              
              
def netMargin (netIncome, revenue):
    if revenue == 0 or revenue == None or revenue != revenue or netIncome == 0 or netIncome == None or netIncome != netIncome:
            return None 
    return netIncome / revenue


def netMarginDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
             return  "no net margin data"
    if len(values) == 1:
             return  "no net margin change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
            x += 1

            c[f"net margin percent change {x}"] = (values[j] - values[j + 1]) / values[j + 1]
    c["overall net margin percent change"] = (values[0] - values[len(values) - 1]) / values[len(values) - 1]
    return c

def opMargin (opIncome, revenue):
    if revenue == 0 or revenue == None or revenue != revenue or opIncome == 0 or opIncome == None or opIncome != opIncome:
            return None 
    return opIncome / revenue

def opMarginDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
             return  "no operating margin data"
    if len(values) == 1:
             return  "no operating margin change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
            x += 1

            c[f"operating margin percent change {x}"] = (values[j] - values[j + 1]) / values[j + 1]
    c["overall operating margin percent change"] = (values[0] - values[len(values) - 1]) / values[len(values) - 1]
    return c

def currentRatio (currentAssets, currentLiabilities):
    if currentLiabilities == 0 or currentLiabilities == None or currentLiabilities != currentLiabilities or currentAssets == 0 or currentAssets == None or currentAssets != currentAssets:
             return None 
    return currentAssets / currentLiabilities

def currentRatioDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
                 return  "no current ratio data"
    if len(values) == 1:
                 return  "no current ratio change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
             x += 1
    
             c[f"current ratio raw difference {x}"] = (values[j] - values[j + 1]) / 1
    c["overall current ratio raw difference"] = (values[0] - values[len(values) - 1]) / 1
    return c



def quickRatio(currentAssets, currentLiabilities, inventory):
    if currentLiabilities == 0 or currentLiabilities == None or currentLiabilities != currentLiabilities or inventory == 0 or inventory == None or inventory != inventory or currentAssets != currentAssets or currentAssets == 0 or currentAssets == None:
             return None 
    return (currentAssets - inventory) / currentLiabilities

def quickRatioDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
                 return  "no quick ratio data"
    if len(values) == 1:
                 return  "no quick ratio change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
             x += 1
    
             c[f"quick ratio raw difference {x}"] = (values[j] - values[j + 1]) / 1
    c["overall quick ratio raw difference"] = (values[0] - values[len(values) - 1]) / 1
    return c

def debtToEquity(totalLiabilities, shareholderEquity):
    if shareholderEquity != shareholderEquity or shareholderEquity == 0 or shareholderEquity == None or totalLiabilities == 0 or totalLiabilities == None or totalLiabilities != totalLiabilities:
        return None
    
    return totalLiabilities / shareholderEquity

def debtToEquityDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
                 return  "no debt to equity data"
    if len(values) == 1:
                 return  "no debt to equity change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
             x += 1
    
             c[f"debt to equity raw difference {x}"] = (values[j] - values[j + 1]) / 1
    c["overall debt to equity raw difference"] = (values[0] - values[len(values) - 1]) / 1
    return c

def returnOnEquity(netIncome, shareholderEquity):
    if shareholderEquity == 0 or shareholderEquity != shareholderEquity or shareholderEquity == None  or netIncome == 0 or netIncome == None or netIncome != netIncome: # Revenue and total assets cancel
            return None
    return netIncome / shareholderEquity

def returnOnEquityDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
             return  "no return on equity data"
    if len(values) == 1:
             return  "no return on equity change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
            x += 1

            c[f"return on equity percent change {x}"] = (values[j] - values[j + 1]) / values[j + 1]
    c["overall return on equity percent change"] = (values[0] - values[len(values) - 1]) / values[len(values) - 1]
    return c


def returnOnAssets(netIncome, totalAssets):
    if totalAssets == 0 or totalAssets == None or totalAssets != totalAssets or netIncome == 0 or netIncome == None or netIncome != netIncome:
            return None
    return netIncome / totalAssets

def returnOnAssetsDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
             return  "no return on asset data"
    if len(values) == 1:
             return  "no return on asset change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
            x += 1

            c[f"return on assets percent change {x}"] = (values[j] - values[j + 1]) / values[j + 1]
    c["overall return on assets percent change"] = (values[0] - values[len(values) - 1]) / values[len(values) - 1]
    return c

def interestCoverage(operatingIncome, interestExpense):
    if interestExpense ==  0 or interestExpense == None or interestExpense != interestExpense or operatingIncome == 0 or operatingIncome == None or operatingIncome != operatingIncome:
     return None
    
    return operatingIncome / interestExpense

def interestCoverageDelta(values):
    c = {}
    clean = []
    for i in values:
        if i != None and i == i:
            clean.append(i)
    values = clean
    x = 0
    if len(values) == 0:
                 return  "no interest coverage data"
    if len(values) == 1:
                 return  "no interest coverage change yet"
    for j in range (len(values)):
        if j < (len(values) - 1 ) and len(values) > 1:
             x += 1
    
             c[f"interest coverage raw difference {x}"] = (values[j] - values[j + 1]) / 1
    c["overall interest coverage raw difference"] = (values[0] - values[len(values) - 1]) / 1
    return c


