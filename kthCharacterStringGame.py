def kthCharacter(k: int) -> str:
    word = "a"
    for i in range(1, 10):
        word += genRightHalf(word)
    return word[k - 1]

def genRightHalf(word: str) -> str:
    l = list(word)
    n = list(map(nextChr, l))
    return ''.join(n)
    
def nextChr(word: chr) -> chr:
    if word == 'z':
        return 'a'
    else:
        return chr(ord(word) + 1)

def main():
    print(kthCharacter(1))   # Output: "a"
    print(kthCharacter(2))   # Output: "b" 
    print(kthCharacter(3))   # Output: "b"
    print(kthCharacter(4))   # Output: "c"
    print(kthCharacter(5))   # Output: "b"
    
    print(kthCharacter(27))  # Output: "a"
    

if __name__ == "__main__":  
    main()