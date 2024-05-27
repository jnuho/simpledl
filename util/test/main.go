package main

import (
	"fmt"

	"github.com/jnuho/simpledl/util/expkg"
)

func main() {
	found := expkg.BinarySearch(7, []int{1, 2, 5, 7, 23, 66, 99})
	fmt.Println(found)

}
