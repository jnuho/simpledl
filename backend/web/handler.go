package web

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"syscall"
)

type key int

const (
	serverKey key = iota
	queueKey
	cacheKey
	userKey
)

type Item struct {
	URL    string `json:"cat_url"`
	STATUS int64  `json:"status"`
}

type Server struct {
	rootCtx    context.Context
	rootCancel func()
	webURL     url.URL
	httpServer *http.Server

	donec chan struct{}
}

func with(h ContextHandler, srv *Server) ContextHandler {
	return ContextHandlerFunc(func(ctx context.Context, w http.ResponseWriter, req *http.Request) error {
		ctx = context.WithValue(ctx, serverKey, srv)
		// ctx = context.WithValue(ctx, queueKey, qu)
		// ctx = context.WithValue(ctx, cacheKey, cache)
		// ctx = context.WithValue(ctx, userKey, generateUserID(req))

		// CORS setting
		w.Header().Set("Access-Control-Allow-Origin", "*") // Allow any origin
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		w.Header().Set("Access-Control-Allow-Credentials", "true") // Allow credentials (cookies, etc.)

		// if r.Method == "OPTIONS" {
		// 	http.Error(w, "No Content", http.StatusNoContent)
		// 	return nil
		// }
		return h.ServeHTTPContext(ctx, w, req)
	})
}

func getRequestHandler(ctx context.Context, w http.ResponseWriter, r *http.Request) error {
	switch r.Method {
	case http.MethodGet:
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("pong"))
	default:
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return fmt.Errorf("method not allowed (%d): %v", http.StatusMethodNotAllowed, r.Method)
	}
	return nil
}

func validateRequest(w http.ResponseWriter, r *http.Request) (*Item, error) {
	err := r.ParseForm()
	if err != nil {
		http.Error(w, "Error parsing form data", http.StatusBadRequest)
		return nil, err
	}

	// Get the value of the "cat_url" parameter
	catURL := r.FormValue("cat_url")
	catObj := Item{URL: catURL, STATUS: http.StatusOK}

	return &catObj, nil
}

func postRequestHandler(ctx context.Context, w http.ResponseWriter, r *http.Request) error {
	catObj, err := validateRequest(w, r)
	if err != nil {
		http.Error(w, "Error parsing form data", http.StatusBadRequest)
		return err
	}

	switch r.Method {
	case http.MethodPost:
		// jsonData, _ := json.Marshal(map[string]string{
		// 	"cat_url": catURL,
		// })
		return json.NewEncoder(w).Encode(catObj)

	default:
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return fmt.Errorf("invalid request method: %v", r.Method)
	}
}

// func CORS(next http.HandlerFunc) http.HandlerFunc {
// 	return func(w http.ResponseWriter, r *http.Request) {
// 		w.Header().Set("Access-Control-Allow-Origin", "*") // Allow any origin
// 		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
// 		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
// 		w.Header().Set("Access-Control-Allow-Credentials", "true") // Allow credentials (cookies, etc.)

// 		if r.Method == "OPTIONS" {
// 			http.Error(w, "No Content", http.StatusNoContent)
// 			return
// 		}

// 		next(w, r)
// 	}
// }

func StartServer(scheme, hostPort string) (*Server, error) {
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
		webURL:     url.URL{Scheme: scheme, Host: hostPort},
		httpServer: &http.Server{Addr: hostPort, Handler: mux},
		donec:      make(chan struct{}),
	}

	// Create a channel to handle OS signals (e.g., Ctrl+C)
	// and registers the channel sigCh to receive notifications for specific OS signals.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Create a ServeMux
	mux.Handle("/ping", &ContextAdapter{
		ctx:     srv.rootCtx,
		handler: with(ContextHandlerFunc(getRequestHandler), srv),
	})

	mux.Handle("/web/cat", &ContextAdapter{
		ctx:     srv.rootCtx,
		handler: with(ContextHandlerFunc(postRequestHandler), srv),
	})

	// mux.HandleFunc("/ping", CORS(helloHandler))
	// mux.HandleFunc("/web/cat", CORS(helloHandler))
	// r.POST("/", postMethodHandler) // in k8s ingress env
	// // router.POST("/web/cat", postMethodHandler) // in docker env

	// Start HTTP server in a separate goroutine
	go func() {
		// Ensures that resources (goroutines, network connections, etc.) associated with the context
		// are properly cleaned up when the program exits.
		defer func() {
			srv.rootCancel()
		}()

		log.Printf("Server listening on %v\n", hostPort)
		if err := srv.httpServer.ListenAndServe(); err != nil {
			fmt.Println(err)
			log.Fatalf("%v", err)
		}

		// Wait for OS signals or context cancellation
		select {
		case <-sigCh:
			log.Println("Received interrupt signal. Shutting down gracefully...")
			srv.rootCancel() // Cancel the context
		case <-srv.rootCtx.Done():
			return
		case <-srv.donec:
			return
			// Context canceled (e.g., due to an error)
		default:
			close(srv.donec)
		}
	}()

	// Shutdown the server gracefully
	// if err := server.Shutdown(ctx); err != nil {
	if err := srv.httpServer.Shutdown(ctx); err != nil {
		log.Fatalf("Error shutting down server: %v\n", err)
	}
	return srv, nil
}

// StopNotify returns receive-only stop channel to notify the server has stopped.
func (srv *Server) StopNotify() <-chan struct{} {
	return srv.donec
}
