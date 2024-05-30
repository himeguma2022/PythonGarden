from Anime import Anime

class AnimeDataBase:
    def __init__(self):
        self.Animes = []
    def AddAnime(self, Anime:Anime):
        if(self.HasAnime(Anime) == False):
            self.Animes.append(Anime)
    def ExportToFile(self, exportName:str):
        f = open(exportName,'w',encoding='U8')
        for A in self.Animes:
            if(A==self.Animes[-1]):
                f.write(A.csvString())
            else:
                f.write(A.csvString()+'\n') 
        f.close()
        
    def ImportFromFile(self, importName:str):
        f = open(importName,'r',encoding='U8')
        while(f.readable()):
            ToAnime = f.readline()
            ToAnime = ToAnime.strip()
            if(ToAnime == ''):
                f.close()
                break
            ToAnimeParts = ToAnime.split(", tags:")
            AnimeNames = ToAnimeParts[0].split(", Name: ")
            AddAnime = Anime(AnimeNames[0])
            AddAnime.AddNamesList(AnimeNames[1:])
            AnimeTags = []
            if(ToAnime.find(", tags: ") > 0):
                AnimeTags = ToAnimeParts[1].split(", ")
            AddAnime.AddTagsList(AnimeTags)
            self.AddAnime(AddAnime)
            AnimeTags = []
            
        f.close()
        
    def IncludeDB(self, Importing:object):
        if(type(Importing) != AnimeDataBase):
            pass
        I:AnimeDataBase = Importing
        
        for anime in I.Animes:
            if(anime in self.Animes):
                ReAdd:Anime = self.Animes.pop(self.Animes.index(anime))
                anime.Merge(ReAdd)
            self.AddAnime(anime)
        
    def HasAnime(self,Anime:Anime):
        return Anime in self.Animes
    
    def LookUpAnime(self, Anime:Anime) -> Anime:
        if(not self.HasAnime(Anime)):
            return None
        return self.Animes[self.Animes.index(Anime)]
    
    def IncludeAnimeList(self, List:list[Anime]):
        Adb = AnimeDataBase()
        for Anime in List:
            Adb.AddAnime(Anime)
        self.IncludeDB(Adb)
    

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
    B.AddName('Kaichou wa Maid-sama!')
    
    AdB = AnimeDataBase()
    AdB.AddAnime(A)
    print(AdB.HasAnime(A))
    print(AdB.HasAnime(B) == False)
    AdB.AddAnime(B)
    print(AdB.HasAnime(B))
    AdB.AddAnime(C)
    print(AdB.LookUpAnime(A))
    AdB.ExportToFile('AnimeDataBaseT.csv')
    
    AdB2 = AnimeDataBase()
    AdB2.ImportFromFile('AnimeDataBaseT.csv')
    print(AdB2.HasAnime(A))
    print(AdB2.HasAnime(C))
    AdB.IncludeDB(AdB2)
    AdB.ExportToFile('AnimeDataBaseT.csv')
    
    
    
if __name__ == '__main__':
    main()