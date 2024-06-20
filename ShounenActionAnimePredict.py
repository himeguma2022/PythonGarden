
from Anime import Anime
from AnimeDataBase import AnimeDataBase
global Adb
global missingAnime
Adb = AnimeDataBase()
if(Adb.IsEmpty()):
    Adb.ImportFromFile('AnimeDataBase.txt')


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
    A = ShounenActionAnimePredict([('LadyCassandra','LadyCassandra.csv'),('HanakoCheeks','HanakoCheeks.csv'),('StarShower','StarShowerC.csv')],[])
    Adb.ExportToFile("AnimeDataBase.txt")  
    missingAnime = [set(missingAnime)]
    f = open("AniList Missing Anime.txt",'w',encoding='U8')
    for s in missingAnime:
        f.write(s+'\n')
    f.close()
         
if __name__ == '__main__':
    main()