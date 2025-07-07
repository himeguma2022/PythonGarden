class FindSumPairs(object):
    def __init__(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        """
        self.nums1D = {}
        while len(nums1) > 0:
            self.nums1D.update({nums1[0]: nums1.count(nums1[0])})
            removeAllFromList(nums1, nums1[0])
        self.nums2 = nums2.copy()
        self.nums2D = {}
        while len(nums2) > 0:
            self.nums2D.update({nums2[0]: nums2.count(nums2[0])})
            removeAllFromList(nums2, nums2[0])

    def add(self, index, val):
        """
        :type index: int
        :type val: int
        :rtype: None
        """
        rv = self.nums2D.get(self.nums2[index])
        self.nums2D.update({self.nums2[index]: rv - 1})
        if rv < 2:
            self.nums2D.pop(self.nums2[index])
        self.nums2[index] += val
        if self.nums2[index] not in self.nums2D:
            self.nums2D.update({self.nums2[index]: 0})
        self.nums2D.update({self.nums2[index]: self.nums2D.get(self.nums2[index]) + 1})

    def count(self, tot):
        """
        :type tot: int
        :rtype: int
        """
        result = 0
        for i in self.nums1D:
            if tot - i in self.nums2D:
                result += self.nums1D.get(i) * self.nums2D.get(tot - i)
        return result
    
def removeAllFromList(lst, val):
    """
    Helper function to remove all occurrences of val from lst.
    """
    while val in lst:
        lst.remove(val)
        

# Your FindSumPairs object will be instantiated and called as such:
# obj = FindSumPairs(nums1, nums2)
# obj.add(index,val)
# param_2 = obj.count(tot)

def test(m:list[str], p:list):
    for i in range(len(m)):
        match m[i]:
            case "FindSumPairs":
                n = FindSumPairs(p[i][0], p[i][1])
            case "count":
                print(n.count(p[i][0]))
            case "add":
                n.add(p[i][0], p[i][1])
        

def main():
    test(["FindSumPairs","count","add","count","count","add","add","count"],
         [[[1,1,2,2,2,3],[1,4,5,2,5,4]],[7],[3,2],[8],[4],[0,1],[1,1],[7]])
    
    
    
if __name__ == "__main__":
    main()