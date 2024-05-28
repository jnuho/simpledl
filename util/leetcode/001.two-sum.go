package main

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
