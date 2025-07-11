class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        l = 0
        m = 1
        if len(s) < 2:
            return len(s)
        lastCharPos = {s[l]:l}
        for c in range(1,len(s)):
            if s[c] in lastCharPos:
                m = max(m, c - l)
                l = max(lastCharPos.get(s[c]) + 1, l)
            lastCharPos.update({s[c]:c})
            if m >= len(s[l:]):
                return m
        return max(m, len(s) - l)
    
def main():
    s = Solution()
    print(s.lengthOfLongestSubstring("abcabcbb"))  # Example usage, should return 3
    print(s.lengthOfLongestSubstring("bbbbb"))     # Example usage, should return 1
    print(s.lengthOfLongestSubstring("pwwkew"))    # Example usage, should return 3
    print(s.lengthOfLongestSubstring("a"))         # Example usage, should return 1
    print(s.lengthOfLongestSubstring("au"))        # Example usage, should return 2
    print(s.lengthOfLongestSubstring("abba"))      # Example usage, should return 2
    print(s.lengthOfLongestSubstring("tmmzuxt"))      # Example usage, should return 5
    print(s.lengthOfLongestSubstring("wurdkgchlfnbukhflntsklzznfgsknrvldfcmaxsnvjbrgcblmbvwxnklscmgbxasfmgjbalmsncglvxmasxbqlcmadabnfldmsgvmjbgcvlsbfgvlmbsnsmefcrdsmb"))      # Example usage, should return 5
    
if __name__ == "__main__":
    main()