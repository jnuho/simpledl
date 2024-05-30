package main

// Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
// You may assume that each input would have exactly one solution, and you may not use the same element twice.
// You can return the answer in any order.
// Example 1:
// Input: nums = [2,7,11,15], target = 9
// Output: [0,1]
// Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
func twoSum(nums []int, target int) []int {

	numMap := map[int]int{}
	for i, num := range nums {
		complement := target - num
		// ok: true if key exists in the map
		//	if ok == true: set j as the value
		//	if ok == false: set j is set to zero value of the map's value type
		if j, ok := numMap[complement]; ok {
			return []int{j, i}
		}
		numMap[num] = i
	}
	return nil
}
