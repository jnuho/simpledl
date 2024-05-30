package main

// Longest Substring Without Repeating Characters
// Given a string s, find the length of the longest substring without repeating characters.
func lengthOfLongestSubstring(s string) int {
	charMap := make(map[rune]int)
	maxlen := 0
	start := 0

	for i, char := range s {
		if lastIdx, found := charMap[char]; found && lastIdx >= start {
			start = lastIdx + 1
		}
		charMap[char] = i
		len := i - start + 1
		if len > maxlen {
			maxlen = len
		}
	}
	return maxlen
}
