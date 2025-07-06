class Solution(object):
    recallDict = {}
    
    def kthCharacter(self, k, operations):
        """
        :type k: int
        :type operations: List[int]
        :rtype: str
        """
        
        word = "a"
        if k == 1:
            return word
        for op in operations:
            if op == 0:
                word += word
            else:
                word += self.genRightHalf(word, len(word)//2)
            if k - 1 < len(word):
                return word[k - 1]
        return word[k - 1]
    
    def genRightHalf(self, word, frameLength):
        lookUpFrames = []
        if len(word) < 2:
            return self.generateWord(word)
        for i in range(0, len(word)//frameLength):
            lookUpFrames.append(self.lookUpWord(word[i*frameLength:(i+1)*frameLength]))
        rightHalf = ""
        for f in range(len(lookUpFrames)):
            if lookUpFrames[f] == "":
                rightHalf += self.genRightHalf(word[f*frameLength:(f+1)*frameLength], frameLength//2)
            else:
                rightHalf += lookUpFrames[f]
        
        self.recallDict.update({word: rightHalf})
        return rightHalf
    
    def generateWord(self, word):
        res = ""
        for char in word:
            if char == 'z':
                res += 'a'
            else:
                res += chr(ord(char) + 1)
        return res
                
    def lookUpWord(self, word):
        if word in self.recallDict:
            return self.recallDict.get(word)
        return ""
        
        
        
def main():
    sol = Solution()
    print(sol.kthCharacter(5, [0, 0, 0]))  # Example usage, should return 'a'
    print(sol.kthCharacter(10, [0, 1, 0, 1]))  # Example usage, should return 'b'
    print(sol.kthCharacter(11552081, [0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,0])) # Example usage, should return 'h' 
    print(sol.kthCharacter(28172699, [0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,1,1,0,1])) # Example usage, should return 'f' 

if __name__ == "__main__":
    main()