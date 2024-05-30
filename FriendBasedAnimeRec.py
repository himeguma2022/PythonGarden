import math
import numpy as np
from AniUser import AniUser
from Anime import Anime
from AnimeDataBase import AnimeDataBase
import itertools

class FriendBasedAnimeRec:
    def __init__(self, AniUsers:list[AniUser]):
        self.AniUsers:set[AniUser] = set(AniUsers)
        self.AniDB = AnimeDataBase()
        self.AniDB.ImportFromFile('AnimeDataBase.csv')
        
        if(len(AniUsers) < 3):
            return
        for U in AniUsers:
            for tup in U.AnimeList:
                if(tup[0] in self.AniDB.Animes):  
                    U.UpdateAnime(self.AniDB.Animes[self.AniDB.Animes.index(tup[0])])
                    
        UserSets:list[set[AniUser]] = []
        for i in range(2,len(self.AniUsers)+1):
            adding = list(itertools.combinations(self.AniUsers,i))
            for e in adding:
                UserSets.append(e)
        CommonLists:dict[set[AniUser],list[Anime]] = dict()
        for l in UserSets:
            CommonLists.update({tuple(l):CommonList(l)})
        self.AnimeRawData = CommonLists
        for U in self.AniUsers:
            print("Predict for: "+U.name)
            self.Predict(U)
            
    def Predict(self, user:AniUser):
        LabelledSets:dict[str:list] = dict({'Animes':self.AnimeRawData.get(tuple(self.AniUsers)).copy()})
        TestSetsSize = max(1, math.floor(len(LabelledSets.get('Animes'))/4))
        for U in self.AniUsers:
            Scores:list[float] = []
            for A in LabelledSets.get('Animes'):
                Scores.append(U.GetScoreFor(A))
            LabelledSets.update({U.name:Scores})
        TestSet:dict[str:list] = dict({'Animes':[]})
        for U in set(LabelledSets.keys()).difference(set(['Animes'])):
            TestSet.update({U:[]})
        for i in range(TestSetsSize):
            A = LabelledSets.get('Animes').pop()
            if(len(LabelledSets.get('Animes'))<1):
                return
            TestSet.get('Animes').append(A)
            for U in set(LabelledSets.keys()).difference(set(['Animes'])):
                S = LabelledSets.get(U).pop()
                TestSet.get(U).append(S)
        HypothesizeOff:dict[str:list] = dict({'Animes':self.AnimeRawData.get(tuple(set(self.AniUsers).difference(set([user]))))})
        for U in set(self.AniUsers).difference(set([user])):
            Scores = []
            for A in HypothesizeOff.get('Animes'):
                Scores.append(U.GetScoreFor(A))
            HypothesizeOff.update({U.name:Scores})
        H_Scores:list[float] = []
        heading:list[Anime] = HypothesizeOff.get('Animes')
        axes = []
        for a in set(HypothesizeOff.keys()).difference(set(['Animes'])):
            axes.append(HypothesizeOff.get(a))
        for A in heading:
            H_Scores.append(dGuess(3, heading, axes, LabelledSets.get('Animes').copy(), LabelledSets.get(user.name).copy(), A))
            print(str(A)+": "+str(H_Scores[-1]))
        HypothesizeOff.update({user.name+"_h":H_Scores})
        AverageError = 0
        for A in TestSet.get('Animes'):
            scoreIndex = TestSet.get('Animes').index(A)
            hIndex = HypothesizeOff.get('Animes').index(A)
            AverageError += pow(TestSet.get(user.name)[scoreIndex] - HypothesizeOff.get(user.name+"_h")[hIndex],2)
        AverageError = pow(AverageError,1/2)/TestSetsSize
        print(AverageError)
        

def Guess(k:int, heading: list[Anime], axes:list[list[float]], labelledHeadings:list[Anime], userPoints:list[float], anime:Anime) -> float:
    if(k > len(userPoints)):
        return Guess(k-1,heading,axes,labelledHeadings,userPoints,anime)
    i = heading.index(anime)
    coords = []
    for a in axes:
        coords.append(a[i])
    distances = []
    for A in labelledHeadings:
        i = heading.index(A)
        dCoords = []
        for a in axes:
            dCoords.append(a[i])
        distances.append(Distance(np.array(coords), np.array(dCoords)))
    if(k == 1):
        return userPoints[distances.index(min(distances))]
    add = 0
    for i in range(k):
        minDex = distances.index(min(distances))
        add += userPoints[minDex]
        labelledHeadings.remove(labelledHeadings[minDex])
        userPoints.remove(userPoints[minDex])
        distances.remove(distances[minDex])
    return add/k

def dGuess(k:int, heading: list[Anime], axes:list[list[float]], labelledHeadings:list[Anime], userPoints:list[float], anime:Anime) -> float:
    if(k > len(userPoints)):
        return dGuess(k-1,heading,axes,labelledHeadings,userPoints,anime)
    i = heading.index(anime)
    coords = []
    for a in axes:
        coords.append(a[i])
    distances = []
    for A in labelledHeadings:
        i = heading.index(A)
        dCoords = []
        for a in axes:
            dCoords.append(a[i])
        distances.append(Distance(np.array(coords), np.array(dCoords)))
    if(k == 1):
        return userPoints[distances.index(min(distances))]
    weightsNums = []
    neighborsUsed = []
    for i in range(k):
        minDex = distances.index(min(distances))
        neighborsUsed.append(userPoints[minDex])
        weightsNums.append(distances[minDex])
        if(distances[minDex] == 0):
            return userPoints[minDex]
        labelledHeadings.remove(labelledHeadings[minDex])
        userPoints.remove(userPoints[minDex])
        distances.remove(distances[minDex])
    weightsDem = sum(pow(np.array(weightsNums),-2))
    return sum((np.array(pow(np.array(weightsNums),-2))/weightsDem)*np.array(neighborsUsed))

def Distance(A:np, B:np) -> float:
    return pow(sum(pow(A-B,2)),1/2)
    
       
def CommonList(UserLists:list[AniUser]) -> list:
    out = UserLists[0].ScoredAnimeList()
    for i in UserLists[1:]:
        check = out.copy()
        for A in check:
            if(not(i.HasScored(A))):
                out.remove(A)
    return out
        
def main():
    Au = AniUser('himeguma')
    Bu = AniUser('Kai')
    Cu = AniUser('StarShower')
    Cu.CsvToUser('StarShowerC.csv')
    Bu.CsvToUser('Kai.csv')
    Au.CsvToUser('HimegumaCAnimeList.csv')
    Atempt = FriendBasedAnimeRec([Au,Bu,Cu])
    Du = AniUser('HanakoCheeks')
    Du.CsvToUser('HanakoCheeks.csv')
    Attempt2 = FriendBasedAnimeRec([Au,Cu,Du])
    Attempt3 = FriendBasedAnimeRec([Au, Bu, Du])
    Attempt4 = FriendBasedAnimeRec([Au, Bu, Cu, Du])
    
        
if __name__ == '__main__':
    main()