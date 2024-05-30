from datetime import date, timedelta
import math
from StockMoment import StockMoment
class StockHist:
    def __init__(self) -> None:
        self.Hist = dict()
    
    def AddMoment(self, moment: StockMoment):
        self.Hist.update({moment.date: moment.val})
        
    def CsvToHist(self, csv:str):
        scan = open(csv,"r",buffering=-1,encoding="utf-8")
        while(scan.readable()):
            dateVal = scan.readline().strip().strip('\ufeff')
            if(dateVal.__eq__('') == False):
                self.AddCsvStringMoment(dateVal)
            else:
                scan.close()
                break
            
    def AddCsvStringMoment(self, csvPoint:str):
        addMoment = StockMoment()
        addMoment.CsvToStockMoment(csvPoint)
        self.AddMoment(addMoment)
    
    def ClosingPrice(self, day:date) -> float:
        if(self.Hist.keys().__contains__(day)):
            return float(self.Hist.get(day))
        return float(self.ClosingPrice(day.__add__(timedelta(-1))))
    
    def OneShareGain(self, buyDate:date, sellDate:date) -> float:
        if((sellDate - buyDate).days < 0):
            return self.OneShareGain(sellDate, buyDate)
        return self.ClosingPrice(sellDate) - self.ClosingPrice(buyDate)
    
    def RatioGain(self, buyDate:date, sellDate:date) -> float:
        if((sellDate - buyDate).days < 0):
            return self.RatioGain(sellDate, buyDate)
        return self.ClosingPrice(sellDate)/self.ClosingPrice(buyDate)
    
    def ExpectedGainInDays(self, daysGap:int) -> float:
        firstDay:date = min(self.Hist.keys())
        sumVals = 0
        for valPoints in self.Hist.keys():
            if(valPoints > firstDay + timedelta(daysGap)):
                sumVals += self.OneShareGain(valPoints, valPoints - timedelta(daysGap))            
        return sumVals/((max(self.Hist.keys()) - firstDay - timedelta(daysGap)).days)
    
    def ExpectedGainRatioInDays(self, daysGap:int) -> float:
        firstDay:date = min(self.Hist.keys())
        sumVals = 0
        valsCounted = 0
        for valPoints in self.Hist.keys():
            if(valPoints > firstDay + timedelta(daysGap)):
                sumVals += self.RatioGain(valPoints, valPoints - timedelta(daysGap)) - 1 
                valsCounted+=1        
        return 1 + (sumVals/valsCounted)
    
    def ExpectedGainInWeeks(self, weeks:int) -> float:
        return self.ExpectedGainInDays(7 * weeks)
    
    def ExpectedGainInMonths(self, months:int) -> float:
        return self.ExpectedGainInWeeks(4 * months)
    
    def ExpectedGainInYears(self, years:int) -> float:
        return self.ExpectedGainInDays(365 * years)
    
    def ExpectedGainRatioInWeeks(self, weeks:int) -> float:
        return self.ExpectedGainRatioInDays(7 * weeks)
    
    def ExpectedGainRatioInMonths(self, months:int) -> float:
        return self.ExpectedGainRatioInWeeks(4 * months)
    
    def ExpectedGainRatioInYears(self, years:int) -> float:
        return self.ExpectedGainRatioInDays(365 * years)
    
    def Stats(self, dayGap:int):
        self.HistRatioGains:float = []
        firstDay:date = min(self.Hist.keys())
        for valPoints in self.Hist.keys():
            if(valPoints > firstDay + timedelta(dayGap)):
                self.HistRatioGains.append(self.RatioGain(valPoints, valPoints - timedelta(dayGap)))
        self.HistAverage = 1 + (sum([x-1 for x in self.HistRatioGains])/len(self.HistRatioGains))
        self.HistVariance = sum([pow(x-self.HistAverage,2) for x in self.HistRatioGains])/(len(self.HistRatioGains) - 1)
        self.HistSd = pow(self.HistVariance,1/2)
        
        
        
    
def main():
    A = StockHist()
    f = 'Boeing.csv'
    A.CsvToHist(f)
    print(len(A.Hist))
    Ad = date(2001,1,21)
    Bd = date(2002,1,21)
    #print(A.ClosingPrice(Ad))
    #print(A.ClosingPrice(Bd)) 
    #print(A.OneShareGain(Ad, Bd))
    #print(A.RatioGain(Ad, Bd))
    print(A.ExpectedGainInDays(1))
    print(A.ExpectedGainInDays(100))
    print(A.ExpectedGainRatioInDays(1))
    print(A.ExpectedGainRatioInYears(25))
    A.Stats(1)
    print(A.HistAverage)
    print(A.HistSd)
    A.Stats(365)
    print(A.HistAverage)
    print(A.HistSd)
    
            
if __name__ == '__main__':
    main()

    