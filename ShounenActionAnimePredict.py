
import math
import random
from Anime import Anime
from AnimeDataBase import AnimeDataBase
import numpy as np 
import tensorflow as tf 
import matplotlib.pyplot as plt 
from keras import ops

class ShounenActionAnimePredict:
    def __init__(self, allDataFile:str, targetUsers:list[str], OutputAnimes:list[str]) -> None:
        OutputAnimeList:list[Anime] = []
        self.targetUsers = targetUsers
        self.outputAnimeIndex:dict[Anime:int] = dict()
        for s in OutputAnimes:
            OutputAnimeList.append(RetrieveAnime(s))
            self.outputAnimeIndex.update({OutputAnimeList[-1]:len(OutputAnimeList) - 1})  
        self.OutputAnimeList = OutputAnimeList      
        allData:dict[str:dict[Anime:float]] = ExtractOutFile(allDataFile)
        self.allData:dict[str:dict[Anime:float]] = ExtractOutFile(allDataFile)
        dictData = PosNegRankScoreDict(self.allData)
        self.uScoreGuide = dictData[1]
        dictData2 = PosNegRankScoreDict(allData.copy())
        labelledData:dict[str:dict[Anime:float]] = dictData2[0]
        nonTrainTest:dict[str:dict[Anime:float]] = dict()
        for t in targetUsers:
            if(t in labelledData.keys()):
                nonTrainTest.update({t:labelledData.get(t)})
            else:
                nonTrainTest.update({t:dict()})     
        
        AniPopularity:dict[Anime:int] = dict()
        for u in allData:
            for A in allData.get(u):
                if(not A in AniPopularity.keys()):
                    AniPopularity.update({A:0})
                val = AniPopularity.get(A)
                val += 1
                if(u in targetUsers):
                    val += len(labelledData)
                AniPopularity.update({A:val})
                
        inAnis:list[Anime] = []
        inAnisIndex:dict[Anime:int] = dict()
        checked:list[Anime] = []
        while(len(inAnis) < math.ceil(2.5 * len(OutputAnimeList))):
            top:int = max(AniPopularity.values())
            for A in set(AniPopularity.keys()).copy():
                if(AniPopularity.get(A) == top):
                    AniPopularity.pop(A)
                    if((A not in OutputAnimeList) and not HasRelations(A,OutputAnimeList) and not HasRelations(A,checked)):
                        inAnis.append(A)
                        inAnisIndex.update({A:len(inAnis) - 1})
                    checked.append(A)
        
        yTrainData = dict()
        for u in labelledData:
            d = FilterAnimes(labelledData.get(u),OutputAnimeList)
            if(not OnlyZeros(d)):
                yTrainData.update({u:d})
                    
        xTrainData = dict()
        for u in yTrainData:
            d = FilterAnimes(labelledData.get(u),inAnis)
            if(not OnlyZeros(d)):
                xTrainData.update({u:d})    
        
        X_trainRaw:list[dict[Anime:float]] = list(xTrainData.values())
        X_train_List:list = []
        for e in X_trainRaw:
            vals:list[float] = list(e.values())
            X_train_List.append(np.array(vals))
        X_train = np.array(X_train_List)
        
        y_trainRaw:list[dict[Anime:float]] = list(yTrainData.values())
        y_train_List:list = []
        for e in y_trainRaw:
            vals = list(e.values())
            y_train_List.append(np.array(vals))
        y_train = np.array(y_train_List)
        
        
        model = tf.keras.models.Sequential([
            tf.keras.layers.Dense(units = 1, input_shape = [len(inAnis)]),
            tf.keras.layers.Dense(math.ceil((len(inAnis)+len(OutputAnimeList))/2),activation='tanh'),
            tf.keras.layers.Dense(math.ceil((len(inAnis)+len(OutputAnimeList))/2),activation='tanh'),
            tf.keras.layers.Dense(math.ceil((len(inAnis)+len(OutputAnimeList))/2),activation='tanh'),
            tf.keras.layers.Dense(len(OutputAnimeList),activation='tanh')
            ])
        
        xInInNums = []
        self.resultUIndex:dict[str:int] = dict()
        for u in nonTrainTest:
            filteredU = FilterAnimes(nonTrainTest.get(u), inAnis)
            vals = list(filteredU.values())
            xInInNums.append(np.array(vals))
            self.resultUIndex.update({u:len(xInInNums) - 1})
        xIn = np.array(xInInNums)
                
        model.compile(optimizer='adam',  
               
              # MAE error is good for
              # numerical predictions
              loss=my_loss_fn,
              run_eagerly=True) 
        epsPerFit = 100
        model.fit(X_train, y_train,epochs=epsPerFit, verbose=0)
        self.res = model.predict(xIn,verbose=0)
        self.predictedAnimes = OutputAnimes
        z = model.predict(X_train)
        
        
        self.EvalModel()
        fitTimes = 1
        missList = [self.iacc]
        while(fitTimes * epsPerFit < 1000):
            model.fit(X_train, y_train,epochs=epsPerFit,verbose=0)
            self.res = model.predict(xIn,verbose=0)
            self.EvalModel()
            missList.append(self.iacc)
            fitTimes += 1
        
        self.model = model
        
        
        ScoreResultsList = []
        for t in targetUsers:
            if(t in self.uScoreGuide):
                ScoreResultsList.append(ClassScoreArray(self.res[self.resultUIndex.get(t)],self.uScoreGuide.get(t)))
            else:
                ScoreResultsList.append(self.res[self.resultUIndex.get(t)])
        self.ScoreResults = np.array(ScoreResultsList)
                  
    def EvalModel(self):
        self.HData:dict[str:dict[Anime:float]] = dict()
        for u in self.targetUsers:
            d:dict[Anime:float] = dict()
            uix = self.resultUIndex.get(u)
            for a in self.OutputAnimeList:
                aix = self.outputAnimeIndex.get(a)
                d.update({a:self.res[uix][aix]})
            self.HData.update({u:d})
        self.TestDataPoints:dict[str:dict[Anime:float]] = dict()
        iaccSum = 0
        for u in self.targetUsers:
            if(u not in self.allData):
                break
            offAcc = dict()
            for a in self.OutputAnimeList:
                d = self.allData.get(u)
                hd:dict[Anime:float] = self.HData.get(u)
                AIacc = 0
                if(a in d):
                    AIacc = pow((d.get(a) - hd.get(a)),2)
                    iaccSum += AIacc
                offAcc.update({a:AIacc})
            self.TestDataPoints.update({u:offAcc})        
        self.iacc = pow(iaccSum,0.5)
        
    def printResults(self):
        print("Overall Inaccuracy: "+str(self.iacc))
        for u in self.TestDataPoints:
            print("Inaccuracies for : " + u)
            for A in self.TestDataPoints.get(u):
                print(A.name + ": " + str(self.TestDataPoints.get(u).get(A)))

def ClassScoreArray(hScores:np.array, scoreGuide:dict[float:float]) -> np.array:
    for i in range(len(hScores)):
        val = hScores[i]
        hScores[i] = ClassScore(val, scoreGuide)
    
    return hScores

def ClassScore(val:float, scoreGuide:dict[float:float]) -> float:
    return scoreGuide.get(min(scoreGuide, key=lambda x:abs(x-val)))

def ExtractOutFile(fileString:str) -> dict[str:dict[Anime:float]]:
    out = dict()
    f = open(fileString,"r",encoding='U8')
    content = f.readline()
    while(content != ''):
        content.strip()
        dataPointList = content.rsplit(',',2)
        uname = dataPointList[-1].strip()
        if(uname not in out.keys()):
            out.update({uname:dict()})
        targetDict:dict[Anime:float] = out.get(uname)
        AddAnime = RetrieveAnime(dataPointList[0])
        if(AddAnime != None and(hasattr(AddAnime, 'ID'))):
            targetDict.update({AddAnime: float(dataPointList[1])})
        content = f.readline()
    return out
        
                       
def PosNegRankScoreDict(userScores:dict[str:dict[Anime:float]]) -> list[dict, dict]:
    uGuide:dict[str:dict[float:float]] = dict()
    for u in userScores:
        od = userScores.get(u).copy()
        d = PosNegRankScore(userScores.get(u))
        userScores.update({u:d})
        uGuideD = ScoreToPosNeg(d, od)
        uGuide.update({u:uGuideD})
    return [userScores, uGuide]

def ScoreToPosNeg(posNegs:dict[Anime:float], originalScores:dict[Anime:float]) -> dict:
    out = dict()
    for a in posNegs:
        pn = posNegs.get(a)
        if(pn not in out):
            out.update({pn:originalScores.get(a)})
    return out

def PosNegRankScore(userScore:dict[Anime:float]) -> dict:
    vals = list(userScore.values())
    vals.sort()
    disVals = vals.copy()
    while(min(vals) in disVals):
        disVals.remove(min(vals))
    while(max(vals) in disVals):
        disVals.remove(max(vals))
        
    for a in userScore:
        oval = userScore.get(a)
        if(oval == min(vals)):
            userScore.update({a:-1})
        elif(oval == max(vals)):
            userScore.update({a:1})
        else:
            userScore.update({a:(2*(1+disVals.index(oval))/len(disVals))-1})
    return userScore
    

def FilterAnimes(ulist:dict, aniList:list) -> dict:
    out = dict()
    for a in aniList:
        if(a not in ulist.keys()):
            out.update({a:0})
        else:
            out.update({a:ulist.get(a)})
    return out

def RemoveZeros(ulist:dict) -> dict:
    for a in ulist.copy():
        if(ulist.get(a) == 0):
            ulist.pop(a)
    return ulist             
            
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

def HasRelations(A:Anime, L:list[Anime]):
    if(A in L):
        return True
    for a in L:
        if(a.Related(A.ID)):
            return True
    return False

def OnlyZeros(d:dict) -> bool:
    for e in d.values():
        if(e != 0):
            return False
    return True

def my_loss_fn(y_true:tf.Tensor, y_pred:tf.Tensor):
    copyY = y_true.numpy()
    yPredAsArray = y_pred.numpy()
    for i in range(len(copyY)):
        for j in range(len(copyY[i])):
            original = copyY[i][j]
            if(original == 0):
                copyY[i][j] = yPredAsArray[i][j]
    tensorY = tf.convert_to_tensor(copyY)
    squared_difference = ops.square(tensorY - y_pred)
    return ops.mean(squared_difference, axis=-1)  # Note the `axis=-1`

def CalcAverageOfManyModels(modelsData:np.ndarray) -> np.ndarray:
    out = np.ndarray(shape=modelsData[0].shape)
    for u in range(len(out)):
        for a in range(len(out[u])):
            out[u][a] = np.mean(modelsData[:,u,a])
    return out

def CalcStdOfManyModels(modelsData:np.ndarray) -> np.ndarray:
    out = np.ndarray(shape=modelsData[0].shape)
    for u in range(len(out)):
        for a in range(len(out[u])):
            out[u][a] = np.std(modelsData[:,u,a])
    return out
    
def main():
    global Adb
    Adb = AnimeDataBase()
    recFor:list[str] = ["Shingeki no Kyojin",
                        "Kimetsu no Yaiba",
                        "Jujutsu Kaisen",
                        "Boku no Hero Academia",
                        "HUNTER×HUNTER (2011)",
                        "Hagane no Renkinjutsushi: FULLMETAL ALCHEMIST",
                        "NARUTO",
                        "ONE PIECE",
                        "BLEACH",
                        "Dragon Ball"]
    if(Adb.IsEmpty()):
        Adb.ImportFromFile('AnimeDataBase.txt')
    print("Database Loaded!")
    train = "AniListUserData.csv"
    resultsList = []
    for i in range(10):
        A = ShounenActionAnimePredict(train,['Himeguma','new'],recFor)
        resultsList.append(A.ScoreResults)
    
    results = np.array(resultsList)
    meanResults = CalcAverageOfManyModels(results)
    stdResults = CalcStdOfManyModels(results)
    print(meanResults)
    print(stdResults)
    
    Adb.ExportToFile("AnimeDataBase.txt")
         
if __name__ == '__main__':
    main()
