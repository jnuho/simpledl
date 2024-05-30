package main

import "sort"

// Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
// The overall run time complexity should be O(log (m+n)).
func findMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	merged := append(nums1, nums2...)
	sort.Ints(merged)

	n := len(merged)
	if n%2 == 0 {
		mid1, mid2 := n/2-1, n/2
		return float64(merged[mid1]+merged[mid2]) / 2.0
	} else {
		mid := n / 2
		return float64(merged[mid])
	}
}
