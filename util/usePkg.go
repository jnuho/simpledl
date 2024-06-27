package main

import (
	"fmt"
	"time"

	"github.com/jnuho/simpledl/pkg"
)

func main() {
	startNow := time.Now()

	found := pkg.BinarySearch(7, []int{1, 2, 5, 7, 23, 66, 99})
	fmt.Println(found)
	str := pkg.GetWeatherInfo()
	fmt.Println(str)

	duration := time.Since(startNow).Seconds()
	fmt.Println(duration)
}
