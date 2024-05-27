package main

import (
	"fmt"
)

func main() {
	found := util.BinarySearch(7, []int{1, 2, 5, 7, 23, 66, 99})
	fmt.Println(found)

}
