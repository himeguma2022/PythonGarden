
import math
import random
from Anime import Anime
from AnimeDataBase import AnimeDataBase
import numpy as np 
import tensorflow as tf 
import matplotlib.pyplot as plt 
from keras import ops

class ShounenActionAnimePredict:
    def __init__(self, allDataFile:str, OutputAnimes:list[str]) -> None:
        OutputAnimeList:list[Anime] = []
        OutArrayAniIndex:dict[Anime:int] = dict()
        for s in OutputAnimes:
            OutputAnimeList.append(RetrieveAnime(s))
            OutArrayAniIndex.update({OutputAnimeList[-1]:len(OutputAnimeList) - 1})
        self.OutArrayAniIndex = OutArrayAniIndex
        self.OutputAnimeList = OutputAnimeList      
        allData:dict[str:dict[Anime:float]] = ExtractOutFile(allDataFile)
        self.allData:dict[str:dict[Anime:float]] = ExtractOutFile(allDataFile)
        dictData = PosNegRankScoreDict(self.allData)
        self.uScoreGuide = dictData[1]
        dictData2 = PosNegRankScoreDict(allData.copy())
        labelledData:dict[str:dict[Anime:float]] = dictData2[0]
        nonTrainTest:dict[str:dict[Anime:float]] = dict()     
        
        AniPopularity:dict[Anime:int] = dict()
        for u in allData:
            for A in allData.get(u):
                if(not A in AniPopularity.keys()):
                    AniPopularity.update({A:0})
                val = AniPopularity.get(A)
                val += 1
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
        self.inAnisIndex = inAnisIndex
        self.inAnis = inAnis
        
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
        epsPerFit = 10000
        model.fit(X_train, y_train,epochs=epsPerFit, verbose=0)
        
        self.model = model
        
    def Predict(self, predictFrom:np.ndarray) -> dict:
        if(len(predictFrom) != len(self.inAnis)):
            return None
        z:np.ndarray = self.model.predict(predictFrom)[0]
        out:dict[Anime:float] = dict()
        for A in range(self.OutputAnimeList):
            out.update({A:z[self.OutArrayAniIndex.get(A)]})
        return out
    
    def Test(self, predictFrom: np.ndarray, trueOut:dict[Anime:float]) -> dict:
        if(len(trueOut) != len(self.OutputAnimeList)):
            return None
        hOut = self.Predict(predictFrom)
        out = dict()
        for A in hOut:
            if(trueOut.get(A) == 0):
                out.update({A:0})
            else:
                out.update({A:math.pow(hOut.get(A) - trueOut.get(A),2)})
        return out
    
    def Plot2D(self, inDim:int, outDim:int, fixInPoint:np.ndarray):
        xIn = np.arange(-1, 1, 2/99)
        yOut = []
        for i in range(len(xIn)):
            fixInPoint[inDim] = xIn[i]
            yOut.append(self.model.predict(fixInPoint)[0][outDim])
        plt.plot(xIn,yOut)
        plt.show()
        
    def Plot3D(self, inDim1:int, inDim2:int, outDim:int, fixInPoint:np.ndarray):
        xIn = np.arange(-1, 1, 2/99)
        yIn = np.arange(-1, 1, 2/99)
        xIn, yIn = np.meshgrid(xIn, yIn)
        zOut = []
        for i in range(len(xIn)):
            fixInPoint[inDim1] = xIn[i]
            for j in range(len(xIn)):
                fixInPoint[inDim2] = yIn[j]
                zOut.append(self.model.predict(fixInPoint)[0][outDim])
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        surf = ax.plot_surface(xIn, yIn, zOut, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.plot(xIn,yIn,zOut)
        plt.show()

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
    A = ShounenActionAnimePredict(train,recFor)
    
    A.predict()
    Adb.ExportToFile("AnimeDataBase.txt")
         
if __name__ == '__main__':
    main()
