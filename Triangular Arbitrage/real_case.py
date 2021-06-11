from bs4 import BeautifulSoup 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time
from datetime import datetime
import itertools
import pytz

tz_London = pytz.timezone('Europe/London')

#url of the page we want to scrape 
url = 'https://www.investing.com/currencies/streaming-forex-rates-majors'


def currency_arbitrage_parameters(x = 1_000_000, y = 0.005, z = 'USD'):
    # Initial investment amount, transaction cost and the currency of the investment amount 
    global investmentAmount, transactionCommission, currency
    investmentAmount = x
    transactionCommission = y
    currency = z
    filteredList = list(filter(filtering_function, triangular_composition()))
    calculate_arbitrage(filteredList)

    
def forexrates_parser():
    driver = webdriver.Chrome('/Users/hasanserdaraltan/OneDrive/Files/Education/Data_Science/Lab/ZL_Supplementary_Files/chromedriver')
    driver.get(url)  

    # Make sure that the page is loaded 
    time.sleep(2)  
    html = driver.page_source 
    soup = BeautifulSoup(html, "html.parser")  
    all_divs = soup.find("table", {"id": "cr1"}).find('tbody').find_all('tr') 

    # Get the exchange rates
    forEXRates = {} 
    for i in all_divs:
        cur = i.find("td", {"class": "bold left noWrap elp plusIconTd"}).text
        block = i.find_all('td')
        bid = float(block[2].text.replace(",", ""))
        ask = float(block[3].text.replace(",", ""))
        forEXRates[cur] = [bid, ask]
    
    # Discard crypto currencies
    del forEXRates['BTC/USD']
    del forEXRates['BTC/EUR']
    del forEXRates['ETH/USD']
    driver.close()
    return forEXRates


def triangular_composition():
    forexKeys = forexrates_parser()
    currencyList = list(forexKeys.keys())
    """To take advantage of the anomaly, triangular arbitrage will realize 3 transactions across three exchange
    rates. The following code composes all combinations of three exchange rates in the given set."""
    n=3
    listCur = list(itertools.permutations(currencyList,n))
    return listCur


def filtering_function(a):
    """Out of all combinations, we will select those in which the investment currency is in the first and last 
    exchange rates AND not in the middle rate which must contain currencies one of which is in the first and the
    other in the last exchange rate so that we can complete the full chain of transactions."""
    if a[0].find(currency) !=-1 and a[-1].find(currency) !=-1 and a[1].find(currency)==-1\
        and (a[1].find(a[0][:3]) !=-1 or a[1].find(a[0][4:7]) !=-1) \
        and (a[-1].find(a[1][:3]) !=-1 or a[-1].find(a[1][4:7]) !=-1):
        return True
    else:
        return False
    
    
def calculate_arbitrage(filteredList):    
    n = 0
    while n < 3:
#    while True:
        forEXRates = forexrates_parser()
        Explanations = []
        Transactions = {"x":[0,0,0,0,0,0]}

        for p in filteredList:

            firstTransactionBid = forEXRates[p[0]][0]
            firstTransactionAsk = forEXRates[p[0]][1]
            firstTransactionCommission = investmentAmount * transactionCommission
            firstShortTransactionAmount = investmentAmount - firstTransactionCommission    
            if p[0].find(currency) == 0:
                firstLongTransactionAmount = firstShortTransactionAmount * firstTransactionBid 
                otex_1 = p[0][4:7]
                forex_1 = firstTransactionBid
            else:
                firstLongTransactionAmount = firstShortTransactionAmount / firstTransactionAsk
                otex_1 = p[0][:3]
                forex_1 = firstTransactionAsk     
            firstTransaction = f"Sell {currency} {investmentAmount:,.2f} and buy {otex_1} {firstLongTransactionAmount:,.2f} at the rate of {forex_1} and transaction cost of {currency} {firstTransactionCommission:,.2f}"

            secondTransactionBid = forEXRates[p[1]][0]
            secondTransactionAsk = forEXRates[p[1]][1]
            secondTransactionCommission = firstLongTransactionAmount * transactionCommission
            secondShortTransactionAmount = firstLongTransactionAmount - secondTransactionCommission    
            if p[1].find(otex_1) == 0:
                secondLongTransactionAmount = secondShortTransactionAmount * secondTransactionBid 
                otex_2 = p[1][4:7]
                forex_2 = secondTransactionBid
            else:
                secondLongTransactionAmount = secondShortTransactionAmount / secondTransactionAsk
                otex_2 = p[1][:3]
                forex_2 = secondTransactionAsk
            secondTransaction = f"Sell {otex_1} {secondShortTransactionAmount:,.2f} and buy {otex_2} {secondLongTransactionAmount:,.2f} at the rate of {forex_2} and transaction cost of {otex_1} {secondTransactionCommission:,.2f}"  

            thirdTransactionBid = forEXRates[p[2]][0]
            thirdTransactionAsk = forEXRates[p[2]][1]
            thirdTransactionCommission = secondLongTransactionAmount * transactionCommission
            thirdShortTransactionAmount = secondLongTransactionAmount - thirdTransactionCommission    
            if p[2].find(otex_2) == 0:
                thirdLongTransactionAmount = thirdShortTransactionAmount * thirdTransactionBid 
                otex_3 = p[2][4:7]
                forex_3 = thirdTransactionBid
            else:
                thirdLongTransactionAmount = thirdShortTransactionAmount / thirdTransactionAsk
                otex_3 = p[2][:3]
                forex_3 = thirdTransactionAsk
            thirdTransaction = f"Sell {otex_2} {thirdShortTransactionAmount:,.2f} and buy {otex_3} {thirdLongTransactionAmount:,.2f} at the rate of {forex_3} and transaction cost of {otex_2} {thirdTransactionCommission:,.2f}"

            profitOrLoss = thirdLongTransactionAmount - investmentAmount
            datetime_London = datetime.now(tz_London)
            londonDateTime = datetime_London.strftime("%Y/%m/%d - %H:%M:%S")
            if profitOrLoss > 0 and profitOrLoss > Transactions["x"][4]:
                Transactions.clear()
                Explanations.extend([londonDateTime, firstTransaction, secondTransaction, thirdTransaction, profitOrLoss, thirdLongTransactionAmount])
                Transactions["x"] = Explanations

        if Transactions["x"][4] > 0:
            print('---------------------------------------------------------------------------------------------------------------------')
            print('\n')
            print('London time: ', Transactions["x"][0])
            print('\n')
            print('---------------------------------------------------------------------------------------------------------------------')
            print(Transactions["x"][1])
            print('---------------------------------------------------------------------------------------------------------------------')
            print(Transactions["x"][2])
            print('---------------------------------------------------------------------------------------------------------------------')
            print(Transactions["x"][3])
            print('---------------------------------------------------------------------------------------------------------------------')    
            netProfit = Transactions["x"][4]
            earnedAmount = Transactions["x"][5]
            print('\n')
            print(f'Invested {currency} {investmentAmount:,.2f} and earned {currency} {earnedAmount:,.2f} thus making {currency} {netProfit:,.2f} profit.')
            print('\n')
            print('---------------------------------------------------------------------------------------------------------------------')          
            print('\n')
            print('\n')
        else:   
            print('London time: ', londonDateTime)
            print('\n')
            print("no occassion for triangular arbitrage")
            print('\n')

        Transactions.clear()
        Explanations = []
        n += 1
