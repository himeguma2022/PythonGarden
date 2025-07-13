class Solution:
    def removeDuplicates(self, nums: list[int]) -> int:
        if len(nums) < 2:
            return nums[0] if nums else 0
        l = 0
        r = len(nums) - 1
        while l < r:
            if nums[l] == nums[l + 1]:
                nums.append(nums.pop(l))
                r -= 1
            else:
                l += 1
        return r + 1

def main():
    sol = Solution()
    print(sol.removeDuplicates([1, 2, 3, 4, 5, 5, 6, 7, 8, 8]))  # Example usage, should return 8
    print(sol.removeDuplicates([1, 1, 1, 1]))  # Example usage, should return 1
    print(sol.removeDuplicates([1]))  # Example usage, should return 1
    print(sol.removeDuplicates([]))  # Example usage, should return 0
    print(sol.removeDuplicates([0,0,1,1,1,2,2,3,3,4]))  # Example usage, should return 5
    
if __name__ == "__main__":
    main()
        