package main

import (
	"context"
	"flag"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"syscall"
	// "github.com/jnuho/simpledl/backend/web"
)

func main() {
	// `go run main.go -web-scheme=http -web-host=localhost:8181`
	webScheme := flag.String("web-scheme", "http", "Specify scheme for backend.")
	hostPort := flag.String("web-host", "localhost:3001", "Specify host and port for backend.")
	flag.Parse()

	// Log format
	log.SetFlags(log.Ltime)

	// Create a context with cancellation support
	ctx, cancel := context.WithCancel(context.Background())

	// Create a ServeMux
	mux := http.NewServeMux()

	// Define HTTP server abstraction and encapsulation of server configuration
	srv := &Server{
		rootCtx:    ctx,
		rootCancel: cancel,
		webURL:     url.URL{Scheme: *webScheme, Host: *hostPort},
		httpServer: &http.Server{Addr: *hostPort, Handler: mux},
	}

	// Create a channel to handle OS signals (e.g., Ctrl+C)
	// and registers the channel sigCh to receive notifications for specific OS signals.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Create a ServeMux
	mux.HandleFunc("/ping", CORS(getRequestHandler))
	mux.HandleFunc("/web/cat", CORS(postRequestHandler))
	// mux.HandleFunc("/ping", CORS(helloHandler))
	// mux.HandleFunc("/web/cat", CORS(helloHandler))
	// r.POST("/", postMethodHandler) // in k8s ingress env
	// // router.POST("/web/cat", postMethodHandler) // in docker env

	// Start HTTP server in a separate goroutine
	go func() {
		// Ensures that resources (goroutines, network connections, etc.) associated with the context
		// are properly cleaned up when the program exits.
		defer func() {
			cancel()
		}()

		log.Printf("Server listening on %v\n", *hostPort)
		if err := srv.httpServer.ListenAndServe(); err != nil {
			log.Fatalf("%v", err)
		}
	}()

	// Wait for OS signals or context cancellation
	select {
	case <-sigCh:
		log.Println("Received interrupt signal. Shutting down gracefully...")
		cancel() // Cancel the context
	case <-ctx.Done():
		// Context canceled (e.g., due to an error)
	}

	// Shutdown the server gracefully
	// if err := server.Shutdown(ctx); err != nil {
	if err := srv.httpServer.Shutdown(ctx); err != nil {
		log.Fatalf("Error shutting down server: %v\n", err)
	}
}
