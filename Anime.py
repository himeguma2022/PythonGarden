import math


class Anime:
    def __init__(self, name:str) -> None:
        self.names = set()
        self.names.add(name)
        self.tags = set()
        
    def __eq__(self, value: object) -> bool:
        if(type(value) != Anime):
            return False
        return (self.names & value.names) != set()
    
    def __str__(self) -> str:
         out = self.names.pop()
         self.names.add(out)
         return out
    
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
            
    def Merge(self, Matching:object):
        if(type(Matching) != Anime):
            return
        A2:Anime = Matching
        for name in A2.names.difference(self.names):
            self.AddName(name)
        for tag in A2.tags.difference(self.tags):
            self.AddTag(tag)
            
        
def main():
    A = Anime('Fruits Basket (2019)')
    B = Anime('Maid-sama')
    A.AddName('フルーツバスケット 1st Season')
    print((A==B) == False)
    C = Anime('フルーツバスケット 1st Season')
    C.AddTag('Zodiac')
    print(A==C)
    B.AddTag('Maids')
    print(A.HasTag('Maids') == False)
    print(B.HasTag('Maids'))
    print(A.csvString())
    print(B.csvString())
    A.Merge(C)
    print(A.csvString())
    
if __name__ == '__main__':
    main()