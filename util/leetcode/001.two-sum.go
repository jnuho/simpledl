package main

import "fmt"

type pair struct {
	nums   []int
	target int
}

func twoSum(nums []int, target int) []int {
	m := map[int]int{}
	for i, v := range nums {
		m[v] = i
	}
	for i, v := range nums {
		j := m[target-v]
		if j {
			return []int{i, j}
		}
	}

	for i, num := range nums {
		complement := target - num
		// ok: whether the key exists in the map or not
		// if key exists; set j as the value and ok as true
		// if key does not exist; set j is set to zero value of the map's value type and ok as false
		if j, ok := m[complement]; ok {
			return []int{j, i}
		}
		m[num] = i
	}

	// for i, v := range nums {
	// }
	for i := 0; i < len(nums); i++ {
		for j := i + 1; j < len(nums); j++ {
			if target == nums[i]+nums[j] {
				return []int{i, j}
			}
		}
	}
	return nil
}

func main() {
	pairs := []pair{
		{nums: []int{2, 7, 11, 15}, target: 9},
		{nums: []int{3, 2, 4}, target: 6},
		{nums: []int{3, 3}, target: 6},
	}

	for _, pair := range pairs {
		fmt.Println(twoSum(pair.nums, pair.target))
	}

	// fmt.Println(twoSum([]int{2, 7, 11, 15}, 9))
	// twoSum([]int{2, 7, 11, 15}, 9)
}
