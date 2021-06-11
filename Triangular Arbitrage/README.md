This program calculates loss or profit from triangular transactions among various global currencies. Rates are collected from <https://www.investing.com/currencies/streaming-forex-rates-majors>.  

Those who want to know about what triangular arbitrage is may visit <https://www.investopedia.com/terms/t/triangulararbitrage.asp> to find out.  

Triangular arbitrage is way of riskless trading taking advantage of momentary imbalances between the exchange rates. In real life, institutional investors engage in such transactions and those transactions are fulfilled by special software automatically in a second or so. This program obviously does not have that capacity but imitates the process and shows the use of some python libraries in performing that process.  

`real_case.py` detects any triangular arbitrage opportunity looking at the real exchange rates. However, as this is just an imitation of the real process, such an opportunity is seldom exposed.  

In order to see the working of the program more obviously, `scenario_case.py` fakes movements in the currency rates and returns results similar to below:  

>---------------------------------------------------------------------------------------------------------  
>sell USD 995,000.00 and buy JPY 103,727,070.16 at the rate  104.24831 and transaction cost USD 5,000.00  
>- -------------------------------------------------------------------------------------------------------  
>sell JPY 103,208,434.81 and buy CHF 881,466.36 at the rate  0.00854 and transaction cost JPY 518,635.35  
>- -------------------------------------------------------------------------------------------------------  
>sell CHF 877,059.03 and buy USD 998,660.72 at the rate  1.13865 and transaction cost CHF 4,407.33  
>- -------------------------------------------------------------------------------------------------------  
>
>Invested USD 1,000,000.00 and earned USD 998,660.72 thus making USD -1,339.28 profit.  

There is also AWS version of this application: <https://github.com/hsaltan/AWS-Projects/tree/main/Triangular%20Arbitrage>
