from Anime import Anime
from AnimeDataBase import AnimeDataBase

class AniUser:
    def __init__(self, name):
        self.Adb = AnimeDataBase()
        self.Adb.ImportFromFile('AnimeDataBase.csv')
        self.AnimeList:list[tuple[Anime, float]] = []
        self.name = name
    
    def AddAnimeScore(self,Anime:Anime, score: float):
        if(self.Adb.HasAnime(Anime)):
            Anime = self.Adb.LookUpAnime(Anime)
        self.AnimeList.append((Anime, score))
        
    def AnimeWatchedList(self) -> list[Anime]:
        out = []
        for A in self.AnimeList:
            out.append(A[0])
        return out
        
    def HasScored(self, Anime:Anime):
        for A in self.AnimeList:
            if(A[0] == Anime):
                return True
        return False
    
    def CsvToUser(self, FileName:str):
        f = open(FileName,'r',encoding='U8')
        Criteria = f.readline()
        Criteria = Criteria.strip()
        CriteriaL = Criteria.split(',')
        MaxScore = float(CriteriaL[1])
        while(f.readable()):
            ToAnime = f.readline()
            ToAnime = ToAnime.strip()
            if(ToAnime == ''):
                f.close()
                break
            ToAnimeParts = ToAnime.rsplit(",",1)
            AddAnime = Anime(ToAnimeParts[0])
            self.AddAnimeScore(AddAnime, NormalizeScore(float(ToAnimeParts[1]),MaxScore))
        f.close()
        
    def ExportAnimeList(self, fileName:str):
        f = open(fileName,'w',encoding='U8')
        for A in self.AnimeList:
            if(A==self.AnimeList[-1]):
                f.write(A[0].csvString())
            else:
                f.write(A[0].csvString()+'\n') 
        f.close()
        
    def ScoredAnimeList(self) -> list:
        out = []
        for A in self.AnimeList:
            out.append(A[0])     
        return out
    
    def GetScoreFor(self, Anime: Anime) -> float:
        for A in self.AnimeList:
            if(A[0] == Anime):
                return A[1]
        return -1
    
    def UpdateAnime(self, Anime: Anime):
        if(not self.HasScored(Anime)):
            return
        replaceTup:tuple = [Anime, self.GetScoreFor(Anime)]
        for e in self.AnimeList:
            if(e[0] == Anime):
                self.AnimeList.remove(e)
                self.AnimeList.append(replaceTup)
                break
        
            

def NormalizeScore(score:float, maxScore:float):
        return score/(maxScore + 1)
   
def main():
    A = Anime('Fruits Basket (2019)')
    B = Anime('Maid-sama')
    A.AddName('フルーツバスケット 1st Season')
    B.AddTag('Maids')
    A.AddTag('Zodiac')
    C = Anime('Horimiya')
    C.AddTag('Romance')
    A.AddTag('Romance')
    B.AddTag('Romance')
    A.AddTag('Shojo')
    B.AddTag('Shojo')
    A.AddName('Fruits Basket 1st Season')
    
    himeguma = AniUser('himeguma')
    himeguma.AddAnimeScore(A,NormalizeScore(10,10))
    himeguma.AddAnimeScore(B,NormalizeScore(10,10))
    himeguma.AddAnimeScore(C,NormalizeScore(7,10))
    
    himeguma = AniUser('himeguma')
    himeguma.CsvToUser('HimegumaCAnimeList.csv')
    print(himeguma.HasScored(A))
    print(himeguma.HasScored(C))
    himeguma.ExportAnimeList('himegumaAnimeList.csv')
    
    Kai = AniUser('Kai')
    Kai.CsvToUser('Kai.csv')
    
    Star = AniUser('Star')
    Star.CsvToUser('StarShowerC.csv')
    
    Adb = AnimeDataBase()
    Adb.ImportFromFile('AnimeDataBase.csv')
    Adb.IncludeAnimeList(Star.ScoredAnimeList())
    print(Kai.HasScored(C) == False)
    
    hanako = AniUser('Hanako')
    hanako.CsvToUser('HanakoCheeks.csv')
    Adb.IncludeAnimeList(hanako.ScoredAnimeList())
    Adb.ExportToFile('AnimeDataBase.csv')
    
if __name__ == '__main__':
    main()