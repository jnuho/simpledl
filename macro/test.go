package main

import (
	"flag"
	"fmt"
)

func print(o interface{}) {
	fmt.Println(o)
}

func main() {
	stringFlag := flag.String("web-port", ":3001", "Enter a string and have it printed back out.")
	flag.Parse()

	fmt.Println("You entered:", *stringFlag)
}
