
class AniUser:
    def __init__(self, name):
        self.AnimeList:dict[str: float] = dict()
        self.name = name
        self.min = 10000000.0
        self.max = -1
    
    def AddAnimeScore(self,Anime:str, score: float):
        self.AnimeList.update({Anime:score})
        if score < self.min:
            self.min = score
        if score > self.max:
            self.max = score
        
    def HasScored(self, Anime:str):
        return Anime in self.AnimeList.keys()
    
    def CsvToUser(self, FileName:str):
        f = open(FileName,'r',encoding='U8')
        Criteria = f.readline()
        Criteria = Criteria.strip()
        CriteriaL = Criteria.split(',')
        while(f.readable()):
            ToAnime = f.readline()
            ToAnime = ToAnime.strip()
            if(ToAnime == ''):
                f.close()
                break
            ToAnimeParts = ToAnime.rsplit(",",1)
            AddAnime = ToAnimeParts[0]
            self.AddAnimeScore(AddAnime, float(ToAnimeParts[1]))
        f.close()
        
    def ScoredAnimeList(self) -> list:    
        return [self.AnimeList.keys()]
    
    def AnimeScores(self) -> dict:
        out:dict[str:dict[str:float]] = dict()
        for A in self.AnimeList:
            out.update({A:dict()})
            out.get(A).update({self.name:self.AnimeList.get(A)})
        return out
    
    def GetScoreFor(self, Anime: str) -> float:
        return self.AnimeList.get(Anime)
   
def main():
    
    himeguma = AniUser('himeguma')
    himeguma = AniUser('himeguma')
    himeguma.CsvToUser('HimegumaCAnimeList.csv')
    
    Kai = AniUser('Kai')
    Kai.CsvToUser('Kai.csv')
    
    Star = AniUser('Star')
    Star.CsvToUser('StarShowerC.csv')
    
    
    hanako = AniUser('Hanako')
    hanako.CsvToUser('HanakoCheeks.csv')
    
if __name__ == '__main__':
    main()