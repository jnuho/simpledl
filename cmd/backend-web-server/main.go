package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/golang/glog"
	"github.com/jnuho/simpledl/backend/web"
	"github.com/joho/godotenv"
)

const (
	YYYYMMDD  = "2006-01-02"
	HHMMSS24h = "15:04:05"
)

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	done := make(chan error)

	// Load environment variables
	go func() {
		if err := godotenv.Load(); err != nil {
			done <- fmt.Errorf("error loading .env file: %v", err)
			cancel()
		}
	}()

	host := flag.String("web-host", ":3001", "Specify host and port for backend.")
	flag.Parse()

	log.SetPrefix(time.Now().Format(YYYYMMDD+" "+HHMMSS24h) + ": ")
	log.SetFlags(log.Lshortfile)

	go func() {
		web.StartServer(ctx, *host, done)
	}()

	// Handle OS signals for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	select {
	case err := <-done:
		if err != nil {
			glog.Fatal(err)
		}
	case sig := <-sigChan:
		log.Printf("Received signal: %v. Shutting down...", sig)
		cancel()
	case <-ctx.Done():
		fmt.Println("Context cancelled")
	}
}
