package main

import "fmt"

func main() {
	s1 := "Hello"
	s2 := "Hell"
	s3 := "Hello"

	fmt.Printf("%s == %s, %v\n", s1, s2, s1 == s2)
	fmt.Printf("%s == %s, %v\n", s1, s3, s1 == s3)

	str1 := "BBB"
	str2 := "aaaaAAA"
	str3 := "BBAD"
	str4 := "ZZZ"

	fmt.Printf("%s > %s, %v\n", str1, str2, str1 > str1)
	fmt.Printf("%s <= %s, %v\n", str3, str4, str3 <= str4)
}
