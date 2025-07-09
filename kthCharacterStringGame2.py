class Solution(object):
    def kthCharacter(self, k, operations):
        """
        :type k: int
        :type operations: List[int]
        :rtype: str
        """
        
        word = "a"
        if k == 1:
            return word
        kb = list(bin(k - 1)[2:])
        kb.reverse()
        for b in range(len(kb)):
            if kb[b] == '1' and operations[b] == 1:
                if word == 'z':
                    word = 'a'
                else:
                    word = chr(ord(word) + 1)
        return word
        
       
def main():
    sol = Solution()
    print(sol.kthCharacter(5, [0, 0, 0]))  # Example usage, should return 'a'
    print(sol.kthCharacter(10, [0, 1, 0, 1]))  # Example usage, should return 'b'
    print(sol.kthCharacter(11552081, [0,0,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,0,1,0,1,1,1,1,0])) # Example usage, should return 'h' 
    print(sol.kthCharacter(28172699, [0,0,1,0,0,1,0,1,0,0,0,1,0,1,0,0,1,1,0,0,1,1,1,0,1])) # Example usage, should return 'f' 

if __name__ == "__main__":
    main()