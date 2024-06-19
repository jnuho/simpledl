package web

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"os"
	"os/signal"
	"syscall"
)

type Response struct {
	CatURL       string `json:"cat_url"`
	GoServer     string `json:"go-server"`
	PythonServer int    `json:"python-server"`
}

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

type key int

const (
	serverKey key = iota
	queueKey
	cacheKey
	userKey
)

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

func validateCatRequest(w http.ResponseWriter, r *http.Request) (*Item, error) {
	decoder := json.NewDecoder(r.Body)
	var t Item
	err := decoder.Decode(&t)
	if err != nil {
		http.Error(w, "Error parsing form data", http.StatusBadRequest)
		return nil, err
	}
	log.Printf("catURL: %v\n", t.URL)

	if t.URL == "" {
		http.Error(w, "missing cat_url parameter", http.StatusBadRequest)
		return nil, fmt.Errorf("missing cat_url parameter %v", http.StatusBadRequest)
	}

	catObj := &Item{
		URL:    t.URL,
		STATUS: http.StatusOK,
	}

	return catObj, nil
}

// Send POST Request to another backend python server
func callPythonBackend(catURL string) (*Item, error) {
	jsonData, _ := json.Marshal(map[string]string{
		"cat_url": catURL,
	})
	resp, err := http.Post("http://be-py-service:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	// resp, err := http.Post("http://be-py:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("request to python failed: %v", err)
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("reading python server response failed: %v", err)
	}

	var result Item
	err = json.Unmarshal(b, &result)
	if err != nil {
		return nil, fmt.Errorf("unmarshal python response body failed: %v", err)
	}

	return &result, nil
}

func clientRequestHandler(ctx context.Context, w http.ResponseWriter, r *http.Request) error {
	switch r.Method {
	case http.MethodGet:
		if r.URL.Path == "/healthz" {
			log.Println(r.URL.Path)
			w.WriteHeader(http.StatusOK)
			w.Write([]byte("OK"))
			return nil
		}
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return fmt.Errorf("method not allowed (%d): %v", http.StatusMethodNotAllowed, r.Method)
	case http.MethodPost:
		catObj, err := validateCatRequest(w, r)
		if err != nil {
			http.Error(w, "Error parsing form data", http.StatusBadRequest)
			return err
		}
		result, err := callPythonBackend(catObj.URL)
		if err != nil {
			// log.Fatalln(err)
			// c.AbortWithStatus(http.StatusForbidden)
			// c.JSON(http.StatusInternalServerError, gin.H{
			// 	"message": "Error calling Python backend",
			// })
			return fmt.Errorf("error calling python backend: %v", err)
		}
		log.Printf("RESULT FROM Python ASGI SERVER!!! %v\n", result)

		// Response
		// c.JSON(http.StatusOK, catUrl)
		retObj := &Response{
			CatURL:       result.URL,
			GoServer:     "ok",
			PythonServer: int(result.STATUS),
		}
		log.Printf("RESPONSE DATA : %v\n", retObj)

		// Set response header to JSON
		w.Header().Set("Content-Type", "application/json")

		// jsonData, _ := json.Marshal(map[string]string{
		// 	"cat_url": catURL,
		// })
		if err := json.NewEncoder(w).Encode(retObj); err != nil {
			http.Error(w, "Error encoding response", http.StatusInternalServerError)
			log.Printf("Error encoding response: %v", err)
			return err
		}
		return nil

	default:
		http.Error(w, "Method Not Allowed", http.StatusMethodNotAllowed)
		return fmt.Errorf("method not allowed (%d): %v", http.StatusMethodNotAllowed, r.Method)
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
	rootCtx, rootCancel := context.WithCancel(context.Background())

	// Create a ServeMux
	mux := http.NewServeMux()

	// Define HTTP server abstraction and configuration
	webURL := url.URL{Scheme: scheme, Host: hostPort}
	srv := &Server{
		rootCtx:    rootCtx,
		rootCancel: rootCancel,
		webURL:     webURL,
		httpServer: &http.Server{Addr: webURL.Host, Handler: mux},
		donec:      make(chan struct{}),
	}

	// Create a ServeMux
	mux.Handle("/", &ContextAdapter{
		ctx:     rootCtx,
		handler: with(ContextHandlerFunc(clientRequestHandler), srv),
	})

	// Start HTTP server in a separate goroutine
	go func() {
		// Ensures that resources (goroutines, network connections, etc.) associated with the context
		// are properly cleaned up when the program exits.
		defer func() {
			srv.rootCancel()
		}()

		log.Printf("Server listening on %v\n", hostPort)
		if err := srv.httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("%v", err)
		}

		// Wait for OS signals or context cancellation
		select {
		// case <-sigCh:
		// 	log.Println("Received interrupt signal. Shutting down gracefully...")
		// 	srv.rootCancel() // Cancel the context
		// 	return

		// Wait for srv.rootCancel()
		case <-srv.rootCtx.Done():
			log.Println("srv.rootCtx.Done()")
			return
		// srv.donec is an unbuffered channel and receiving from an unbuffered channel blocks until a sender is ready.
		// so it's effectively used here for signal notification rather than data passing.
		case <-srv.donec:
			log.Println("<-srv.donec:")
			return
			// Context canceled (e.g., due to an error)
		default:
			log.Println("close(srv.donec)")
			close(srv.donec)
		}
	}()

	// Create a channel to handle OS signals (e.g., Ctrl+C)
	// and registers the channel sigCh to receive notifications for specific OS signals.
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// listens for OS signals and triggers graceful shutdown
	// Handle OS signals (e.g., Ctrl+C) for graceful shutdown
	go func() {
		sig := <-sigCh
		log.Printf("Received signal %v. Shutting down gracefully...\n", sig)
		close(srv.donec)
	}()

	return srv, nil
}

// StopNotify returns receive-only stop channel to notify the server has stopped.
func (srv *Server) StopNotify() <-chan struct{} {
	return srv.donec
}
