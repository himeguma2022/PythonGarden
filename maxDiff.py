class Solution:
    def maximumDifference(self, nums: list[int]) -> int:
        diffs = []
        for n in range(len(nums) - 1):
            diffs.append(max(list(x - nums[n] for x in nums[n + 1:])))  # If no valid difference found, return -1
        if max(diffs) <= 0:
            return -1
        return max(diffs)
    
def main():
    s = Solution()
    print(s.maximumDifference([1, 5, 2, 10]))  # Example usage should return 9
    print(s.maximumDifference([7, 1, 5, 4]))   # Example usage should return 4
    print(s.maximumDifference([9, 4, 3, 2]))   # Example usage should return -1
    print(s.maximumDifference([999,997,980,976,948,940,938,928,924,917,907,907,881,878,864,862,859,857,848,840,824,824,824,805,802,798,788,777,775,766,755,748,735,732,727,705,700,697,693,679,676,644,634,624,599,596,588,583,562,558,553,539,537,536,509,491,485,483,454,449,438,425,403,368,345,327,287,285,270,263,255,248,235,234,224,221,201,189,187,183,179,168,155,153,150,144,107,102,102,87,80,57,55,49,48,45,26,26,23,15]))
    # Example usage should return -1
    

if __name__ == "__main__":
    main()