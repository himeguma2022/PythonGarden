from datetime import date
class StockMoment:
    def __init__(self):
        pass
    
    def setAs(self, date: date, val: float):
        self.setVal(val)
        self.setDate(date)
        
    def setVal(self, val:float): 
        self.val = val
    
    def setDate(self, date: date) -> None:
        self.date = date
        
    def DayDifference(self, nextMoment: date) -> int: 
        return (self.date - nextMoment).days
    
    def ValueGain(self, nextVal:float):
        return nextVal - self.val
    
    def GainPerDay(self, nextMoment):
        return self.ValueGain(nextMoment.val)/self.DayDifference(nextMoment.date)
    
    def CsvToStockMoment(self, commaedText:str):
        newMoment = commaedText.split(sep=",") 
        self.setAs(self.StringToDate(newMoment[0]),newMoment[1])
    
    def StringToDate(self, dateString:str) -> date:
        yearMonthDay = dateString.split(sep="/")
        return date(int(yearMonthDay[-1]), int(yearMonthDay[0]), int(yearMonthDay[1]))

def main(): 
    A = StockMoment()
    A.setAs(date(2024,4,30),100)
    B = StockMoment()
    B.setAs(date(2020,4,29),90)
    print(A.DayDifference(B.date))
    print(B.DayDifference(A.date))
    print(A.ValueGain(B.val))
    print(A.GainPerDay(B))
if __name__ == '__main__':
    main()