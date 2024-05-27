package main

import "fmt"

func do(nums []int, target int) []int {
	// for i, v := range nums {

	// }
	for i := 0; i < len(nums); i++ {
		for j := i; j < len(nums); j++ {
			if target == nums[i]+nums[j] {
				return []int{i, j}
			}

		}
	}
	return nil
}

func main() {
	fmt.Println(do([]int{2, 7, 11, 15}, 9))
}
