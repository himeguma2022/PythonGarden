class ListNode(object):
     def __init__(self, val=0, next=None):
         self.val = val
         self.next = next
         
def addTwoNumbers(l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        if l1 is None:
            return l2
        if l2 is None:
            return l1
        if l1.val == 0 and l1.next is None:
            return l2
        if l2.val == 0 and l2.next is None:
            return l1
        
        result = ListNode(l1.val + l2.val)
        if result.val >= 10:
            result.val -= 10
            l1.next = addTwoNumbers(l1.next, ListNode(1))
        
        result.next = addTwoNumbers(l1.next, l2.next)
        return result
        
        
def main():
    # Example usage:
    l1 = ListNode(2, ListNode(4, ListNode(3)))
    l2 = ListNode(5, ListNode(6, ListNode(4)))
    
    result = addTwoNumbers(l1, l2)
    
    # Print the result
    while result:
        print(result.val, end=' ')
        result = result.next

if __name__ == "__main__":
    main()