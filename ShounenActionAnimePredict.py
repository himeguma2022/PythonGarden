import json
import time
import requests
from Anime import Anime


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
        response = requests.post('https://graphql.anilist.co') 
        OutputAnimeList:list[Anime] = []
        for s in OutputAnimes:
            OutputAnimeList.append(FetchIntoAnime(s))
        labelledData = dict()
        for u in csvdata:
            labelledData.update({u[0]:UserCsvToList(u[1])})
        
        
def FetchIntoAnime(title:str) -> Anime:
    query = '''
    query ($title: String) { 
        Media (search:$title, type:ANIME) {
            id
            title {
                romaji
                english
                native
            }
            tags {
                name
                rank
            }
        }
    }
    ''' 

    url = 'https://graphql.anilist.co'

# Make the HTTP Api request
    variables = {
        'title': title
    }
    response = requests.post(url, json={'query': query, 'variables': variables})
    if(response.status_code == 429):
        time.sleep(60)
        print('429 occured with '+title)
        return FetchIntoAnime(title)
    if(response.status_code == 404):
        return None
    raw = response.text
    
    return StringToAnime(raw)       

def StringToAnime(raw:str) -> Anime:
    lraw:dict[str:dict[str:dict]] = json.loads(raw)
    llraw:dict[str:dict] = lraw.get('data')
    organizedIn:dict[str] = llraw.get('Media')
    titles:dict[str:str] = organizedIn.get('title')
    titleList:list[str] = list(set(titles.values()).difference(set([None])))
    out = Anime(titleList[0])
    if(len(titleList) > 1):
        out.AddNamesList(titleList[1:])
    out.setID(organizedIn.get('id'))
    tagTups:list[dict[str]] = organizedIn.get('tags')
    tags = []
    for tup in tagTups:
        tags.append(tup.get('name'))
    out.AddTagsList(tags)
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
        AddAnime = FetchIntoAnime(ToAnimeParts[0])
        if(AddAnime != None):
            out.update({AddAnime: float(ToAnimeParts[1])})
    f.close()
    return out

def main():
    A = ShounenActionAnimePredict([('LadyCassandra','LadyCassandra.csv'),('HanakoCheeks','HanakoCheeks.csv'),('StarShower','StarShowerC,csv')],[])       
if __name__ == '__main__':
    main()