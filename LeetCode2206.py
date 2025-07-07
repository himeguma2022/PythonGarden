class Solution:
    def divideArray(self, nums: List[int]) -> bool:
        keys = set(nums)
        for key in keys:
            if nums.count(key) % 2 != 0:
                return False
        return True
