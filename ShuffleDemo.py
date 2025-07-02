import itertools
import math
import queue
import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

class ShuffleDemo:
    def __init__(self, shufItems:list) -> None:
        if(len(shufItems) < 3):
            return
        self.originalOrder:list = shufItems.copy()
        self.Test(shufItems)
        fCount = 0
        if(len(shufItems) > 12):
            return
        while(fCount < 3 and not self.fair):
            fCount += 1
            shufItems = self.originalOrder.copy()
            self.Test(shufItems)
           
    def Test(self, shufItems):
        Results:dict[tuple:int] = dict()
        self.L = 10000
        for i in range(self.L):
            shufAttempt:tuple = RiffleShuffle(shufItems,7)
            if(shufAttempt not in Results):
                Results.update({shufAttempt:0})
            val:int = Results.get(shufAttempt)
            val += 1
            Results.update({shufAttempt:val})
            shufItems = self.originalOrder.copy()
            
        if(len(shufItems) > 12):
            return
        self.AllPossibliitiesPresent = len(Results) == math.factorial(len(shufItems))
        lResults:list[tuple:int] = sorted(Results.items(), key=lambda x:x[1])
        self.Results:dict[tuple:int] = dict(lResults)
        self.EvenPossibilities(10)
        
        
    def EvenPossibilities(self, topRanks:int):
        rawVals = list(self.Results.values())
        vals = np.asarray(rawVals, dtype=int)
        self.std = np.std(vals)
        self.min = min(vals)
        self.max = max(vals)
        self.mean = np.mean(vals)
        self.median = np.median(vals)
        self.skew = scipy.stats.skew(vals)
        commonList = list(self.Results.keys())
        self.leastCommonPresentOrders:list[tuple] = commonList[0:topRanks]
        self.mostCommontOrders:list[tuple] = commonList[-topRanks:len(commonList)]
        mostCommonFirst = commonList.copy()
        mostCommonFirst.reverse()
        ex = self.L/math.factorial(len(self.originalOrder))
        df = math.factorial(len(self.originalOrder)) - 1
        stat, pval = scipy.stats.chisquare(vals)
        self.fair = pval > 0.01 and self.AllPossibliitiesPresent
        
        plt.hist(vals)
        plt.show()
            
        
        
def PythonShuffle(deck:list) -> tuple:
    random.shuffle(deck)
    return tuple(deck)

def RiffleShuffle(deck:list, times: int) -> tuple:
    magicNum = math.ceil((len(deck)*(2 + math.tanh(random.random() - 1)) - 2)/4)
    g1 = deck[0:magicNum]
    g2 = deck[magicNum:]
    deck = []
    while(len(g1) > 0 and len(g2) > 0):
        if(random.random() > 0.5):
            deck.insert(0,g1.pop())
        else:
            deck.insert(0,g2.pop())
            
    while(len(g1) > 0 or len(g2) > 0):
        if(len(g1) > 0):
            deck.insert(0,g1.pop())
        if(len(g2) > 0):
            deck.insert(0,g2.pop())
        
    if(times > 0):
        return RiffleShuffle(deck, times - 1)
    return tuple(deck)
        

def OverHandShuffle(deck:list, moves:int) -> tuple:
    magicNum = math.ceil(2*len(deck)*random.random()/3)
    g1 = deck[0:magicNum]
    g2 = deck[magicNum:]
    g2.extend(g1)
    
    if(moves > 0):
        return OverHandShuffle(g2, moves - 1)
    return tuple(g2)
    
def main():
    shufItems = [1,2,3,4,5]
    A = ShuffleDemo(shufItems)
    print('Done!')

if __name__ == '__main__':
    main()
    