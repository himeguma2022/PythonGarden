import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
import threading

def main():
    '''
    APIGetStock("AAPL")  # Example ticker symbol for Apple Inc.
    APIGetStock("GOOGL")  # Example ticker symbol for Alphabet Inc.
    APIGetStock("MSFT")  # Example ticker symbol for Microsoft Corporation
    APIGetStock("AMZN")  # Example ticker symbol for Amazon.com Inc.
    APIGetStock("TSLA")  # Example ticker symbol for Tesla Inc.
    APIGetStock("NFLX")  # Example ticker symbol for Netflix Inc.
    APIGetStock("META")  # Example ticker symbol for Meta Platforms Inc.
    APIGetStock("NVDA")  # Example ticker symbol for NVIDIA Corporation
    APIGetStock("AMD")  # Example ticker symbol for Advanced Micro Devices Inc.
    APIGetStock("INTC")  # Example ticker symbol for Intel Corporation
    APIGetStock("CSCO")  # Example ticker symbol for Cisco Systems Inc.
    APIGetStock("ORCL")  # Example ticker symbol for Oracle Corporation
    APIGetStock("IBM")  # Example ticker symbol for International Business Machines Corporation
    APIGetStock("WMT")  # Example ticker symbol for Walmart Inc.
    APIGetStock("DIS")  # Example ticker symbol for The Walt Disney Company
    APIGetStock("PFE")  # Example ticker symbol for Pfizer Inc.
    APIGetStock("JNJ")  # Example ticker symbol for Johnson & Johnson
    APIGetStock("V")    # Example ticker symbol for Visa Inc.
    APIGetStock("MA")   # Example ticker symbol for Mastercard Incorporated
    APIGetStock("KO")  # Example ticker symbol for The Coca-Cola Company
    APIGetStock("PEP")  # Example ticker symbol for PepsiCo Inc. 
    APIGetStock("MRK")  # Example ticker symbol for Merck & Co., Inc.
    APIGetStock("ABT")  # Example ticker symbol for Abbott Laboratories
    APIGetStock("CVX")  # Example ticker symbol for Chevron Corporation
    APIGetStock("XOM")  # Example ticker symbol for Exxon Mobil Corporation
    APIGetStock("BA")  # Example ticker symbol for The Boeing Company
    APIGetStock("CAT")  # Example ticker symbol for Caterpillar Inc.
    APIGetStock("MMM")  # Example ticker symbol for 3M Company
    APIGetStock("UNH")  # Example ticker symbol for UnitedHealth Group Incorporated
    APIGetStock("HD")  # Example ticker symbol for The Home Depot, Inc.
    APIGetStock("VZ")  # Example ticker symbol for Verizon Communications Inc.
    APIGetStock("T")  # Example ticker symbol for AT&T Inc. 
    APIGetStock("ADBE")  # Example ticker symbol for Adobe Inc.
    APIGetStock("BTC-USD")  # Example ticker symbol for Bitcoin in USD
    APIGetStock("EUR-USD")  # Example ticker symbol for Euro to USD exchange rate
    APIGetStock("GBP-USD")  # Example ticker symbol for British Pound to USD exchange rate
    APIGetStock("SPY")  # Example ticker symbol for SPDR S&P 500 ETF Trust
    APIGetStock("QQQ")  # Example ticker symbol for Invesco QQQ Trust
    APIGetStock("JPY=X")  # Example ticker symbol for USD to Japanese Yen exchange rate
    APIGetStock("TWD=X")  # Example ticker symbol for USD to New Taiwan Dollar exchange rate
    APIGetStock("GC=F")  # Example ticker symbol for Gold Futures
    APIGetStock("SI=F")  # Example ticker symbol for Silver Futures
'''
    [Ay, Ad, Ap] = APIGetStock("COST")  # Example ticker symbol for Costco Wholesale Corporation

    #R = TestBestFitKnn(Ay)
    [p,a] = SingleStockKnn(Ay, 2, 0.7, 1)
    
    plt.plot(Ad, Ay)
    plt.plot(Ad, p)
    plt.show()
    #print(R)
    
    
    
def APIGetStock(ticker_symbol: str):
    T:yf.Ticker = yf.Ticker(ticker_symbol)
    # Get historical market data
    hist = T.history(period="max")
    d = hist.get("Close").index.normalize().date
    yc = hist.get("Close").values
    y = np.zeros(len(d))
    for i in range(1,len(y)):
        y[i] = yc[i] / yc[i-1] - 1
    return[y, d, yc]

def TestBestFitKnn(x:np.array):
    results = []
    for d in range(2, 3):
        results.append(testKs(x, d))
    return results

def testKs(x:np.array, d:int):
    results = []
    for k in range(1, 5):
        [p, r1] = SingleStockKnn(x, d, 0.9, k)
        [p, r2] = SingleStockKnn(x, d, 0.9, k)
        [p, r3] = SingleStockKnn(x, d, 0.9, k)
        results.append(np.mean([r1, r2, r3]))
    return results   
        
def SingleStockKnn(x:np.array,d:int,t:float,k:int):
    train = x[:math.floor(len(x) * t - d)]
    test = x[math.floor(len(x) * t - d):]
    trainX = np.zeros((len(train) - d, d))
    testX = np.zeros((len(test) - d, d))
    for i in range(d):
        trainX[:, i] = train[i:len(train) - d + i]
        testX[:, i] = test[i:len(test) - d + i]
    trainY = train[d:len(train)]
    testY = test[d:len(test)]
    
    pTest = np.zeros(len(testY))
    eTest = np.zeros(len(testY))
    rAccuracyCount = 0
    for t in range(len(pTest)):
        distances = np.array([distance(train[t], x) for x in trainX])
        indices = np.argsort(distances)[:k]
        pTest[t] = np.mean(trainY[indices])
        eTest[t] = pTest[t] - testY[t]
        if sameSign(pTest[t], testY[t]):
            rAccuracyCount += 1
    rAccuracy = rAccuracyCount / len(pTest)
    print(f"Total Error: {np.sum(eTest):.4f}")
    print(f"Accuracy: {rAccuracy * 100:.2f}%")
    
    return [np.append(x[:-len(pTest)], pTest), rAccuracy]
        
def distance(a:np.array, b:np.array):
    return np.sqrt(np.sum((a - b) ** 2))

def sameSign(a:float, b:float):
    return (a > 0 and b > 0) or (a < 0 and b < 0)

if __name__ == "__main__":
    main()