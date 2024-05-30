package main

import (
	"testing"
)

func TestLengthOfLongestSubstring(t *testing.T) {
	// Define test cases
	tests := []struct {
		input string
		want  int
	}{
		{"abcabcbb", 3}, // Example: "abc"
		{"bbbbb", 1},    // Example: "b"
		{"pwwkew", 3},   // Example: "wke"
		{"", 0},         // Empty string
		{"aab", 2},      // Example: "ab"
		{"dvdf", 3},     // Example: "vdf"
		{"abcde", 5},    // No repeating characters
		{"abba", 2},     // Example: "ab"
		{"tmmzuxt", 5},  // Example: "mzuxt"
		{"abcdefg", 7},  // No repeating characters
		{"aabbcc", 2},   // Example: "ab" or "bc"
	}

	for _, tt := range tests {
		got := lengthOfLongestSubstring(tt.input)
		if got != tt.want {
			t.Errorf("Input: %s, got: %d, want: %d", tt.input, got, tt.want)
		}
	}
}
