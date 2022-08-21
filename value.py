import yahoo_fin.stock_info as yf

def getStockData(stock):   
    cashflow = yf.get_cash_flow(stock)
    income = yf.get_income_statement(stock)
    balance = yf.get_balance_sheet(stock)
    print()
    print(income)
    print()
    print(cashflow)
    print()
    print(balance)
    # Total Cash From Operating Activities  
    TCFOA = (cashflow.loc["totalCashFromOperatingActivities"]).tolist()
    # Capital Expenditures 
    CE = (cashflow.loc["capitalExpenditures"]).tolist()
    # Net income
    NI = (cashflow.loc["netIncome"]).tolist()
    # Total revenue
    TR = (income.loc["totalRevenue"]).tolist()
    
    return TCFOA, CE, NI, TR

def FCF(TCFOA, CE):
    freeCashFlowOvertime = []
    for length in range(len(TCFOA)):
        fcf =  (TCFOA[length]) + (CE[length])
        freeCashFlowOvertime.append(fcf)
    freeCashFlowOvertime.reverse()
    return freeCashFlowOvertime

def percent(top,bottom):
    percentageChange = []
    for i in range(len(top)):
        change = (top[i]/bottom[i])
        percentageChange.append(change)
    APTI = percentageChange[0]
    SPTI = percentageChange[0]
    for i in range(1,len(percentageChange)):
        APTI += percentageChange[i]
        if percentageChange[i] < SPTI:
            SPTI = percentageChange[i]
    APTI /= len(percentageChange)
    percentageChange = sorted(percentageChange)
    med = percentageChange[(len(percentageChange)//2)-1]
    print()
    print(percentageChange)
    return round(APTI,3), round(SPTI,3), round(med,3)


def choosePercent(one, two, three, talk):
    print(f"Choose one of the two percentages for {talk}.")
    print(f"Press 1 for the mean value over the years which is {round(one*100,2)}%")    
    print(f"Press 2 for the lowest value over the years which is {round(two*100,2)}%")
    print(f"Press 3 for the median value over the years which is {round(three*100,2)}%")    
    val = int(input("Enter 1-3: "))
    if val == 2:
        return two
    elif val == 1:
        return one
    return three


def averagePercentageChange(list1):
    percentageChange = []
    for val in range(1,len(list1)):
        change = (list1[val] - list1[val-1])/abs(list1[val-1])            
        percentageChange.append(change)
    ave = 0
    for percent in percentageChange:
        ave += percent
    ave /= len(percentageChange)
    return ave, percentageChange


def revenuePotentialGrowth(averageChange, lastYearFCF):
    averageChange += 1
    futureCashFlow = []
    nextyear = lastYearFCF
    for i in range(5):
        nextyear *= averageChange
        futureCashFlow.append(nextyear)
    return futureCashFlow


def netPotentialGrowth(averageChange, revGrowth):
    futureCashFlow = []
    for i in range(len(revGrowth)):
        nextyear = revGrowth[i] * averageChange
        futureCashFlow.append(nextyear)
    return futureCashFlow

def requiredRateReturn():
    print()
    ret = int(input("What is the required rate of return in % "))
    ret /= 100
    return ret


def terminalValue(lastyear, RRR):
    perpetual_growth = 0.025
    ter = (lastyear*(1+perpetual_growth))/(RRR-perpetual_growth)    
    return ter


def presentValue(cfGrowth, terVal, RRR):
    cashFlowValueNow = []
    for i in range(len(cfGrowth)):
        nowVal = cfGrowth[i] / ((1+RRR)**(i+1))
        cashFlowValueNow.append(nowVal)
    nowVal = terVal / ((1+RRR)**(len(cfGrowth)))
    cashFlowValueNow.append(nowVal)    
    return cashFlowValueNow


def todaysCompanyValue(presVal):
    tCV = 0
    for i in presVal:
        tCV += i
    return tCV
                
        
def main():
    stock = input("Stock symbol ")        
    TCFOA, CE, NI, TR = getStockData(stock)
    TR.reverse()
    NI.reverse()    
    freeCashFlowOvertime = FCF(TCFOA, CE)
    APTI, SPTI, MPTI = percent(freeCashFlowOvertime,NI)
    talk = "Free Cash Flow / Net Income"
    chosen1 = choosePercent(APTI, SPTI, MPTI, talk)
    # Revenue Growth Rate
    RGR, l = averagePercentageChange(TR)
    rGrowth = revenuePotentialGrowth(RGR, TR[-1])
    # Net Income Margins
    ANIM, LNIM, MNIM = percent(NI,TR)
    talk = "Net Income Margins"
    chosen3 = choosePercent(ANIM, LNIM, MNIM, talk)   
    iGrowth = netPotentialGrowth(chosen3, rGrowth)   
    cfGrowth = netPotentialGrowth(chosen1,iGrowth)
    RRR = requiredRateReturn()
    terVal = terminalValue(cfGrowth[-1],RRR)
    presVal = presentValue(cfGrowth, terVal, RRR)
    tCV = todaysCompanyValue(presVal)
    print()
    print(f"Revenue from now until 5 years {TR} {rGrowth}")
    print(f"Net income from now until 5 years {NI} {iGrowth}")    
    print(f"Free cash flow from now until 5 years {freeCashFlowOvertime} {cfGrowth}") 
    print(f"Making the terminal value of the company {terVal/1000000000}B")
    print(f"Discounting future cash flow of the company {presVal}")    
    print(f"The intrinsic value of the company is {round((tCV/1000000000),2)}B")
    print(f"With a safety net of 30% it is {round((tCV/1000000000)*0.7,2)}B")
    
main()

