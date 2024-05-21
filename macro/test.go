package main

import "fmt"

func print(o interface{}) {
	fmt.Println(o)
}

func main() {
	slice2 := []int{1, 5: 2, 10: 3}
	print(slice2)
}
