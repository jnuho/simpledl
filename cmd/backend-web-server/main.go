package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/golang/glog"
)

type requestParam struct {
	URL string `json:"cat_url"`
}

type responseParam struct {
	URL    string `json:"cat_url"`
	STATUS int    `json:"status"`
}

func oneTimeOp() {
	fmt.Println("one time op start")
	time.Sleep(1 * time.Second)
	fmt.Println("one time op started")
}

// handle GET request from client
func getMethodHandler(c *gin.Context) {
	c.String(http.StatusOK, "OK")
}

func validateRequest(c *gin.Context) (*requestParam, error) {
	catObj := requestParam{}
	if err := c.BindJSON(&catObj); err != nil {
		return nil, fmt.Errorf("invalid request: %v", err)
	}

	// Validate URL format
	_, err := url.ParseRequestURI(catObj.URL)
	if err != nil {
		return nil, fmt.Errorf("invalid URL format: %v", err)
	}

	return &catObj, nil
}

// Send POST Request to another backend python server
func callPythonBackend(catURL string) (*responseParam, error) {
	jsonData, _ := json.Marshal(map[string]string{
		"cat_url": catURL,
	})
	resp, err := http.Post("http://be-py-service:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("request to python failed: %v", err)
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("reading python server response failed: %v", err)
	}

	var result responseParam
	err = json.Unmarshal(b, &result)
	if err != nil {
		return nil, fmt.Errorf("unmarshal python response body failed: %v", err)
	}

	return &result, nil
}

// handle POST request from client
// func postMethodHandler(c *gin.Context, done chan<- error) {
func postMethodHandler(c *gin.Context) {
	// log.Printf("Before python call\n")
	catObj, err := validateRequest(c)
	if err != nil {
		log.Println("Validation error: ", err)
		c.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		// done <- err // Send error to done channel
		return
	}

	// Python backend call
	result, err := callPythonBackend(catObj.URL)
	if err != nil {
		log.Println("Python backend call error:", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Error calling Python backend",
		})
		// done <- err // Send error to done channel
		return
	}
	// log.Printf("RESULT FROM Python ASGI SERVER!!! %v\n", result)

	// Response
	c.JSON(http.StatusOK, gin.H{
		"cat_url":       result.URL,
		"go-server":     "ok",
		"python-server": result.STATUS,
	})

	// done <- nil // No error, send nil to done channel
}

func StartServer(ctx context.Context, host string, done chan<- error) {
	var once sync.Once
	once.Do(oneTimeOp)

	// Router
	r := gin.Default()

	// Apply the CORS middleware to the router
	config := cors.Config{
		AllowOrigins:     []string{"*"}, // or use "*" to allow all origins
		AllowMethods:     []string{"POST", "GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}
	r.Use(cors.New(config))

	// GET endpoint
	r.GET("/healthz", func(c *gin.Context) {
		// getMethodHandler(c, done) // Pass done channel to getMethodHandler
		getMethodHandler(c)
	})

	// POST endpoint
	r.POST("/web/cat", func(c *gin.Context) {
		// postMethodHandler(c, done) // Pass done channel to postMethodHandler
		postMethodHandler(c)
	})

	r.POST("/weather", func(c *gin.Context) {
		// weatherHandler(c, done) // Pass done channel to postMethodHandler
		c.String(http.StatusOK, time.Now().Format(time.RFC3339)+"weather")
	})

	server := &http.Server{
		Addr:    host,
		Handler: r,
	}

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			done <- err
		}
	}()

	// blocks until the context ctx is canceled or times out. The Done method of a context returns a channel that is closed when the context is canceled or times out.
	// wait for a signal to shut down the server gracefully. The signal could come from an external source, such as a user interrupt (Ctrl+C) or a timeout.
	<-ctx.Done()

	// If the server does not shut down within 5 seconds, the context will be canceled, and the shutdown process will be forced to stop.
	ctxShutDown, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctxShutDown); err != nil {
		done <- fmt.Errorf("server shutdown failed: %v", err)
	}

	done <- nil
}

const (
	YYYYMMDD  = "2006-01-02"
	HHMMSS24h = "15:04:05"
)

func main() {
	host := flag.String("web-host", ":3001", "Specify host and port for backend.")
	flag.Parse()

	log.SetPrefix(time.Now().Format(YYYYMMDD+" "+HHMMSS24h) + ": ")
	log.SetFlags(log.Lshortfile)

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	done := make(chan error)
	go StartServer(ctx, *host, done)

	select {
	case err := <-done:
		if err != nil {
			fmt.Println("DDD")
			glog.Fatal(err)
		}
	case <-ctx.Done():
		fmt.Println("Context cancelled")
	}
}
