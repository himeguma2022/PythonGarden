class Solution:
    cache = {}
    def climbStairs(self, n: int) -> int:
        if n < 3:
            return n
        if n in self.cache:
            return self.cache[n]
        self.cache[n] = self.climbStairs(n - 1) + self.climbStairs(n - 2)
        return self.cache[n]

def main():
    sol = Solution()
    print(sol.climbStairs(2))  # Output: 2
    print(sol.climbStairs(3))  # Output: 3
    print(sol.climbStairs(4))  # Output: 5
    print(sol.climbStairs(5))  # Output: 8
    print(sol.climbStairs(6))  # Output: 13 
    
if __name__ == "__main__":
    main()