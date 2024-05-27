package main

import (
	"fmt"

	"github.com/jnuho/simpledl/pkg"
	"github.com/jnuho/simpledl/util/crawl"
)

func main() {
	found := pkg.BinarySearch(7, []int{1, 2, 5, 7, 23, 66, 99})
	fmt.Println(found)

	crawl.Crawl()
}
