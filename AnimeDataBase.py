from Anime import Anime

class AnimeDataBase:
    def __init__(self):
        self.AnimesID:dict[int:Anime] = dict()
        self.AnimesNameToID:dict[str:int] = dict()
        
    def AddAnime(self, Anime:Anime):
        if(not hasattr(Anime,'ID')):
            return 
        self.AnimesID.update({Anime.ID:Anime})
        for t in Anime.names:
            self.AnimesNameToID.update({t:Anime.ID})
                
    def ExportToFile(self, exportName:str):
        f = open(exportName,'w',encoding='U8')
        for t in self.AnimesNameToID.keys():
            f.write(t+'\t'+str(self.AnimesNameToID.get(t))+'\n')
        f.close()
        for A in self.AnimesID.values():
            A.AnimeToTxtFile()
        
        
    def ImportFromFile(self, importName:str):
        f = open(importName,'r',encoding='U8')
        while(f.readable()):
            AniData = f.readline()
            if(AniData == ''):
                break
            TitleID = AniData.rsplit('\t',1)
            self.AnimesNameToID.update({TitleID[0]:int(TitleID[1])})
        f.close()
        for id in set(self.AnimesNameToID.values()):
            A = Anime('')
            A.ImportAsFile(str(id)+'Anime.txt')
            self.AnimesID.update({id:A})
            
    def IsEmpty(self) -> bool:
        return set(self.AnimesID.keys()) == set([])  
        
    def HasAnime(self,Anime:str):
        return Anime in self.AnimesNameToID.keys()
    
    def LookUpAnime(self, Anime:str) -> Anime:
        if(not self.HasAnime(Anime)):
            return None
        return self.AnimesID.get(self.AnimesNameToID.get(Anime))


def main():
    A = Anime('Fruits Basket (2019)')
    A.AniListUpdate()
    B = Anime('Maid-sama')
    B.AniListUpdate()
    C = Anime('Kamisama Kiss')
    C.AniListUpdate()
    Adb = AnimeDataBase()
    Adb.AddAnime(A)
    Adb.AddAnime(B)
    Adb.AddAnime(C)
    Adb.ExportToFile("TestBase.txt")
    print(Adb.LookUpAnime('Kamisama Kiss').name)
    
    Adb2 = AnimeDataBase()
    Adb2.ImportFromFile("TestBase.txt")
    print(Adb2.LookUpAnime('Kamisama Kiss').name)
    
    
    
if __name__ == '__main__':
    main()