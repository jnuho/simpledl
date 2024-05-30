package main

// Given a string s, return the longest palindromic substring in s.
func longestPalindrome(s string) string {
	if len(s) < 1 {
		return ""
	}

	start, end := 0, 0
	for i := 0; i < len(s); i++ {
		len1 := expandAroundCenter(s, i, i)
		len2 := expandAroundCenter(s, i, i+1)
		maxLen := max(len1, len2)
		if maxLen > end-start {
			// if maxLen %2 == 1: maxLen/2 == (maxLen-1)/2
			// if maxLen %2 == 0: (maxLen-1)/2
			//	-> 두가지 케이스모두 (maxLen-1)/2
			start = i - (maxLen-1)/2
			end = i + maxLen/2
		}
	}

	return s[start : end+1]
}

func expandAroundCenter(s string, left, right int) int {
	for left >= 0 && right < len(s) && s[left] == s[right] {
		left--
		right++
	}
	return right - left - 1
}

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func isPalindrome(s string) bool {
	for i := range len(s) / 2 {
		if s[i] != s[len(s)-i-1] {
			return false
		}
	}
	return true
}
