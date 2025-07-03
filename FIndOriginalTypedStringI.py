def possibleStringCount(word: str) -> int:
    if len(word) < 2:
        return 1
    for i in range(len(word) - 1):
        if word[i] != word[i + 1]:
            return possibleStringCount(word[i + 1:]) + i
    return len(word)

def main():
    print(possibleStringCount("aabbcc"))  # Example usage, should return 4
    print(possibleStringCount("abc"))     # Example usage, should return 1  
    print(possibleStringCount("aab"))     # Example usage, should return 2
    print(possibleStringCount("a"))       # Example usage, should return 1
    print(possibleStringCount(""))         # Example usage, should return 1
    print(possibleStringCount("aa"))      # Example usage, should return 2
    print(possibleStringCount("ab"))      # Example usage, should return 1
    print(possibleStringCount("aabb"))     # Example usage, should return 3
    print(possibleStringCount("abab"))     # Example usage, should return 1
    print(possibleStringCount("abbcccc"))  # Example usage, should return 5
    print(possibleStringCount("abcd"))  # Example usage, should return 1
    print(possibleStringCount("aaaa"))  # Example usage, should return 4
    
if __name__ == "__main__":
    main()