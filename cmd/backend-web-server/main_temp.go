package main

import (
	"context"
	"flag"
	"log"

	"github.com/jnuho/simpledl/backend/web"
)

func main() {
	// `go run main.go -web-scheme=http -web-host=localhost:8181`
	webScheme := flag.String("web-scheme", "http", "Specify scheme for backend.")
	hostPort := flag.String("web-host", "localhost:3001", "Specify host and port for backend.")
	flag.Parse()

	// Log format
	log.SetFlags(log.Ltime)

	// Create a context with cancellation support
	_, cancel := context.WithCancel(context.Background())
	defer cancel()

	// func StartServer(scheme, hostPort string) (*Server, error) {
	srv, err := web.StartServer(*webScheme, *hostPort)
	if err != nil {
		log.Fatal(err)
	}

	select {
	case <-srv.StopNotify():
		log.Println("stopped web server")
	}

}
