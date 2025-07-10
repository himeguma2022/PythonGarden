class Solution:
    def countBits(self, n: int) -> list[int]:
        if n == 0:
            return [0]
        if n == 1:
            return [0, 1]
        if n & (n-1) == 0:
            out = self.countBits(n - 1)
            out.append(1)  # If n is a power of 2, the count of bits is one more than the previous number
            return out
        rightPart = 2**(len(bin(n)[2:]) - 1)  # Get the number without the rightmost set bit
        leftPart = n - rightPart  # Get the rightmost set bit
        out = self.countBits(rightPart)  # Count the rightmost set bit
        remainingBits = self.countBits(leftPart)[1:]
        out.extend(list(r + 1 for r in remainingBits))  # Add the count of the left part
        return out
        
def main():
    s = Solution()
    print(s.countBits(5000))  # Example usage, should return [0, 1, 1, 2, 1, 2]
    
if __name__ == '__main__':
    main()