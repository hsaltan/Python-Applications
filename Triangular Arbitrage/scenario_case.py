import numpy as np
import itertools
import time
from datetime import datetime
import pytz

tz_London = pytz.timezone('Europe/London')

# Starting currencies and their quotations. Rates as of January 5, 2021 14:50 UTC+3
initialExchangeRates = {"USD/EUR": 1.22831, "JPY/USD": 102.820,"USD/GBP": 1.35942,"USD/CHF": 1.1409,
                            "JPY/EUR": 126.295, "EUR/GBP": 1.10674,"CHF/EUR": 1.08069,"JPY/GBP": 139.766,
                            "JPY/CHF": 116.856,"CHF/GBP": 1.19600}

# Randomly chosen rate of change in currencies 
ratesOfChange = np.linspace(-0.1, 0.1, 40)  

exchangeRateNames = list(initialExchangeRates.keys())
numberOfExchangeRates = len(initialExchangeRates)
currencySet = set()
for i in exchangeRateNames:
    currencySet.add(i[0:3])
    currencySet.add(i[4:7])
listOfCurrencies = list(currencySet)


def currency_arbitrage_parameters(x = 1_000_000, y = 0.005, z = 'USD'):
    # Initial investment amount, transaction cost and the currency of the investment amount 
    global investmentAmount, transactionCommission, currency
    investmentAmount = x
    transactionCommission = y
    currency = z
    print(f' Investment amount: {investmentAmount:,.2f} \n Transaction commission percentage: {transactionCommission:,.4f} \n Initial currency for investment: {currency}')
    print('\n')
    filteredList = list(filter(filtering_function, triangular_composition()))
    find_transactions(filteredList)
    
    
def rearrange_exchange_rates(listOfCurrencies):
    """Rearranging the dictionary so that there will be an equal number of mention of each currency in the 
    nominator and denominator of exchange rates."""
    repeatedList = list(itertools.chain.from_iterable(itertools.repeat(i, 2) for i in listOfCurrencies))
    extendedList = [x for x in repeatedList]
    extendedList.extend(repeatedList[0:3])
    del extendedList[:3]
    combinedList = [a +"/" + b for a, b in zip(repeatedList, extendedList)]
 
    """Currencies are cross-aligned such as EUR/GBP, USD/EUR, JPY/USD. Their multiplication should almost equal 
        to 1, which is the initial efficient equilibrium value. Any significantly different value indicates an 
        opportunity for triangular arbitrage."""
    rearrangedExchangeRates = {}
    for key, value in initialExchangeRates.items():
        if key in combinedList:
            rearrangedExchangeRates[key] = initialExchangeRates[key]
        else:
            newKey = key[4:7] + "/" + key[0:3]
            newValue = 1 / value
            rearrangedExchangeRates[newKey] = newValue    
    initialEfficientEquilibriumValue = np.prod(list(rearrangedExchangeRates.values())) # This should almost equal to 1  
    print(f" Rearranged exchange rates: {rearrangedExchangeRates} \n Initial efficient equilibrium value: {initialEfficientEquilibriumValue:.5f}")
    print("\n")
    return rearrangedExchangeRates

    
def currency_change():
    rearrangedExchangeRates = rearrange_exchange_rates(listOfCurrencies)
    global efficientExchangeRates
    efficientExchangeRates = {}
    rearrangedExchangeRateNames = list(rearrangedExchangeRates.keys())

    # The value of a randomly chosen currency changes
    changedCurrency = np.random.choice(rearrangedExchangeRateNames)

    # Randomly chosen rate of increase or decrease in the value of chosen currency
    rateOfChange = np.random.choice(ratesOfChange)
    newValueOfChangedCurrency = rearrangedExchangeRates[changedCurrency] * (1 + rateOfChange)

    """The change should have cascading effect on other rates so that the initial efficient equilibrium value (EEV) 
    stays around 1. Geometric mean refers to the average should-be change in other rates for IEEV to stay at its
    initial level. The following code imitates that cascading effect."""
    geometricMean = (1 + rateOfChange)**(1/(numberOfExchangeRates-1))

    # efficientExchangeRates is the collection of new exchange rates after the change when initial EEV =~ 1
    efficientExchangeRates = {} 
    for key, value in rearrangedExchangeRates.items():
        if key == changedCurrency:
            efficientExchangeRates[key] = newValueOfChangedCurrency
        else:
            efficientExchangeRates[key] = value / geometricMean

    # The new EEV will be the same as the initial EEV.
    newEfficientEquilibriumValue = np.prod(list(efficientExchangeRates.values())) 
    print(f" Changed currency: {changedCurrency} \n Rate of change: {rateOfChange:.4f} \n Average dependent change in other rates: {geometricMean:.5f}")
    print(f" Exchange rates after the change: {efficientExchangeRates} \n EEV after the change: {newEfficientEquilibriumValue:.5f}")
    print("\n")

    """A randomly chosen exchange rate deviates from the efficient path, thus making EEV significantly differ 
    from 1. The following code imitates that anomaly"""
    anomalousCurrency = np.random.choice([x for x in efficientExchangeRates.keys() if x != changedCurrency])

    # For a more realistic anomaly effect, a lower rate of change is applied
    anomalousRateOfChange = 1 + (np.random.choice(ratesOfChange) * 0.20)
    efficientExchangeRates[anomalousCurrency] = efficientExchangeRates[anomalousCurrency] * anomalousRateOfChange
    latestEfficientEquilibriumValue = np.prod(list(efficientExchangeRates.values()))
    print(f" Anomalous currency: {anomalousCurrency} \n Anomalous rate of change: {anomalousRateOfChange-1:.4f}")
    print(f" Exchange rates after the anomalous change: {efficientExchangeRates} \n EEV after the change: {latestEfficientEquilibriumValue:.5f}")
    print("\n")
    

def triangular_composition():  
    currency_change()

    """To take advantage of the anomaly, triangular arbitrage will realize 3 transactions across three exchange
    rates. The following code composes all combinations of three exchange rates in the given set."""
    n=3
    listCur = list(itertools.permutations(efficientExchangeRates.keys(),n))
    return listCur


def filtering_function(a):
    """Out of all combinations, we will select those in which the investment currency is in the first and last 
    exchange rates AND not in the middle rate which must contain currencies one of which is in the first and the
    other in the last exchange rate so that we can complete the full chain of transactions."""
    if a[0].find(currency) !=-1 and a[-1].find(currency) !=-1 and a[1].find(currency)==-1\
        and (a[1][4:7].find(a[0][:3]) !=-1 or a[1][:3].find(a[0][4:7]) !=-1) \
        and (a[-1][4:7].find(a[1][:3]) !=-1 or a[-1][:3].find(a[1][4:7]) !=-1):
        return True
    else:
        return False   

    
def find_transactions(filteredList):    
    print("Exchange rates that can be part of triangular arbitrage: ", filteredList)
    print("\n")

    #This function finds the most promising chain of transactions in the filtered list
    EquilibriumValues = []
    arbitrageBundle = {}
    for p in filteredList:

        # Finds the investment currency's index in the first exchange rate
        initialCurrencyIndex = p[0].find(currency)

        # Finds the currency in the first exchange rate, to which investment funds will be converted
        firstConvertedCurrency = p[0][4:7] if initialCurrencyIndex == 0 else p[0][0:3]

        # First exchange rate in the chain of three rates
        firstTermValue = efficientExchangeRates[p[0]]

        """Depending on the position of investment currency as the nominator or denominator, we either have to 
        multiply or divide it by the first exchange rate. For the calculation here, we take the investment amount as
        1 unit of investment currency"""
        evFirstTerm = (1 / firstTermValue) if initialCurrencyIndex == 0 else (1 * firstTermValue)
        EquilibriumValues.append(evFirstTerm)
        for r in range(1, len(p)):

            # Same process for the second and last exchange rates in the chain of transactions
            nextCurrencyIndex = p[r].find(firstConvertedCurrency)
            nextConvertedCurrency = p[r][4:7] if nextCurrencyIndex == 0 else p[r][0:3]
            nextTermValue = efficientExchangeRates[p[r]]
            evNextTerm = (1 / nextTermValue) if nextCurrencyIndex == 0 else (1 * nextTermValue)
            firstConvertedCurrency = nextConvertedCurrency
            EquilibriumValues.append(evNextTerm)
 
        # Finds the equilibrium value for each transaction chain in the filtered list
        bundleEquilibriumValue = np.prod(EquilibriumValues)
        arbitrageBundle[p] = bundleEquilibriumValue      
        EquilibriumValues = []

    # Finds the transaction chain with the highest equilibrium value, that is the most promising candidate for arbitrage    
    maxEquilibriumValue =(max(arbitrageBundle, key=arbitrageBundle.get), max(arbitrageBundle.values()))
    print("The most promising transaction for triangular arbitrage: ", maxEquilibriumValue)
    print("\n")
    calculate_profitability(maxEquilibriumValue)


def calculate_profitability(maxEquilibriumValue):
    # This function calculates if the selected transaction chain is profitable for a triangular arbitrage or not   
    tradingRate_1 = efficientExchangeRates[maxEquilibriumValue[0][0]]
    tradingRate_2 = efficientExchangeRates[maxEquilibriumValue[0][1]]
    tradingRate_3 = efficientExchangeRates[maxEquilibriumValue[0][2]]

    # There will be three transactions so, three times the investor will incur the transaction commission
    transactionCost = maxEquilibriumValue[1] * ((1 + transactionCommission) ** 3 - 1)
    valueAfterCost = maxEquilibriumValue[1] - transactionCost
    print(f"Transaction cost: {transactionCost:.6f} \nValue after cost: {valueAfterCost:.6f} \n")
    datetime_London = datetime.now(tz_London)
    print("London time:", datetime_London.strftime("%Y/%m/%d - %H:%M:%S"), "\n")
    if valueAfterCost > 1:
        calculate_arbitrage(tradingRate_1, tradingRate_2, tradingRate_3, valueAfterCost, maxEquilibriumValue)
    else:
        print("no occassion for triangular arbitrage")


def calculate_arbitrage(tradingRate_1, tradingRate_2, tradingRate_3, valueAfterCost, maxEquilibriumValue):       
    # In case the transaction chain is profitable, the following chunk of code calculates the transactions
    currencyIndex_1 = maxEquilibriumValue[0][0].find(currency)
    sellCurrency_1 = currency
    buyCurrency_1 = maxEquilibriumValue[0][0][0:3] if currencyIndex_1 == 4 else maxEquilibriumValue[0][0][4:7]
    transactionCostAmount_1 = investmentAmount * transactionCommission
    netTransactionAmount_1 = investmentAmount - transactionCostAmount_1
    tradingAmount_1 = netTransactionAmount_1 * tradingRate_1 if currencyIndex_1 == 4 \
                                                            else netTransactionAmount_1 / tradingRate_1
    print('---------------------------------------------------------------------------------------------------------------------')
    print(f'sell {sellCurrency_1} {netTransactionAmount_1:,.2f} and buy {buyCurrency_1} {tradingAmount_1:,.2f} at the rate {tradingRate_1: .5f} and transaction cost {sellCurrency_1} {transactionCostAmount_1:,.2f}')
    print('---------------------------------------------------------------------------------------------------------------------')
    currencyIndex_2 = maxEquilibriumValue[0][1].find(buyCurrency_1)
    sellCurrency_2 = buyCurrency_1
    buyCurrency_2 = maxEquilibriumValue[0][1][0:3] if currencyIndex_2 == 4 else maxEquilibriumValue[0][1][4:7]
    transactionCostAmount_2 = tradingAmount_1 * transactionCommission
    netTransactionAmount_2 = tradingAmount_1 - transactionCostAmount_2
    tradingAmount_2 = netTransactionAmount_2 * tradingRate_2 if currencyIndex_2 == 4 \
                                                            else netTransactionAmount_2 / tradingRate_2
    print(f'sell {sellCurrency_2} {netTransactionAmount_2:,.2f} and buy {buyCurrency_2} {tradingAmount_2:,.2f} at the rate {tradingRate_2: .5f} and transaction cost {sellCurrency_2} {transactionCostAmount_2:,.2f}')
    print('---------------------------------------------------------------------------------------------------------------------')        
    currencyIndex_3 = maxEquilibriumValue[0][2].find(buyCurrency_2)
    sellCurrency_3 = buyCurrency_2
    buyCurrency_3 = maxEquilibriumValue[0][2][0:3] if currencyIndex_3 == 4 else maxEquilibriumValue[0][2][4:7]
    transactionCostAmount_3 = tradingAmount_2 * transactionCommission
    netTransactionAmount_3 = tradingAmount_2 - transactionCostAmount_3
    tradingAmount_3 = netTransactionAmount_3 * tradingRate_3 if currencyIndex_3 == 4 \
                                                            else netTransactionAmount_3 / tradingRate_3
    print(f'sell {sellCurrency_3} {netTransactionAmount_3:,.2f} and buy {buyCurrency_3} {tradingAmount_3:,.2f} at the rate {tradingRate_3: .5f} and transaction cost {sellCurrency_3} {transactionCostAmount_3:,.2f}')      
    print('---------------------------------------------------------------------------------------------------------------------')
    print('\n')
    netProfit = tradingAmount_3 - investmentAmount
    print(f'Invested {sellCurrency_1} {investmentAmount:,.2f} and earned {buyCurrency_3} {tradingAmount_3:,.2f} thus making {buyCurrency_3} {netProfit:,.2f} profit.')
    print('\n')
    print('---------------------------------------------------------------------------------------------------------------------')          
   
