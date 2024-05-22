package main

import (
	"flag"

	"github.com/golang/glog"
)

func main() {

	// ./go-app -web-host=":3001"
	host := flag.String("web-host", ":3001", "Specify host and port for backend.")
	err := StartServer(*host)
	if err != nil {
		glog.Fatal(err)
	}
}
