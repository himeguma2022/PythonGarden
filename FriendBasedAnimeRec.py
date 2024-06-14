import math
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
from AniUser import AniUser
from Anime import Anime
from AnimeDataBase import AnimeDataBase
import itertools
import matplotlib.pyplot as plt
global Adb
Adb = AnimeDataBase()
if(Adb.Animes == []):
    Adb.ImportFromFile('AnimeDataBase.csv')
class FriendBasedAnimeRec:
    def __init__(self, UserList:list[AniUser]):
        AniDataPoints:dict[Anime:dict[str:float]] = dict()
        for U in UserList:
            for A in U.AnimeScores():
                if not A in AniDataPoints.keys():
                    AniDataPoints.update({A:dict()})
                normalizedScore = ReScore(U.min, U.max, U.GetScoreFor(A))
                AniDataPoints.get(A).update({U.name:normalizedScore})
        self.RawData = AniDataPoints
        self.Users = set(UserList)
        for U in self.Users:
            print("Predict for: "+U.name)
            self.Predict(U)
            
    def Predict(self, user:AniUser):
        Labelled = set(self.RawData.keys())
        for U in self.Users:
            Labelled.intersection_update(set(U.AnimeScores().keys()))
        Training = Labelled.copy()
        Test = set()
        for i in range(math.ceil(len(Labelled) / 4)):
            Test.add(Training.pop())

def ReScore(min:float, max:float, score:float) -> float:
    return 2*((score - min)/(max - min)) - 1        

def Distance(A:np, B:np) -> float:
    return pow(sum(pow(A-B,2)),1/2)
            
def main():
    Au = AniUser('himeguma')
    Bu = AniUser('Kai')
    Cu = AniUser('StarShower')
    Cu.CsvToUser('StarShowerC.csv')
    Bu.CsvToUser('Kai.csv')
    Au.CsvToUser('HimegumaCAnimeList.csv')
    #Atempt = FriendBasedAnimeRec([Au,Bu,Cu])
    Du = AniUser('HanakoCheeks')
    Du.CsvToUser('HanakoCheeks.csv')
    Attempt2 = FriendBasedAnimeRec([Au,Cu,Du])
    #Attempt3 = FriendBasedAnimeRec([Au, Bu, Du])
    #Attempt4 = FriendBasedAnimeRec([Au, Bu, Cu, Du])
    
        
if __name__ == '__main__':
    main()