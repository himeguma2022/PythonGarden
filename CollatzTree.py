import pandas as pd
import numpy as np

slopes = [1/2, 3]
bias = [0, 1]

class CollatzNode:
    def __init__(self, value: int):
        self.value = value

    def add_child(self, child: 'CollatzNode'):
        self.children = child

    def __repr__(self):
        return f"CollatzNode(value={self.value})"

def collatzDict() -> dict:
    D = {1: CollatzNode(1)}
    updateAdd(D, next_collatz(1))
    return D

def updateAdd(D:dict, n:int):
    if n not in D:
        D.update({n: CollatzNode(n)})
        updateAdd(D, next_collatz(n))
    D.get(n).add_child(D.get(next_collatz(n)))
    
def colValList(D:dict, n:int) -> list:
    if n not in D:
        return []
    c = D.get(n)
    L = []
    while c.value not in L:
        L.append(c.value)
        if c.children:
            c = c.children
    return L

def next_collatz(n: int) -> int:
    return int(n * slopes[n % len(slopes)] + bias[n % len(bias)])

def main():
    A = collatzDict()
    for i in range(1, 1000000):
        updateAdd(A, i)
        print(str(i) + " Done!")
    #for i in range(1, 1000000):
        #print(colValList(A, i))
    
    
if __name__ == "__main__":
    main()