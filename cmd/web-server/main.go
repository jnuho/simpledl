package main

import (
	"flag"

	"github.com/golang/glog"
	"github.com/jnuho/simpledl/backend/web"
)

func main() {

	// ./go-app -web-host=":3001"
	host := flag.String("web-host", ":3001", "Specify host and port for backend.")
	err := web.StartServer(*host)
	if err != nil {
		glog.Fatal(err)
	}
}
