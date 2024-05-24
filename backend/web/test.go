package main

import (
	"fmt"
)

func print(o ...interface{}) {
	fmt.Println(o...)
}

func main() {
	fmt.Println('a')
	fmt.Println("a")
	slice1 := make([]int, 3, 5)
	slice2 := append(slice1, 4, 5)
	slice3 := append(slice2, 6)

	// len() cap()
	fmt.Println("slice1: ", slice1, len(slice1), cap(slice1))
	fmt.Println("slice2: ", slice2, len(slice2), cap(slice2))
	// 새로운 capacity 적용된 배열은 다른 주소가리킴!
	fmt.Println("slice3: ", slice3, len(slice3), cap(slice3))

	// 문제1: slice1변경 시 둘다 바뀜
	slice1[1] = 100
	fmt.Println("After slice1[1]=100")
	fmt.Println("slice1: ", slice1, len(slice1), cap(slice1))
	fmt.Println("slice2: ", slice2, len(slice2), cap(slice2))
	// 새로운 capacity 적용된 배열은 다른 주소가리킴!
	fmt.Println("slice3: ", slice3, len(slice3), cap(slice3))

}
