
from Anime import Anime
from AnimeDataBase import AnimeDataBase



class ShounenActionAnimePredict:
    def __init__(self,csvdata:list[(str, str)],Uin:list) -> None:
        OutputAnimes:list[str] = ["Shingeki no Kyojin",
                        "Kimetsu no Yaiba",
                        "Jujutsu Kaisen",
                        "Boku no Hero Academia",
                        "HUNTER×HUNTER (2011)",
                        "Hagane no Renkinjutsushi: FULLMETAL ALCHEMIST",
                        "NARUTO",
                        "ONE PIECE",
                        "BLEACH",
                        "Dragon Ball"]
        OutputAnimeList:list[Anime] = []
        for s in OutputAnimes:
            OutputAnimeList.append(RetrieveAnime(s))
        labelledData = dict()
        for u in csvdata:
            labelledData.update({u[0]:UserCsvToList(u[1])})
        nonTrainTest = dict()
        for u in Uin:
            nonTrainTest.update({u[0]:UserCsvToList(u[1])})
        AniPopularity = dict()
        for u in labelledData:
            for A in labelledData.get(u):
                if(not A in AniPopularity.keys()):
                    AniPopularity.update({A:0})
                val = AniPopularity.get(A)
                val += 1
                AniPopularity.update({A:val})
        inAnis = []
        while(len(inAnis) < 20):
            top = max(AniPopularity.values())
            for A in AniPopularity.keys():
                if(AniPopularity.get(A) == top):
                    AniPopularity.pop(A)
                if(A not in OutputAnimeList):
                    inAnis.append(A)
                    break
            
            
            
def RetrieveAnime(title: str) -> Anime:
    if(Adb.HasAnime(title)):
        return Adb.LookUpAnime(title)
    out:Anime = Anime(title)
    out.AniListUpdate()
    Adb.AddAnime(out)
    return out

def MediaListToAnimeList(raw:list) -> list[Anime]:
    out = []
    return out

def UserCsvToList(FileName:str) -> dict[Anime:float]:
    f = open(FileName,'r',encoding='U8')
    Criteria = f.readline()
    Criteria = Criteria.strip()
    CriteriaL = Criteria.split(',')
    out:dict[Anime:float] = dict()
    while(f.readable()):
        ToAnime = f.readline()
        ToAnime = ToAnime.strip()
        if(ToAnime == ''):
            f.close()
            break
        ToAnimeParts = ToAnime.rsplit(",",1)
        AddAnime = RetrieveAnime(ToAnimeParts[0])
        if(AddAnime != None and(hasattr(AddAnime, 'ID'))):
            out.update({AddAnime: float(ToAnimeParts[1])})
    f.close()
    return out

def main():
    global Adb
    Adb = AnimeDataBase()
    if(Adb.IsEmpty()):
        Adb.ImportFromFile('AnimeDataBase.txt')
    A = ShounenActionAnimePredict([('LadyCassandra','LadyCassandra.csv'),
                                   ('StarShower','StarShowerC.csv'),
                                   ('Neb','Neb.csv'),
                                   ('FakeName','FakeName.csv'),
                                   ('Hypersilver69','Hypersilver69.csv'),
                                   ('FinalShion','FinalShion.csv'),
                                   ('CultureKing','CultureKing.csv'),
                                   ('SuperVak','SuperVak.csv'),
                                   ('LoveKaga123','LoveKaga123.csv')
                                   ],[
                                    ('himeguma','himegumaCAnimeList.csv')
                                   ])
    Adb.ExportToFile("AnimeDataBase.txt")  
         
if __name__ == '__main__':
    main()