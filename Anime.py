
from io import FileIO
import json
from msilib.schema import File
import time
import requests

global missingAnime
missingAnime:list[str] = []
f = open("AniList Missing Anime.txt","r",encoding='U8')
content:str = f.readline()
while(content != ''):
    missingAnime.append(content)
    content = f.readline()
f.close()

class Anime:
    def __init__(self, name:str) -> None:
        self.name = name
        self.names = set()
        self.names.add(name)
        self.tags = set()
        
    def setID(self, ID:int):
        self.ID = ID
    
    def __str__(self) -> str:
         return self.name
    
    def AddName(self, name:str):
        self.names.add(name.strip())
        
    def AddTag(self, tag:str):
        self.tags.add(tag.strip())
        
    def HasTag(self, tag:str) -> bool:
        return self.tags.__contains__(tag)
    
    def csvString(self) -> str:
        out = ''
        Added = set()
        for names in self.names:
            Added.add(names)
            if(self.names.difference(Added) == set()):
                out = out + names +', '
            else:
                out = out + names +', Name: '  
        out = out + 'tags: '
        Added = set()
        for tag in self.tags:
            Added.add(tag)
            if(self.tags.difference(Added) == set()):
                out = out + tag
            else:
                out = out + tag +', '
        return out
    
    def AddNamesList(self,Names:list):
        for name in Names:
            self.AddName(name)
    
    def AddTagsList(self,Tags:list):
        for tag in Tags:
            self.AddTag(tag)
            
    def AniListUpdate(self):
        if(self.name in missingAnime):
            return
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
            'title': self.name
        }
        response = requests.post(url, json={'query': query, 'variables': variables})
        if(response.status_code == 429):
            time.sleep(60)
            print('429 occured with '+self.name)
            return self.AniListUpdate()
        if(response.status_code == 404):
            f = open("AniList Missing Anime.txt",'a',encoding='U8')
            f.write(self.name+'\n')
            f.close()
            return None
        raw = response.text
        lraw:dict[str:dict[str:dict]] = json.loads(raw)
        llraw:dict[str:dict] = lraw.get('data')
        organizedIn:dict[str] = llraw.get('Media')
        titles:dict[str:str] = organizedIn.get('title')
        titleList:list[str] = list(set(titles.values()).difference(set([None])))
        self.name = titleList[0]
        self.names.add(self.name)
        if(len(titleList) > 1):
            self.AddNamesList(titleList[1:])
        self.setID(organizedIn.get('id'))
        tagTups:list[dict[str]] = organizedIn.get('tags')
        tags = []
        for tup in tagTups:
            tags.append(tup.get('name'))
        self.AddTagsList(tags)
        
    def AnimeToTxtFile(self):
        f:FileIO = open(str(self.ID)+'Anime.txt', 'w',encoding='U8')
        f.write('ID:\t'+str(self.ID)+'\n')
        for t in self.names:
            f.write('Title:\t'+t+'\n')
        for t in self.tags:
            f.write('Tag:\t'+t+'\n')
        f.close()
        
    def ImportAsFile(self, FileName:str):
        if(not FileName.endswith("Anime.txt")):
            return
        self.name = None
        self.names = set()
        f = open(FileName,'r',encoding='U8')
        while(f.readable()):
            AniData = f.readline()
            if(AniData == ''):
                break
            if(AniData.startswith('ID:\t')):
                self.setID(int(AniData.rsplit('ID:\t',1)[-1]))
            if(AniData.startswith('Title:\t')):
                self.AddName(AniData.rsplit('Title:\t',1)[-1])
            if(AniData.startswith('Tag:\t')):
                self.AddTag(AniData.rsplit('Tag:\t',1)[-1])
        if(self.name not in self.names):
            self.name = self.names.pop()
            self.names.add(self.name)
        f.close()
            
    def Merge(self, Matching:object):
        if(type(Matching) != Anime):
            return
        A2:Anime = Matching
        for name in A2.names.difference(self.names):
            self.AddName(name)
        for tag in A2.tags.difference(self.tags):
            self.AddTag(tag)
            
    def __hash__(self) -> int:
        return self.ID
        
def main():
    A = Anime('Fruits Basket (2019)')
    B = Anime('Maid-sama')
    print(A.name)
    print(B.name)
    A.AniListUpdate()
    B.AniListUpdate()
    print(A.name)
    print(B.name)
    A.AnimeToTxtFile()
    B.AnimeToTxtFile()
    C = Anime("")
    C.ImportAsFile(str(A.ID)+'Anime.txt')
    print(C.name)
    
    
if __name__ == '__main__':
    main()