import math
import numpy as np


class Neuron:
    def __init__(self, actFunc:str):
        self.actFunc = actFunc
        self.bias = 0
        self.weights = np.array([1])
    
    def setWeights(self, weights:np.ndarray[float]):
        self.weights = weights
        
    def setBias(self, bias:float):
        self.bias = bias
        
    def Activate(self, inp: float) -> float:
        match(self.actFunc):
            case 'binary':
                if(inp > 0):
                    return 1
                return 0
            case 'sigmoid':
                return 1/(1+math.exp(-inp))
            case 'tanh':
                return math.tanh(inp)
            case 'relu':
                return max(0,inp)
            case 'leaky relu':
                return max(0.01*inp,inp)
            case 'elu':
                if(inp >= 0):
                    return inp
                return math.exp(inp) - 1
            case _:
                return inp
    
    def WeightBiasSumPreActivate(self, inps:np.ndarray[float]) -> float:
        if(len(self.weights) != len(inps)):
            return sum(inps, self.bias)
        return sum(self.weights * inps, self.bias)
    
    def Eval(self, inps: np.ndarray[float]) -> float:
        return self.Activate(self.WeightBiasSumPreActivate(inps))
        
def main():
    A = Neuron('')
    i1 = np.array([1,2,3,4,5,6])
    i2 = -1 * i1
    print(A.Eval(i1))
    print(A.Eval(i2))
    w1 = np.array([1,-1,1,-1,1,-1])
    A.setWeights(w1)
    print(A.Eval(i1))
    print(A.Eval(i2))
    A.setBias(-10)
    print(A.Eval(i1))
    print(A.Eval(i2))
    
    B = Neuron('sigmoid')
    print(B.Eval(i1))
    print(B.Eval(i2))
    B.setWeights(w1)
    print(B.Eval(i1))
    print(B.Eval(i2))
    B.setBias(-10)
    print(B.Eval(i1))
    print(B.Eval(i2))
    
    
if __name__ == '__main__':
    main()
    